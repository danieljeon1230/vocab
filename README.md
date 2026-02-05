# Sophisticated Vocabulary Learner

## Features
- Curated and random word modes
- Definitions, part of speech, pronunciation, example sentences
- Select word count (1–5)
- Responsive design

## Setup and Installation
```bash
git clone https://github.com/danieljeon1230/vocab.git
cd vocab
pip install flask requests
```

## Usage
```bash
python app.py
```
Then open your browser to `http://127.0.0.1:5000`

## Additional Information
- APIs: Datamuse and Free Dictionary (no keys required)
- REST Endpoints:
  - `/api/daily-words?count=<number>`
  - `/api/random-words?count=<number>`
