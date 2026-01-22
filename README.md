# ComfyUI API Liberation

**Use your own API keys. No ComfyUI account required.**

ComfyUI's built-in API nodes route through `api.comfy.org` which requires an account and uses a credit system. This extension bypasses that entirely - your API calls go directly to the vendors (Google, OpenAI, Stability, etc.) using your own API keys.

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
git clone https://github.com/oxysoft/comfy-api-liberation.git
```

Restart ComfyUI after installation.

## Supported Providers

| Provider | Get API Key |
|----------|-------------|
| Google (Gemini, Veo, Imagen) | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| OpenAI (GPT, DALL-E, Sora) | [OpenAI Platform](https://platform.openai.com/api-keys) |
| Stability AI | [Stability Platform](https://platform.stability.ai/account/keys) |
| BFL (Flux) | [BFL API](https://api.bfl.ml) |
| Ideogram | [Ideogram API](https://ideogram.ai/manage-api) |
| Recraft | [Recraft Docs](https://www.recraft.ai/docs/api-reference/getting-started) |
| Luma Labs | [Luma API Keys](https://lumalabs.ai/dream-machine/api/keys) |
| Runway | [Runway Dev](https://dev.runwayml.com) |
| Kling AI | [Kling API](https://app.klingai.com/global/dev/api-key) |
| MiniMax | [MiniMax Platform](https://platform.minimax.io) |
| Pika | [Pika API](https://pika.art/api) |
| Tripo3D | [Tripo Platform](https://platform.tripo3d.ai) |
| Rodin (Hyper Human) | [Rodin Dashboard](https://hyperhuman.deemos.com/api-dashboard) |
| Topaz Labs | [Topaz API](https://www.topazlabs.com/api) |
| BytePlus | [BytePlus Console](https://console.byteplus.com) |
| PixVerse | [PixVerse Platform](https://platform.pixverse.ai) |
| Vidu | [Vidu Platform](https://platform.vidu.com) |
| Moonvalley | [Moonvalley](https://www.moonvalley.com) |
| LTX Studio | [LTX API](https://ltx.io/model/api) |
| Wan (Alibaba) | [Alibaba Model Studio](https://www.alibabacloud.com/help/en/model-studio/get-api-key) |

## Configuration

### Option 1: UI (Recommended)

1. In ComfyUI, go to **Settings** (gear icon)
2. Find **API Liberation** section
3. Enter your API keys for each provider
4. Keys are saved locally to `api_keys.json`

### Option 2: Environment Variables

Set environment variables before starting ComfyUI:

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

## How It Works

ComfyUI's API nodes make requests to `/proxy/*` endpoints on `api.comfy.org`. This extension:

1. **Intercepts** outgoing API requests before they leave ComfyUI
2. **Rewrites** `/proxy/vendor/...` URLs to direct vendor API URLs
3. **Injects** your API key as the appropriate auth header
4. **Virtualizes** the file upload system so assets stay local

All of this happens transparently - existing workflows work without modification.

## Debugging

Enable debug logging:

```bash
LIBERATION_DEBUG=1 python main.py
```

## Security Notes

- API keys are stored locally in `api_keys.json` (gitignored by default)
- Keys are never sent to ComfyUI/Comfy.org servers
- Each provider only receives its own API key

## License

MIT License - see [LICENSE](LICENSE) file.

## Contributing

Issues and PRs welcome. Please ensure `api_keys.json` is never committed.
