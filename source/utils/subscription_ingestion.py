"""Subscription ingestion, normalization, and safety limits."""

import base64
import json
import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


SUPPORTED_PROTOCOLS = ("vless", "vmess", "trojan", "ss", "hysteria2", "hy2")
_PROTOCOL_RE = re.compile(r"^(vless|vmess|trojan|ss|hysteria2|hy2)://", re.IGNORECASE)
_GLUED_PROTOCOL_RE = re.compile(r"(?i)(?<!^)(?<![A-Za-z0-9])(vless|vmess|trojan|ss|hysteria2|hy2)://")
_BASE64_RE = re.compile(r"^[A-Za-z0-9+/_=-]+$")
_METADATA_PREFIXES = (
    "profile-title",
    "profile-update-interval",
    "support-url",
    "subscription-userinfo",
    "announce",
)
_VALID_VLESS_FLOWS = {"", "xtls-rprx-vision"}
_TCP_ALIASES = {"", "tcp", "raw", "none"}
_SUPPORTED_TRANSPORTS = {"ws", "grpc", "httpupgrade"}


@dataclass
class IngestionStats:
    raw_count: int = 0
    parsed_count: int = 0
    invalid_removed: int = 0
    duplicates_removed: int = 0
    final_saved_count: int = 0
    final_aggregate_outbound_count: int = 0
    limited_removed: int = 0

    def merge(self, other: "IngestionStats") -> None:
        self.raw_count += other.raw_count
        self.parsed_count += other.parsed_count
        self.invalid_removed += other.invalid_removed
        self.duplicates_removed += other.duplicates_removed
        self.final_saved_count += other.final_saved_count
        self.final_aggregate_outbound_count += other.final_aggregate_outbound_count
        self.limited_removed += other.limited_removed


def decode_subscription_content(content: str) -> str:
    """Decode whole-subscription base64 payloads when the response is encoded."""
    stripped = content.strip()
    if not stripped or "://" in stripped:
        return content
    compact = "".join(stripped.split())
    if len(compact) < 16 or not _BASE64_RE.match(compact):
        return content
    try:
        padding = "=" * (-len(compact) % 4)
        decoded = base64.urlsafe_b64decode((compact + padding).encode()).decode("utf-8", errors="ignore")
    except Exception:
        return content
    return decoded if "://" in decoded else content


def extract_candidate_proxy_links(content: str) -> List[str]:
    """Extract only top-level proxy lines; comments are never scanned for nested links."""
    decoded = decode_subscription_content(content)
    candidates = []
    for raw_line in decoded.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        lowered = line.lower().lstrip("#").strip()
        if any(lowered.startswith(prefix) for prefix in _METADATA_PREFIXES):
            continue
        for candidate in _GLUED_PROTOCOL_RE.sub(r"\n\1://", line).splitlines():
            candidate = candidate.strip()
            if _PROTOCOL_RE.match(candidate):
                candidates.append(candidate)
    return candidates


def ingest_subscription_content(
    content: str,
    seen_identity_keys: Optional[Set[str]] = None,
    limit: Optional[int] = None,
) -> Tuple[List[str], IngestionStats]:
    """Parse, normalize, deduplicate, and optionally limit one subscription response."""
    candidates = extract_candidate_proxy_links(content)
    return ingest_proxy_links(candidates, seen_identity_keys=seen_identity_keys, limit=limit)


def ingest_proxy_links(
    links: Iterable[str],
    seen_identity_keys: Optional[Set[str]] = None,
    limit: Optional[int] = None,
) -> Tuple[List[str], IngestionStats]:
    stats = IngestionStats()
    seen_exact: Set[str] = set()
    identity_keys = seen_identity_keys if seen_identity_keys is not None else set()
    saved: List[str] = []

    for raw in links:
        stats.raw_count += 1
        normalized = normalize_proxy_link(raw)
        if not normalized:
            stats.invalid_removed += 1
            continue
        stats.parsed_count += 1
        if normalized in seen_exact:
            stats.duplicates_removed += 1
            continue
        seen_exact.add(normalized)
        identity = proxy_identity_key(normalized)
        if not identity or identity in identity_keys:
            stats.duplicates_removed += 1
            continue
        if limit is not None and len(saved) >= limit:
            stats.limited_removed += 1
            continue
        identity_keys.add(identity)
        saved.append(normalized)

    stats.final_saved_count = len(saved)
    stats.final_aggregate_outbound_count = len(saved)
    return saved, stats


def normalize_proxy_link(link: str) -> Optional[str]:
    link = link.strip()
    if not _PROTOCOL_RE.match(link):
        return None
    protocol = link.split("://", 1)[0].lower()
    if protocol == "hy2":
        protocol = "hysteria2"
        link = "hysteria2://" + link.split("://", 1)[1]
    if protocol == "vmess":
        return _normalize_vmess(link)
    if protocol == "ss":
        return _normalize_ss(link)
    return _normalize_standard_url(link, protocol)


