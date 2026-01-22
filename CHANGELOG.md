# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-11

### Added

- Initial release
- Direct API routing for 20+ providers:
  - Google (Gemini, Veo, Imagen)
  - OpenAI (GPT, DALL-E, Sora)
  - Stability AI
  - BFL (Flux)
  - Ideogram
  - Recraft
  - Luma Labs
  - Runway
  - Kling AI
  - MiniMax
  - Pika
  - Tripo3D
  - Rodin
  - Topaz Labs
  - BytePlus
  - PixVerse
  - Vidu
  - Moonvalley
  - LTX Studio
  - Wan (Alibaba)
- Local asset vault - bypass ComfyUI's cloud storage
- API key management UI in ComfyUI settings
- Environment variable support for API keys
- JSON config file support
- Auto-detection of unmapped proxy endpoints
- Graceful fallback to ComfyUI proxy when keys not configured
- Frontend error interception with helpful key configuration prompts
