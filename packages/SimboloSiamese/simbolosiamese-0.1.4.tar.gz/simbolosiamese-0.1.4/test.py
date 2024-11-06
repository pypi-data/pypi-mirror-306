import re
from typing import Dict
import streamlit as st

# Dictionary mapping Burmese characters to their Romanized equivalents
burmese_to_roman = {
    'က': 'k', 'ခ': 'K', 'ဂ': 'g', 'ဃ': 'G', 'င': 'c', "၏": "E", "၍": "rx", "၌": "Nx", "င်္": "f",
    'စ': 's', 'ဆ': 'S', 'ဇ': 'z', 'ဈ': 'Z', "ဉ": "q", 'ည': 'Q', "ဋ": "tx", "ဌ": "Tx", "ဍ": "dx", "ဎ": "Dx", "ဏ": "nx",
    "ရ": "r", "ဓ": "D", "တ": "t", "ထ": "T", "ဒ": "d", "န": "n", "ပ": "p", "ဖ": "P", "ဗ": "b", "ဘ": "B", "မ": "m",
    "ယ": "y", "ဝ": "w", "သ": "j", "ဟ": "h", "အ": "a", 'လ': 'l', "ဠ": "lx", "ဣ": "ix", "ဤ": "Ix", "်":""
}
# Extend the dictionary with additional mappings for punctuation and diacritics
burmese_to_roman.update({
    "၊": "/", "။": "//", "ဥ": "Ux", "ဦ": "OO", "ဧ": "ax", "ဩ": "O", "ဪ": "OR", "ါ": "A", "ာ": "A", "ိ": "i", "ီ": "I","ေ": "e",
    "ု": "u", "ူ": "U", "ဲ": "L", "ံ": "N", "့": ".", "း": ":", "ျ": "Y", "ြ": "R", "ွ": "W", "ှ": "H","၎":"4",
    "ဿ": "jx"
})

# Function to handle the entire process: tokenization, normalization, and romanization
def burmese_to_romanize(text):
    # Clean and normalize the text
    
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r' ', ',', text)
    text = re.sub(r',+', ',', text)

    # Handle special word and tokenization in Burmese
    text = re.sub(r"([က-အ|ဥ|ဦ](င်္|[က-အ][ှ]*[့း]*[်]|([က-အ]္)|[ါ-ှႏꩻ][ꩻ]*){0,}|.)", r"\1 ", text)
    text = re.sub(r"(([က-အ])္ ([က-အ]))", r"\2် \3", text)

    # List of custom rules for converting specific word patterns to Romanized forms
    rules = [
        (re.compile(r'ကျွန် မ '), "q'm "),
        (re.compile(r'ကျွန် တော် '), "q't "),
        (re.compile(r'ကျွန်ုပ် '), 'Q" '),
        (re.compile(r'ဏ် ဍ'), "F"),
    ]
    for rule in rules:
        text = rule[0].sub(rule[1], text)
    text = re.sub(r'([‌ေ][က-ဪ]*[ာါ]*[်])', r'\1F', text)
    # Perform Romanization by replacing Burmese characters with Roman equivalents
    for burmese_char, roman_char in sorted(burmese_to_roman.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(burmese_char, roman_char)

    # Final clean-up of the text
    text = re.sub(r' ,', ",", text)

    return text

burmese_to_roman = {
    'က': 'k', 'ခ': 'K', 'ဂ': 'g', 'ဃ': 'G', 'င': 'c', "၏": "E", "၍": "rx", "၌": "Nx", "င်္": "f",
    'စ': 's', 'ဆ': 'S', 'ဇ': 'z', 'ဈ': 'Z', "ဉ": "q", 'ည': 'Q', "ဋ": "tx", "ဌ": "Tx", "ဍ": "dx", "ဎ": "Dx", "ဏ": "nx",
    "ရ": "r", "ဓ": "D", "တ": "t", "ထ": "T", "ဒ": "d", "န": "n", "ပ": "p", "ဖ": "P", "ဗ": "b", "ဘ": "B", "မ": "m",
    "ယ": "y", "ဝ": "w", "သ": "j", "ဟ": "h", "အ": "a", 'လ': 'l', "ဠ": "lx", "ဣ": "ix", "ဤ": "Ix", "်":"F"
}

burmese_to_roman.update({
    "၊": "/", "။": "//", "ဥ": "Ux", "ဦ": "OO", "ဧ": "ax", "ဩ": "O", "ဪ": "OR", "ါ": "A", "ာ": "A", "ိ": "i", "ီ": "I","ေ": "e",
    "ု": "u", "ူ": "U", "ဲ": "L", "ံ": "N", "့": ".", "း": ":", "ျ": "Y", "ြ": "R", "ွ": "W", "ှ": "H","၎":"4",
    "ဿ": "jx"
})

roman_to_burmese = {v: k for k, v in burmese_to_roman.items()}

def romanize_to_burmese(text):
    # Step 1: Define special word transformation rules
    reverse_rules = [
        (re.compile(r"q'm "), 'ကျွန် မ '),
        (re.compile(r"q't "), 'ကျွန် တော် '),
        (re.compile(r'Q" '), 'ကျွန်ပ် '),
    ]

    # Initialize the result
    output_text = ""

    # Process each word in the text
    for word in text.split(" "):
        # Apply special word transformations
        for rule in reverse_rules:
            word = rule[0].sub(rule[1], word)

        # Convert Romanized text to Burmese
        for burmese_char, roman_char in sorted(roman_to_burmese.items(), key=lambda x: len(x[0]), reverse=True):
            word = word.replace(burmese_char, roman_char)

        # Additional transformations for accurate Burmese script formation
        word = re.sub(r"([ခဂငဒဝပ]ေ*)ာ", r"\1ါ", word)  # Replace 'ော' with 'ါ' for specific syllables
        word = re.sub(r"([က-အ])(.*)([က-အ])", r"\1\2\3်", word)  # Add '်' for syllable formation

        # Append processed word to output
        output_text += word

    return output_text

tab1, tab2 = st.tabs(["Romanization to Burmese", "Burmese to Romanization"])

with tab1:
    text_input = st.text_input("Romanization to Burmese")
    st.write("Burmese output:", romanize_to_burmese(text_input))

with tab2:
    text_input = st.text_input("Burmese to Romanization")
    st.write("Romanization output:", burmese_to_romanize(text_input))