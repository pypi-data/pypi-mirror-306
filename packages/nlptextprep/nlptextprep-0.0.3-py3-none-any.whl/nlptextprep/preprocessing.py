from .utils import (
    to_lowercase,
    remove_line_breaks,
    remove_punctuation,
    remove_stop_words,
    stem_text,
    remove_special_characters,
    remove_encoded_data,
    remove_tags
)

def preprocess_text(text):
    text = remove_tags(text)
    text = remove_line_breaks(text)
    text = remove_encoded_data(text)
    text = remove_punctuation(text)
    text = to_lowercase(text)
    text = remove_stop_words(text)
    text = remove_special_characters(text)
    text = stem_text(text)
    return text