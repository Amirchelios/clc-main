"""Git-based file updater for GitHub Actions."""

import os
import subprocess
import time
from typing import List, Tuple, Optional
from utils.logger import log


class GitUpdater:
    """Handles git commit and push operations for GitHub Actions."""
    
    def __init__(self, repo_dir: str = None, output_prefix: str = "githubmirror"):
        if repo_dir is None:
            self.repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        else:
            self.repo_dir = repo_dir
        
        self.output_prefix = output_prefix.strip("/")
        log(f"GitUpdater initialized for: {self.repo_dir}")
    
    def _run_git(self, *args, check: bool = True, timeout: int = 60) -> subprocess.CompletedProcess:
        """Run git command with timeout."""
        cmd = ["git"] + list(args)
        log(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_dir,
                capture_output=True,
                text=True,
                check=check,
                timeout=timeout
            )
            
            if result.stdout:
                log(f"Git output: {result.stdout.strip()}")
            if result.stderr:
                log(f"Git stderr: {result.stderr.strip()}")
            
            return result
        except subprocess.TimeoutExpired:
            log(f"Git command timed out: {' '.join(cmd)}")
            raise
        except subprocess.CalledProcessError as e:
            log(f"Git command failed: {e.stderr}")
            raise
    
    def configure_git(self):
        """Configure git user for commits."""
        log("Configuring git user...")
        self._run_git("config", "user.name", "GitHub Actions")
        self._run_git("config", "user.email", "actions@github.com")
        log("Git user configured")
    
    def pull(self, branch: Optional[str] = None):
        """Pull latest changes from remote with rebase."""
        if branch is None:
            # Try to get branch from environment variable (GitHub Actions)
            branch = os.environ.get("GITHUB_REF_NAME")
            if not branch:
                result = self._run_git("rev-parse", "--abbrev-ref", "HEAD")
                branch = result.stdout.strip()
        
        log(f"Pulling from origin/{branch}...")
        try:
            # First stash any local changes (can happen with temp files)
            self._run_git("stash", "push", "-m", "Auto-stash before pull", check=False)
            
            # Now pull with rebase
            self._run_git("pull", "--rebase", "origin", branch)
            log("Pull successful")
            
            # Pop stash if it was created
            self._run_git("stash", "pop", check=False)
        except subprocess.CalledProcessError as e:
            if "cannot pull with rebase" in e.stderr.lower() or "unstaged changes" in e.stderr.lower():
                # Force reset to clean state
                log("Warning: Had unstaged changes, resetting to clean state...")
                self._run_git("reset", "--hard", "HEAD", check=False)
                self._run_git("clean", "-fd", check=False)
                # Try pull again
                self._run_git("pull", "--rebase", "origin", branch)
                log("Pull successful after reset")
            else:
                raise
    
    def stage_files(self, file_pairs: List[Tuple[str, str]]):
        """Stage only the files explicitly produced by the current run."""
        log("Staging generated files...")

        staged_paths = set()
        for local_path, remote_path in file_pairs:
            if not local_path:
                continue
            rel_path = os.path.relpath(local_path, self.repo_dir)
            staged_paths.add(rel_path)

        if not staged_paths:
            log("No generated files to stage")
            return

        # Use force add so newly created tracked/untracked outputs are included,
        # but only for the exact files returned by the generator.
        for rel_path in sorted(staged_paths):
            self._run_git("add", "-f", "--", rel_path, check=False)

        log(f"Staging complete: {len(staged_paths)} file(s)")
    
    def has_changes(self) -> bool:
        """Check if there are staged changes."""
        try:
            result = self._run_git("diff", "--cached", "--quiet", check=False)
            return result.returncode != 0
        except Exception:
            return False
    
    def commit(self, message: str = "Update VPN configs") -> bool:
        """Commit staged changes."""
        if not self.has_changes():
            log("No changes to commit (working tree clean)")
            # Display status for debugging in Action logs
            self._run_git("status", check=False)
            return False

        log(f"در حال ثبت تغییرات (Commit): {message}")
        # Use --allow-empty to be safe in CI environments
        self._run_git("commit", "-m", "به‌روزرسانی خودکار کانفیگ‌ها", "--allow-empty")
        return True
    
    def push(self, branch: Optional[str] = None, force: bool = False):
        """Push commits to remote."""
        if branch is None:
            branch = os.environ.get("GITHUB_REF_NAME")
            if not branch:
                result = self._run_git("rev-parse", "--abbrev-ref", "HEAD")
                branch = result.stdout.strip()
        
        if branch == "HEAD" or not branch or "detached" in branch or branch == "main":
            # Explicitly target 'main' in GitHub Actions
            branch = "main"
            
        log(f"Pushing to origin {branch}...")
        
        if force:
            self._run_git("push", "--force", "origin", f"HEAD:{branch}")
        else:
            self._run_git("push", "origin", f"HEAD:{branch}")
        
        log("Push successful")
    
    def commit_and_push_files(self, file_pairs: List[Tuple[str, str]], 
                               commit_message: str = "Update VPN configs",
                               max_retries: int = 3) -> bool:
        """Complete workflow with retry logic for push conflicts.
        
        Note: In GitHub Actions, repo is already up-to-date from checkout step,
        so we skip the pull to avoid conflicts with generated files.
        """
        log("Starting git commit and push workflow...")
        
        try:
            self.configure_git()
            
            # Skip pull in GitHub Actions - repo is already up-to-date from checkout
            
            self.stage_files(file_pairs)
            
            if not self.has_changes():
                log("Warning: No changes detected in the local repository to commit.")
                # Optionally list files to see what's happening
                self._run_git("status", check=False)
                return True
            
            # Retry loop for push conflicts
            for attempt in range(max_retries):
                if self.commit(commit_message):
                    try:
                        self.push()
                        log("Git workflow completed successfully")
                        return True
                    except subprocess.CalledProcessError as e:
                        log(f"Push failed due to potential conflict. Attempting to pull and rebase...")
                        self.pull() # Pull before retrying to resolve remote conflicts
                        if attempt < max_retries - 1:
                            wait_time = (attempt + 1) * 5
                            log(f"Push failed (attempt {attempt + 1}/{max_retries}), waiting {wait_time}s...")
                            time.sleep(wait_time)
                            # In GitHub Actions, just retry push (no pull needed)
                        else:
                            log(f"Push failed after {max_retries} attempts: {e.stderr}")
                            return False
                else:
                    log("Commit failed or no changes")
                    return False
            
            return False
            
        except Exception as e:
            log(f"Git workflow failed with error: {e}")
            return False
