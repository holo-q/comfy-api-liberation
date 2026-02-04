<div align="center">

# ComfyUI API Liberation

**Use your own API keys. No ComfyUI account required.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ComfyUI](https://img.shields.io/badge/ComfyUI-Custom_Node-blue)](https://github.com/comfyanonymous/ComfyUI)

---

ComfyUI's built-in API nodes route through `api.comfy.org` which requires an account and uses a credit system.
This extension bypasses that entirely - your API calls go directly to the vendors using your own API keys.

</div>

## Features

- **Direct API routing** - Calls go straight to vendor APIs, not through ComfyUI's proxy
- **No account needed** - Works without a ComfyUI/Comfy.org account
- **Local asset storage** - Images/videos stored locally instead of uploaded to Comfy servers
- **20+ providers supported** - All major AI APIs covered
- **Simple UI** - Configure keys through ComfyUI's interface
- **Graceful fallback** - If no key is set, falls back to default ComfyUI behavior

## Installation

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/holo-q/comfy-api-liberation.git
```

Restart ComfyUI after installation.

## Configuration

### Option 1: UI (Recommended)

<div align="center">

**1.** Click **API Keys** in the toolbar

<img src="docs/1.png" width="600" alt="API Keys toolbar button"/>

**2.** Enter keys for each provider

<img src="docs/2.png" width="500" alt="API Key Manager"/>

</div>

> **Get Key** links directly to each provider's API key page
> **Status** shows "Configured" (green) or "Not set"
> Keys are saved locally to `api_keys.json`

### Option 2: Environment Variables

```bash
export GOOGLE_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"
export STABILITY_API_KEY="your-key-here"
# ... etc
```

### Option 3: Config File

Create `api_keys.json` in the extension directory:

```json
{
  "google": "your-google-key",
  "openai": "your-openai-key",
  "stability": "your-stability-key"
}
```

**Priority:** Environment variables > Config file > UI settings

## Supported Providers

<table>
<tr>
<td width="33%" valign="top">

| Provider | |
|:---------|:-:|
| Google (Gemini, Veo, Imagen) | [Get Key](https://aistudio.google.com/app/apikey) |
| OpenAI (GPT, DALL-E, Sora) | [Get Key](https://platform.openai.com/api-keys) |
| Stability AI | [Get Key](https://platform.stability.ai/account/keys) |
| BFL (Flux) | [Get Key](https://api.bfl.ml) |
| Ideogram | [Get Key](https://ideogram.ai/manage-api) |
| Recraft | [Get Key](https://www.recraft.ai/docs) |
| Luma Labs | [Get Key](https://lumalabs.ai/dream-machine/api/keys) |

</td>
<td width="33%" valign="top">

| Provider | |
|:---------|:-:|
| Runway | [Get Key](https://dev.runwayml.com) |
| Kling AI | [Get Key](https://app.klingai.com/global/dev/api-key) |
| MiniMax | [Get Key](https://platform.minimax.io) |
| Pika | [Get Key](https://pika.art/api) |
| Tripo3D | [Get Key](https://platform.tripo3d.ai) |
| Rodin (Hyper Human) | [Get Key](https://hyperhuman.deemos.com/api-dashboard) |
| Topaz Labs | [Get Key](https://www.topazlabs.com/api) |

</td>
<td width="33%" valign="top">

| Provider | |
|:---------|:-:|
| BytePlus | [Get Key](https://console.byteplus.com) |
| PixVerse | [Get Key](https://platform.pixverse.ai) |
| Vidu | [Get Key](https://platform.vidu.com) |
| Moonvalley | [Get Key](https://www.moonvalley.com) |
| LTX Studio | [Get Key](https://ltx.io/model/api) |
| Wan (Alibaba) | [Get Key](https://www.alibabacloud.com/help/en/model-studio/get-api-key) |

</td>
</tr>
</table>

## How It Works

ComfyUI's API nodes make requests to `/proxy/*` endpoints on `api.comfy.org`. This extension:

1. **Intercepts** outgoing API requests before they leave ComfyUI
2. **Rewrites** `/proxy/vendor/...` URLs to direct vendor API URLs
3. **Injects** your API key as the appropriate auth header
4. **Virtualizes** the file upload system so assets stay local

All of this happens transparently - existing workflows work without modification.

## Debugging

```bash
LIBERATION_DEBUG=1 python main.py
```

## Security

- API keys are stored locally in `api_keys.json` (gitignored)
- Keys are never sent to ComfyUI/Comfy.org servers
- Each provider only receives its own API key

---

<div align="center">

**MIT License** · Issues and PRs welcome

</div>
