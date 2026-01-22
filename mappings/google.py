"""Google (Gemini, Veo) endpoint mappings."""
import base64
import logging

from ..asset_vault import vault

log = logging.getLogger("comfy-api-liberation")


def _strip_upload_images_flag(payload):
    """Remove uploadImagesToStorage key Google doesn't accept."""
    if isinstance(payload, dict) and "uploadImagesToStorage" in payload:
        return {k: v for k, v in payload.items() if k != "uploadImagesToStorage"}
    return payload


def _materialize_gemini_filedatas(payload):
    """
    Convert `fileData.fileUri` placeholders into `inlineData` for direct Google calls.

    Comfy's proxy can accept arbitrary file URLs (and may upload them to Google). When routing
    directly to Google, the request must include bytes inline (base64) unless the URI points to
    a Google-hosted location (e.g., `gs://...`). The liberation asset vault returns
    `liberation://asset/<id>` URIs which we must materialize here.
    """
    if not isinstance(payload, dict):
        return payload

    contents = payload.get("contents")
    if not isinstance(contents, list):
        return payload

    for content in contents:
        if not isinstance(content, dict):
            continue
        parts = content.get("parts")
        if not isinstance(parts, list):
            continue
        for part in parts:
            if not isinstance(part, dict):
                continue
            file_data = part.get("fileData")
            if not isinstance(file_data, dict):
                continue

            file_uri = file_data.get("fileUri")
            if not isinstance(file_uri, str):
                continue

            asset_id = vault.parse_asset_uri(file_uri)
            if not asset_id:
                continue

            data, stored_content_type, _filename = vault.get_bytes(asset_id)
            mime = file_data.get("mimeType") or stored_content_type or "application/octet-stream"

            part.pop("fileData", None)
            part["inlineData"] = {
                "mimeType": mime,
                "data": base64.b64encode(data).decode("utf-8"),
            }

    return payload


def _google_request_transform(payload):
    payload = _strip_upload_images_flag(payload)
    payload = _materialize_gemini_filedatas(payload)
    return payload


def _fix_response_for_comfy(response_data):
    """
    Fix response from Google's direct API to work with ComfyUI:
    1. Fix MIME types - Google returns image/jpeg but ComfyUI expects image/png
    2. Ensure usageMetadata has required fields to prevent price extractor errors
    3. Ensure content.role exists to prevent Pydantic validation errors
    """
    if not isinstance(response_data, dict):
        return response_data

    try:
        candidates = response_data.get("candidates", [])
        if candidates:
            for candidate in candidates:
                content = candidate.get("content")

                # Handle empty/missing content (rate limit, content filter, etc.)
                if content is None or content == {}:
                    # Provide minimal valid structure
                    candidate["content"] = {
                        "role": "model",
                        "parts": []
                    }
                    content = candidate["content"]

                # Ensure role field exists (required by Pydantic)
                if "role" not in content:
                    content["role"] = "model"

                # Fix MIME types in image parts
                parts = content.get("parts", [])
                for part in parts:
                    if "inlineData" in part:
                        mime = part["inlineData"].get("mimeType", "")
                        if mime.startswith("image/") and mime != "image/png":
                            part["inlineData"]["mimeType"] = "image/png"
                    elif "fileData" in part:
                        mime = part["fileData"].get("mimeType", "")
                        if mime.startswith("image/") and mime != "image/png":
                            part["fileData"]["mimeType"] = "image/png"

        # Ensure usageMetadata exists with required fields to prevent price extractor crash
        if "usageMetadata" not in response_data:
            response_data["usageMetadata"] = {}
        usage = response_data["usageMetadata"]
        if usage.get("promptTokenCount") is None:
            usage["promptTokenCount"] = 0
        if usage.get("candidatesTokenCount") is None:
            usage["candidatesTokenCount"] = 0

    except Exception as e:
        log.debug(f"[liberation] response transform error: {e}")

    return response_data


MAPPINGS = {
    # Gemini text/multimodal
    r'^/proxy/vertexai/gemini/(.+)$': {
        'provider': 'google',
        'url_template': 'https://generativelanguage.googleapis.com/v1beta/models/{0}:generateContent',
        'auth_fn': lambda key: {'x-goog-api-key': key},
        'request_transform': _google_request_transform,
        'response_transform': _fix_response_for_comfy,
    },
    # Veo video generation
    r'^/proxy/veo/([^/]+)/generate$': {
        'provider': 'google',
        'url_template': 'https://generativelanguage.googleapis.com/v1beta/models/{0}:generateContent',
        'auth_fn': lambda key: {'x-goog-api-key': key},
        'request_transform': _google_request_transform,
        'response_transform': None,
    },
    r'^/proxy/veo/([^/]+)/poll$': {
        'provider': 'google',
        'url_template': 'https://generativelanguage.googleapis.com/v1beta/models/{0}:generateContent',
        'auth_fn': lambda key: {'x-goog-api-key': key},
        'request_transform': _google_request_transform,
        'response_transform': None,
    },
}
