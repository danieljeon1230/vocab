# Sophisticated Vocabulary Learner

A web application that helps users learn sophisticated and complex vocabulary words. The application provides daily and random word suggestions along with their definitions, pronunciations, and example sentences.

## Features

- **Daily Words**: Get a curated set of sophisticated words for each day
- **Random Words**: Get random sophisticated words on demand
- **Word Details**: Each word comes with:
  - Pronunciation
  - Multiple definitions
  - Part of speech
  - Example sentences
- **Customizable**: Choose how many words you want to learn (1-5)
- **Sophisticated Selection**: Words are carefully selected to be:
  - Complex and challenging
  - At least 10 characters long
  - Uncommon in everyday usage
  - Rich in meaning and usage

## Technical Details

- Built with Flask (Python web framework)
- Uses Datamuse API for word selection
- Uses Free Dictionary API for definitions
- Responsive design for all devices
- No API keys required

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vocabulary-learner
```

2. Install the required packages:
```bash
pip install flask requests
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## Usage

1. On the main page, you'll see:
   - A number input to select how many words you want (1-5)
   - "Get Today's Words" button for daily vocabulary
   - "Get Random Words" button for random vocabulary

2. Click either button to get your words:
   - Daily words are consistent for each day
   - Random words are different each time

3. Each word card shows:
   - The word itself
   - Its pronunciation
   - Definitions with parts of speech
   - Example sentences (when available)

## API Endpoints

- `GET /api/daily-words?count=<number>`: Get daily words
- `GET /api/random-words?count=<number>`: Get random words

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License. 