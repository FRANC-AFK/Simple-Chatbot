FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -m nltk.downloader punkt stopwords wordnet -d /usr/local/share/nltk_data

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
