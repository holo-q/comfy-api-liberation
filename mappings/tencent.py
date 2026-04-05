"""Tencent Hunyuan 3D endpoint mappings with TC3 request signing."""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse


TC3_ALGORITHM = "TC3-HMAC-SHA256"
TENCENT_SERVICE = "hunyuan"
TENCENT_VERSION = "2023-09-01"
TENCENT_HOST = "hunyuan.intl.tencentcloudapi.com"
DEFAULT_REGION = "na-ashburn"


@dataclass(frozen=True)
class TencentCredentials:
    secret_id: str
    secret_key: str
    region: str = DEFAULT_REGION


def _sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _hmac_sha256(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _parse_credentials(raw: str) -> TencentCredentials:
    raw = raw.strip()
    if not raw:
        raise ValueError("Tencent credentials are empty")

    if raw.startswith("{"):
        payload = json.loads(raw)
        secret_id = payload.get("secret_id") or payload.get("SecretId")
        secret_key = payload.get("secret_key") or payload.get("SecretKey")
        region = payload.get("region") or payload.get("Region") or DEFAULT_REGION
    else:
        parts = raw.split(":")
        if len(parts) < 2:
            raise ValueError(
                "Tencent credentials must be 'secretId:secretKey[:region]' or JSON "
                "like {'secret_id': ..., 'secret_key': ..., 'region': ...}"
            )
        secret_id = parts[0].strip()
        secret_key = parts[1].strip()
        region = parts[2].strip() if len(parts) > 2 and parts[2].strip() else DEFAULT_REGION

    if not secret_id or not secret_key:
        raise ValueError("Tencent credentials must include both secret_id and secret_key")

    return TencentCredentials(secret_id=secret_id, secret_key=secret_key, region=region)


def _serialize_payload(data: Any) -> str:
    if data is None:
        return "{}"
    return json.dumps(data, ensure_ascii=True, separators=(",", ":"))


def _sign_request(
    *,
    credentials: TencentCredentials,
    action: str,
    body: str,
    timestamp: int,
    host: str,
) -> dict[str, str]:
    date = time.strftime("%Y-%m-%d", time.gmtime(timestamp))
    canonical_headers = (
        "content-type:application/json; charset=utf-8\n"
        f"host:{host}\n"
        f"x-tc-action:{action.lower()}\n"
    )
    signed_headers = "content-type;host;x-tc-action"
    canonical_request = "\n".join(
        [
            "POST",
            "/",
            "",
            canonical_headers,
            signed_headers,
            _sha256_hex(body),
        ]
    )
    credential_scope = f"{date}/{TENCENT_SERVICE}/tc3_request"
    string_to_sign = "\n".join(
        [
            TC3_ALGORITHM,
            str(timestamp),
            credential_scope,
            _sha256_hex(canonical_request),
        ]
    )
    secret_date = _hmac_sha256(f"TC3{credentials.secret_key}".encode("utf-8"), date)
    secret_service = hmac.new(secret_date, TENCENT_SERVICE.encode("utf-8"), hashlib.sha256).digest()
    secret_signing = hmac.new(secret_service, b"tc3_request", hashlib.sha256).digest()
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    authorization = (
        f"{TC3_ALGORITHM} "
        f"Credential={credentials.secret_id}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, "
        f"Signature={signature}"
    )
    return {
        "Authorization": authorization,
        "Content-Type": "application/json; charset=utf-8",
        "Host": host,
        "X-TC-Action": action,
        "X-TC-Version": TENCENT_VERSION,
        "X-TC-Region": credentials.region,
        "X-TC-Timestamp": str(timestamp),
    }


def _prepare_tencent_request(
    *,
    key: str,
    url: str,
    method: str,
    data: Any,
    headers: dict[str, str],
    groups: tuple[str, ...],
    mapping: dict[str, Any],
) -> dict[str, Any]:
    _ = headers, groups
    if method.upper() != "POST":
        raise ValueError("Tencent Hunyuan APIs are expected to use POST")

    credentials = _parse_credentials(key)
    parsed = urlparse(url)
    host = parsed.netloc or TENCENT_HOST
    body = _serialize_payload(data)
    timestamp = int(time.time())
    signed_headers = _sign_request(
        credentials=credentials,
        action=mapping["tencent_action"],
        body=body,
        timestamp=timestamp,
        host=host,
    )
    return {
        "url": f"{parsed.scheme}://{host}/",
        "headers": signed_headers,
        "data": json.loads(body),
    }


def _mapping(action: str) -> dict[str, Any]:
    return {
        "provider": "tencent",
        "url_template": f"https://{TENCENT_HOST}/",
        "auth_fn": lambda _key: {},
        "prepare_request": _prepare_tencent_request,
        "request_transform": None,
        "response_transform": None,
        "tencent_action": action,
    }


MAPPINGS = {
    r"^/proxy/tencent/hunyuan/3d-pro$": _mapping("SubmitHunyuanTo3DProJob"),
    r"^/proxy/tencent/hunyuan/3d-pro/query$": _mapping("QueryHunyuanTo3DProJob"),
    r"^/proxy/tencent/hunyuan/3d-uv$": _mapping("SubmitHunyuanTo3DUVJob"),
    r"^/proxy/tencent/hunyuan/3d-uv/query$": _mapping("DescribeHunyuanTo3DUVJob"),
    r"^/proxy/tencent/hunyuan/3d-texture-edit$": _mapping("SubmitHunyuanTo3DTextureEditJob"),
    r"^/proxy/tencent/hunyuan/3d-texture-edit/query$": _mapping("QueryHunyuanTo3DTextureEditJob"),
    r"^/proxy/tencent/hunyuan/3d-part$": _mapping("SubmitHunyuan3DPartJob"),
    r"^/proxy/tencent/hunyuan/3d-part/query$": _mapping("QueryHunyuan3DPartJob"),
    r"^/proxy/tencent/hunyuan/3d-smart-topology$": _mapping("Submit3DSmartTopologyJob"),
    r"^/proxy/tencent/hunyuan/3d-smart-topology/query$": _mapping("Describe3DSmartTopologyJob"),
}
