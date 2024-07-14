import re
from transformers import AutoTokenizer, AutoModel

# Load a German tokenizer (you may need to fine-tune or select an appropriate model)
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')

# Define a basic phoneme dictionary for German (you need a more comprehensive one)
german_phoneme_dict = {
    'hallo': ['h', 'a', 'l', 'o'],
    'wie': ['v', 'i:'],
    'geht': ['g', 'e:', 't'],
    'es': ['ɛ', 's'],
    'dir': ['d', 'i', 'r'],
    # Add more words and their phonemes
}

def normalize_abbreviations(text):
    abbreviations = {
        "z.B.": "zum Beispiel",
        "u.a.": "unter anderem",
        "etc.": "et cetera",
        "bzw.": "beziehungsweise",
        "d.h.": "das heißt",
        "Dr.": "Doktor",
        "Prof.": "Professor",
        # Add more abbreviations
    }
    for abbr, full in abbreviations.items():
        text = text.replace(abbr, full)
    return text

def normalize_numbers(text):
    def replace_number(match):
        num_dict = {
            '0': 'null', '1': 'eins', '2': 'zwei', '3': 'drei', '4': 'vier',
            '5': 'fünf', '6': 'sechs', '7': 'sieben', '8': 'acht', '9': 'neun',
            '10': 'zehn', '11': 'elf', '12': 'zwölf', '13': 'dreizehn', '14': 'vierzehn',
            '15': 'fünfzehn', '16': 'sechzehn', '17': 'siebzehn', '18': 'achtzehn', '19': 'neunzehn',
            '20': 'zwanzig', '30': 'dreißig', '40': 'vierzig', '50': 'fünfzig',
            '60': 'sechzig', '70': 'siebzig', '80': 'achtzig', '90': 'neunzig'
        }
        num = match.group()
        return num_dict.get(num, num)

    # Match numbers from 0 to 99 for simplicity, expand as needed
    text = re.sub(r'\b[0-9]{1,2}\b', replace_number, text)
    return text

def normalize_time(text):
    # Match times in formats like 12:30, 7:45 pm, etc.
    time_patterns = [
        (r'(\d{1,2}):(\d{2})', lambda m: f"{m.group(1)} Uhr {m.group(2)} Minuten"),
        (r'(\d{1,2})\s*([ap]m)', lambda m: f"{m.group(1)} {'vormittags' if m.group(2) == 'am' else 'nachmittags'}"),
    ]
    for pattern, repl in time_patterns:
        text = re.sub(pattern, repl, text)
    return text

def text_normalize(text):
    text = normalize_abbreviations(text)
    text = normalize_numbers(text)
    text = normalize_time(text)
    return text

def g2p(text):
    words = text.split()
    phonemes = []
    for word in words:
        if word.lower() in german_phoneme_dict:
            phonemes.extend(german_phoneme_dict[word.lower()])
        else:
            phonemes.extend(list(word))  # Fallback to letter spelling
    return phonemes

def get_bert_feature(text, word2ph, device=None):
    inputs = tokenizer(text, return_tensors='pt')
    outputs = model(**inputs)
    return outputs.last_hidden_state

if __name__ == "__main__":
    text = "Hallo, wie geht es dir um 12:30?"
    text = text_normalize(text)
    phonemes = g2p(text)
    print("Normalized Text:", text)
    print("Phonemes:", phonemes)