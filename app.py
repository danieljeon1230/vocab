from flask import Flask, render_template, jsonify, request
import requests
import random
import json
from datetime import datetime, timedelta
import os
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

session = requests.Session()
session.timeout = (3, 3)

def get_sophisticated_words(count=5):
    try:
        sophisticated_words = []
        
        params = {
            'ml': 'intellectual,academic,philosophical,erudite',
            'max': 100,
            'md': 'f'
        }
        
        response = session.get('https://api.datamuse.com/words', params=params, timeout=3)
        if response.status_code == 200:
            words = response.json()
            if words:
                sophisticated_words.extend([
                    word['word'] for word in words 
                    if len(word['word']) >= 10 and
                    word.get('tags', []) and
                    'uncommon' in word.get('tags', [])
                ])
        
        params = {
            'rel_jja': 'complex,sophisticated,erudite',
            'max': 100
        }
        
        response = session.get('https://api.datamuse.com/words', params=params, timeout=3)
        if response.status_code == 200:
            words = response.json()
            if words:
                sophisticated_words.extend([
                    word['word'] for word in words 
                    if len(word['word']) >= 10 and
                    word.get('tags', []) and
                    'uncommon' in word.get('tags', [])
                ])
        
        known_sophisticated = [
            "perspicacious", "ubiquitous", "ephemeral", "sanguine", "obfuscate",
            "pernicious", "ameliorate", "vicissitude", "ineffable", "serendipity",
            "quintessential", "magnanimous", "judicious", "mellifluous", "pristine",
            "superfluous", "tenacious", "voracious", "whimsical", "zealous",
            "acquiesce", "belligerent", "capricious", "deferential", "ebullient",
            "fastidious", "gregarious", "halcyon", "insidious", "juxtapose",
            "laconic", "meticulous", "nefarious", "ostentatious", "pragmatic",
            "quixotic", "recalcitrant", "sagacious", "truculent", "unprecedented",
            "vivacious", "wistful", "xenophobic", "yearning", "abstruse",
            "byzantine", "conundrum", "dilettante", "equivocal", "facetious",
            "grandiloquent", "hackneyed", "iconoclast", "jejune", "kickshaw",
            "loquacious", "munificent", "nascent", "obloquy", "parsimonious",
            "quandary", "rancorous", "surreptitious", "trepidation", "ubiquitous",
            "vexatious", "winsome", "xerophytic", "yoke", "zephyr"
        ]
        
        for word in random.sample(known_sophisticated, 3):
            params = {
                'ml': word,
                'max': 50
            }
            response = session.get('https://api.datamuse.com/words', params=params, timeout=3)
            if response.status_code == 200:
                words = response.json()
                if words:
                    sophisticated_words.extend([
                        word['word'] for word in words 
                        if len(word['word']) >= 10 and
                        word.get('tags', []) and
                        'uncommon' in word.get('tags', [])
                    ])
        
        if len(sophisticated_words) < count:
            sophisticated_words.extend(known_sophisticated)
        
        sophisticated_words = list(set(sophisticated_words))
        return random.sample(sophisticated_words, min(count, len(sophisticated_words)))
            
    except Exception as e:
        print(f"Error fetching words: {e}")
    
    return random.sample(known_sophisticated, count)

def get_word_definition(word):
    try:
        response = session.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}", timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                entry = data[0]
                
                pronunciation = ""
                if 'phonetics' in entry and entry['phonetics']:
                    for phonetic in entry['phonetics']:
                        if 'text' in phonetic and phonetic['text']:
                            pronunciation = phonetic['text']
                            break
                
                definitions = []
                if 'meanings' in entry:
                    for meaning in entry['meanings']:
                        part_of_speech = meaning.get('partOfSpeech', '')
                        for definition in meaning.get('definitions', []):
                            def_text = definition.get('definition', '')
                            example = definition.get('example', '')
                            definitions.append({
                                'partOfSpeech': part_of_speech,
                                'definition': def_text,
                                'example': example
                            })
                
                return {
                    'word': word,
                    'pronunciation': pronunciation,
                    'definitions': definitions
                }
    except Exception as e:
        print(f"Error fetching definition for {word}: {e}")
    
    return None

def get_definitions_parallel(words):
    with ThreadPoolExecutor(max_workers=5) as executor:
        definitions = list(executor.map(get_word_definition, words))
    return definitions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/daily-words')
def get_daily_words():
    word_count = int(request.args.get('count', 1))
    word_count = min(max(word_count, 1), 5)
    
    today = datetime.now().strftime('%Y-%m-%d')
    seed = hash(today)
    random.seed(seed)
    
    selected_words = get_sophisticated_words(word_count)
    words_with_definitions = get_definitions_parallel(selected_words)
    
    words_with_definitions = [
        definition if definition else {
            'word': word,
            'pronunciation': '',
            'definitions': [{
                'partOfSpeech': 'unknown',
                'definition': 'Definition not available',
                'example': ''
            }]
        }
        for word, definition in zip(selected_words, words_with_definitions)
    ]
    
    return jsonify({
        'date': today,
        'words': words_with_definitions
    })

@app.route('/api/random-words')
def get_random_words():
    word_count = int(request.args.get('count', 1))
    word_count = min(max(word_count, 1), 5)
    
    selected_words = get_sophisticated_words(word_count)
    words_with_definitions = get_definitions_parallel(selected_words)
    
    words_with_definitions = [
        definition if definition else {
            'word': word,
            'pronunciation': '',
            'definitions': [{
                'partOfSpeech': 'unknown',
                'definition': 'Definition not available',
                'example': ''
            }]
        }
        for word, definition in zip(selected_words, words_with_definitions)
    ]
    
    return jsonify({
        'words': words_with_definitions
    })

if __name__ == '__main__':
    app.run(debug=True)