## Simple AI Chatbot

- Flask + Rule-based + NLP chatbot
- Local dev: Podman
- Public deploy: Render (Free)

### Run locally
podman run -it --rm -p 5000:5000 -v $(pwd):/app flask-chatbot