def _normalize_standard_url(link: str, protocol: str) -> Optional[str]:
    try:
        parsed = urlsplit(link)
        if not parsed.hostname or not parsed.port or parsed.port < 1 or parsed.port > 65535:
            return None
        username = parsed.username or ""
        if protocol in {"vless", "trojan"} and not username:
            return None
        params = _clean_params(dict(parse_qsl(parsed.query, keep_blank_values=False)))
        transport = params.get("type", "tcp").lower()
        if transport in _TCP_ALIASES:
            params.pop("type", None)
        elif transport in _SUPPORTED_TRANSPORTS:
            params["type"] = transport
        else:
            return None
        if protocol == "vless":
            flow = params.get("flow", "")
            if flow == "xtls-rprx-vision-udp443":
                params["flow"] = "xtls-rprx-vision"
            elif flow not in _VALID_VLESS_FLOWS:
                return None
            if params.get("security") == "reality" and not params.get("pbk"):
                return None
            params.setdefault("encryption", "none")
        query = urlencode(sorted(params.items()))
        netloc = parsed.netloc.split("@", 1)[-1]
        netloc = f"{username}@{netloc}" if username else netloc
        return urlunsplit((protocol, netloc, parsed.path.rstrip("/"), query, parsed.fragment))
    except Exception:
        return None


def _normalize_vmess(link: str) -> Optional[str]:
    try:
        payload = link.split("://", 1)[1].split("#", 1)[0].strip()
        decoded = _b64decode(payload)
        data = json.loads(decoded)
        if not data.get("add") or not data.get("port") or not data.get("id"):
            return None
        port = int(data["port"])
        if port < 1 or port > 65535:
            return None
        net = str(data.get("net") or "tcp").lower()
        if net in _TCP_ALIASES:
            net = "tcp"
        elif net not in _SUPPORTED_TRANSPORTS:
            return None
        normalized = {
            "v": str(data.get("v") or "2"),
            "ps": str(data.get("ps") or ""),
            "add": str(data["add"]).strip(),
            "port": str(port),
            "id": str(data["id"]).strip(),
            "aid": str(data.get("aid") or data.get("alterId") or "0"),
            "scy": str(data.get("scy") or data.get("security") or "auto"),
            "net": net,
            "type": str(data.get("type") or ""),
            "host": str(data.get("host") or ""),
            "path": str(data.get("path") or ""),
            "tls": str(data.get("tls") or ""),
            "sni": str(data.get("sni") or ""),
            "alpn": str(data.get("alpn") or ""),
            "fp": str(data.get("fp") or ""),
        }
        compact = json.dumps(_clean_params(normalized), separators=(",", ":"), ensure_ascii=False)
        return "vmess://" + base64.urlsafe_b64encode(compact.encode()).decode().rstrip("=")
    except Exception:
        return None


def _normalize_ss(link: str) -> Optional[str]:
    parsed = urlsplit(link)
    if parsed.hostname and parsed.port:
        return link
    return link if len(link) > len("ss://") + 8 else None


def proxy_identity_key(link: str) -> Optional[str]:
    protocol = link.split("://", 1)[0].lower()
    try:
        if protocol == "vmess":
            data = json.loads(_b64decode(link.split("://", 1)[1].split("#", 1)[0]))
            return "|".join([
                "vmess",
                str(data.get("add", "")).lower(),
                str(data.get("port", "")),
                str(data.get("id", "")),
                str(data.get("net", "tcp")).lower(),
                str(data.get("sni") or data.get("host") or "").lower(),
                str(data.get("path") or ""),
                "",
            ])
        parsed = urlsplit(link)
        params = dict(parse_qsl(parsed.query, keep_blank_values=False))
        return "|".join([
            protocol,
            (parsed.hostname or "").lower(),
            str(parsed.port or ""),
            parsed.username or "",
            params.get("type", "tcp").lower(),
            (params.get("sni") or params.get("host") or "").lower(),
            params.get("path") or params.get("serviceName") or "",
            params.get("pbk") or params.get("publicKey") or "",
        ])
    except Exception:
        return None


def _clean_params(params: Dict[str, object]) -> Dict[str, str]:
    cleaned = {}
    for key, value in params.items():
        if value is None:
            continue
        text = str(value).strip()
        if text == "" or text.lower() in {"null", "none"}:
            continue
        cleaned[str(key)] = text
    return cleaned


def _b64decode(payload: str) -> str:
    padding = "=" * (-len(payload) % 4)
    return base64.urlsafe_b64decode((payload + padding).encode()).decode("utf-8", errors="ignore")
