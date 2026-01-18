# Simple AI Chatbot

A Flask-based chatbot with rule-based responses enhanced by AI using HuggingFace models. Features include intelligent caching, rate limiting, and comprehensive logging.

## ✨ Features

- 🤖 **AI-Enhanced Responses** - Uses HuggingFace Llama 3.2 model for natural language generation
- 📝 **Rule-Based Fallbacks** - Reliable responses when AI is unavailable
- ⚡ **Response Caching** - Reduces API calls and improves response time
- 🔒 **Rate Limiting** - Protection against abuse (configurable)
- 📊 **Comprehensive Logging** - Track all requests and responses
- 🐳 **Container Ready** - Docker/Podman compatible with security best practices
- ♿ **Accessible UI** - ARIA labels and keyboard navigation
- 🔄 **Auto-Retry Logic** - Handles network failures gracefully
- ☁️ **Cloud Deploy Ready** - Works with Render, Heroku, and other platforms

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone <your-repo-url>
cd simple-ai-chatbot

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export HF_API_TOKEN="your_huggingface_token_here"

# Run application
python app.py
```

Visit [http://localhost:5000](http://localhost:5000)

### Docker/Podman

```bash
# Build image
podman build -t flask-chatbot .

# Run container
podman run -it --rm -p 5000:5000 \
  -e HF_API_TOKEN="your_token" \
  flask-chatbot
```

### Deploy to Render

1. Push your code to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your repository
4. Add environment variable: `HF_API_TOKEN`
5. Deploy! 🎉

## ⚙️ Configuration

All configuration is managed via environment variables. See [config.py](config.py) for all available options:

### Core Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `HF_API_TOKEN` | - | **Required** - Your HuggingFace API token |
| `USE_AI` | `True` | Enable/disable AI-enhanced responses |
| `DEBUG` | `False` | Flask debug mode |
| `PORT` | `5000` | Server port |

### Cache Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `ENABLE_CACHE` | `True` | Enable response caching |
| `CACHE_MAX_SIZE` | `100` | Maximum cached responses |
| `CACHE_TTL` | `3600` | Cache time-to-live (seconds) |

### Rate Limiting

| Variable | Default | Description |
|----------|---------|-------------|
| `RATE_LIMIT_MAX_REQUESTS` | `10` | Max requests per window |
| `RATE_LIMIT_WINDOW_SECONDS` | `60` | Rate limit window (seconds) |

### AI Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `AI_MAX_TOKENS` | `64` | Maximum tokens per response |
| `AI_TIMEOUT` | `60` | API timeout (seconds) |

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=chatbot

# Run specific test file
pytest tests/test_engine.py -v
```

## 📁 Project Structure

```
simple-ai-chatbot/
├── app.py                 # Flask application & routes
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Containerfile          # Container build instructions
├── Procfile              # Render/Heroku deployment
├── chatbot/
│   ├── engine.py         # Core response logic
│   ├── rules.py          # Rule definitions
│   ├── nlp.py            # Text normalization
│   ├── cache.py          # Response caching
│   ├── rate_limiter.py   # Rate limiting
│   ├── logger.py         # Logging configuration
│   └── ai/
│       ├── generator.py  # AI response generation
│       ├── hf_client.py  # HuggingFace API client
│       └── prompts.py    # AI prompts
├── static/
│   ├── css/style.css     # UI styles
│   └── js/chat.js        # Frontend logic
├── templates/
│   └── index.html        # Chat interface
└── tests/
    ├── test_engine.py    # Engine tests
    ├── test_cache.py     # Cache tests
    └── test_rate_limiter.py  # Rate limiter tests
```

## 🛠️ API Endpoints

### `GET /`
Main chat interface

### `POST /chat`
Send a message and receive a response

**Request:**
```json
{
  "message": "What are your hours?"
}
```

**Response:**
```json
{
  "reply": "We're open from 9 AM to 5 PM, Monday through Friday.",
  "type": "ai"
}
```

Response types: `ai`, `rule`, `cached`, `fallback`

### `GET /health`
Health check endpoint for monitoring

**Response:**
```json
{
  "status": "healthy",
  "ai_enabled": true,
  "cache_enabled": true,
  "hf_configured": true
}
```

### `GET /debug/hf`
Test HuggingFace API connectivity

## 📝 Development

### Adding New Rules

Edit [chatbot/rules.py](chatbot/rules.py):

```python
RULES = {
    "my_rule": {
        "keywords": {"keyword1", "keyword2"},
        "response": "Your response here"
    }
}
```

### Customizing AI Prompts

Edit [chatbot/ai/prompts.py](chatbot/ai/prompts.py) to customize how AI enhances responses.

## 🐛 Troubleshooting

### AI responses not working
1. Verify `HF_API_TOKEN` is set: `echo $HF_API_TOKEN`
2. Test API: `curl http://localhost:5000/debug/hf`
3. Check logs for error messages

### Rate limit errors
- Increase `RATE_LIMIT_MAX_REQUESTS` environment variable
- Or increase `RATE_LIMIT_WINDOW_SECONDS`

### Container won't start
- Ensure port 5000 is available
- Check container logs: `podman logs <container-id>`

## 📄 License

MIT License - Feel free to use this project for learning or production!

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 🔗 Resources

- [HuggingFace Serverless Inference](https://huggingface.co/inference-api)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Render Deployment Guide](https://render.com/docs)
