import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
import unicodedata

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

__author__ = "Tashu"
__copyright__ = "Tashu"
__license__ = "MIT"

def to_lowercase(input_str: str) -> str:
    """
    Convert the entire input string to lowercase.

    Parameters:
    input_str (str): The string to be lowercased.

    Returns:
    str: The input string converted to lowercase.
    """
    if not isinstance(input_str, str):
        raise ValueError("Input must be a string.")
    
    return input_str.lower()

def remove_line_breaks(input_string: str) -> str:
    """
    Remove all line breaks from the input string.
    
    This function replaces all newline characters ('\n', '\r', and '\r\n') with a space.
    
    Args:
        input_string (str): The string from which to remove line breaks.
    
    Returns:
        str: The processed string with line breaks removed.
    """
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string")
    
    # Replace any of '\n', '\r', or '\r\n' with a single space
    cleaned_string = ' '.join(input_string.splitlines())

    cleaned_string = re.sub(r'\s+', ' ', cleaned_string).strip()

    return cleaned_string

def remove_punctuation(input_string: str) -> str:
    """
    Remove all punctuation characters from the input string except dots between numbers,
    currency symbols, email addresses, and URLs with http or https protocols.
    
    This function removes any character classified as punctuation (e.g., !, ?, etc.)
    from the input string, but preserves dots when they are part of numeric values,
    currency symbols (e.g., $, €, £), and URLs starting with http or https.
    
    Args:
        input_string (str): The string from which to remove punctuation.
    
    Returns:
        str: The processed string with punctuation removed, except for dots between numbers,
        currency symbols, email addresses, and http/https URLs.
    """
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string")

    # Pattern to identify URLs starting with http or https
    url_pattern = r'(?:https?://[a-zA-Z0-9\-._~:/?#[\]@!$&\'()*+,;=%]+)'
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    # Split the string based on URLs
    segments = re.split(f'({url_pattern}|{email_pattern})', input_string)

    # Process each segment individually
    cleaned_segments = []
    for segment in segments:
        segment = segment.strip()
        # Skip punctuation removal for URL segments
        if re.match(url_pattern, segment) or re.match(email_pattern, segment):
            cleaned_segments.append(segment)
            continue

        # Remove parentheses if they enclose English text
        def remove_text_in_parentheses(segment):
            return re.sub(r'\(([a-zA-Z\s]+)\)', r'\1', segment)

        # Apply the function to remove text enclosed in parentheses
        segment = remove_text_in_parentheses(segment)

        # Function to decide if punctuation should be removed
        def replace_punctuation(match):
            char = match.group(0)
            start = match.start()
            end = match.end()

            # Generalized condition: Preserve punctuation if it's between, before, or after digits, or within mathematical expressions
            if char in './-+%()':
                # Preserve if surrounded by digits or spaces followed by digits
                if ((start > 0 and segment[start - 1].isdigit()) or (end < len(segment) and segment[end].isdigit())) or \
                   ((start > 0 and segment[start - 1].isdigit()) and (end < len(segment) and segment[end].isspace())) or \
                   ((start > 0 and segment[start - 1].isspace()) and (end < len(segment) and segment[end].isdigit())) or \
                   (start > 0 and char in '()-'):
                    return char
                return ''
            if unicodedata.category(char) == 'Sc':  # 'Sc' is the Unicode category for currency symbols
                return char
            return ''

        # Substitute punctuation (excluding dots between numbers and currency symbols)
        cleaned_segment = re.sub(r'[^\w\s]', replace_punctuation, segment)
        
        cleaned_segment = re.sub(r'\s+', ' ', cleaned_segment).strip()
        
        cleaned_segments.append(cleaned_segment)

    # Join all segments back together
    return ' '.join(cleaned_segments).strip()

def remove_stop_words(input_string: str) -> str:
    """
    Remove all stop words from the input string.
    
    This function removes any English stop words (e.g., 'the', 'is', 'in') from the input string.
    
    Args:
        input_string (str): The string from which to remove stop words.
    
    Returns:
        str: The processed string with stop words removed.
    """
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string")

    stop_words = set(stopwords.words('english'))
    words = input_string.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]

    return ' '.join(filtered_words)

def stem_text(input_string: str) -> str:
    """
    Apply stemming to each word in the input string using the Snowball Stemmer, while preserving URLs and email addresses.
    
    Args:
        input_string (str): The input string to be stemmed.
    
    Returns:
        str: The string with words stemmed, except for URLs.
    """
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string")

    # Initialize stemmer
    ps = SnowballStemmer(language='english')

    # Define URL pattern to skip URLs
    url_pattern = r'https?://[a-zA-Z0-9\-._~:/?#[\]@!$&\'()*+,;=%]+'
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    # Split the string based on URLs
    segments = re.split(f'({url_pattern}|{email_pattern})', input_string)
    
    # Process each segment
    processed_segments = []
    for segment in segments:
        segment = segment.strip()
        # Skip stemming for URL segments
        if re.match(url_pattern, segment) or re.match(email_pattern, segment):
            processed_segments.append(segment)
        else:
            # Tokenize and stem non-URL segments
            words = word_tokenize(segment)
            stemmed_words = [ps.stem(word) for word in words]
            processed_segments.append(' '.join(stemmed_words))

    # Join segments with a single space and clean up extra spaces
    cleaned_string = ' '.join(processed_segments).strip()
    return re.sub(r'\s+', ' ', cleaned_string)

def remove_special_characters(input_string: str) -> str:
    """
    Remove special characters and normalize the input string while preserving dots between numbers,
    currency symbols, email addresses, and URLs with http or https protocols.
    
    This function replaces special characters (such as '�') with their closest equivalents
    or removes them entirely, except for dots in numbers, currency symbols (e.g., €, £),
    and URLs starting with http or https. It uses Unicode normalization and regular expressions to clean the string.
    
    Args:
        input_string (str): The input string to be cleaned.
    
    Returns:
        str: The cleaned string with special characters removed or replaced, while preserving
        dots between numbers, currency symbols, emails, and URLs.
    """
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string")

    # Pattern to identify URLs starting with http or https
    url_pattern = r'(?:https?://[a-zA-Z0-9\-._~:/?#[\]@!$&\'()*+,;=%]+)'
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    # Normalize Unicode characters (NFKD will decompose characters into base characters + accents)
    normalized_string = unicodedata.normalize('NFKD', input_string)

    # Encode the string to ASCII bytes, ignoring characters that cannot be converted, then decode back to string
    def encode_except_currency(text):
        result = []
        for char in text:
            # Preserve € and £
            if char in ['€', '£']:
                result.append(char)
            else:
                # Encode other characters to ASCII, ignoring those that can't be encoded
                result.append(char.encode('ascii', 'ignore').decode('ascii'))
        return ''.join(result)

    # Apply the custom encoding function
    ascii_string = encode_except_currency(normalized_string)

    # Split the string based on URLs
    segments = re.split(f'({url_pattern})', ascii_string)

    # Process each segment individually
    cleaned_segments = []
    for segment in segments:
        segment = segment.strip()
        # Skip special character removal for URL segments
        if re.match(url_pattern, segment) or re.match(email_pattern, segment):
            cleaned_segments.append(segment)
            continue

        # Define a function to replace special characters while preserving dots between numbers and currency symbols
        def replace_special_characters(match):
            char = match.group(0)
            start = match.start()
            end = match.end()

            # Generalized condition: Preserve punctuation if it's between, before, or after digits, or within mathematical expressions
            if char in './-+%()':
                # Preserve if surrounded by digits or spaces followed by digits
                if ((start > 0 and segment[start - 1].isdigit()) or (end < len(segment) and segment[end].isdigit())) or \
                   ((start > 0 and segment[start - 1].isdigit()) and (end < len(segment) and segment[end].isspace())) or \
                   ((start > 0 and segment[start - 1].isspace()) and (end < len(segment) and segment[end].isdigit())) or \
                   (start > 0 and char in '()-'):
                    return char
                return ''
            if unicodedata.category(char) == 'Sc':  # 'Sc' is the Unicode category for currency symbols
                return char
            return ''

        # Use regex to match any character that is not alphanumeric, space, apostrophe, hyphen, or currency symbol
        cleaned_segment = re.sub(r'[^\w\s\'\-\.]', replace_special_characters, segment)

        # Clean up extra spaces and strip leading/trailing whitespace
        cleaned_segment = re.sub(r'\s+', ' ', cleaned_segment).strip()

        cleaned_segments.append(cleaned_segment)

    # Join all segments back together with a single space
    return ' '.join(cleaned_segments).strip()

def remove_encoded_data(input_string: str) -> str:
    """
    Remove encoded data such as hexadecimal codes, URL encodings, or other encoded characters.
    
    This function identifies and removes sequences like '%20', '\\xAB', and other encoded patterns.
    
    Args:
        input_string (str): The input string from which encoded data needs to be removed.
    
    Returns:
        str: The cleaned string with encoded data removed.
    """
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string")

    # Remove URL encodings like %20, %3A, etc.
    cleaned_string = re.sub(r'%[0-9A-Fa-f]{2}', '', input_string)

    # Remove hexadecimal escape sequences like \xAB or \u1234
    cleaned_string = re.sub(r'\\x[0-9A-Fa-f]{2}', '', cleaned_string)
    cleaned_string = re.sub(r'\\u[0-9A-Fa-f]{4}', '', cleaned_string)
    
    # Further clean the string by removing any lingering encoded patterns
    cleaned_string = re.sub(r'\\[0-9A-Fa-f]{1,4}', '', cleaned_string)

    # Remove any extra spaces left after encoded data removal
    cleaned_string = re.sub(r'\s+', ' ', cleaned_string).strip()

    return cleaned_string

def remove_tags(input_string: str) -> str:
    """
    Remove HTML, XML, or other tags from the input string and retain proper spacing.
    
    This function removes all text enclosed in angle brackets (<>), which typically
    denotes HTML/XML tags, and ensures spaces are kept between text that was separated by tags.
    
    Args:
        input_string (str): The input string from which tags need to be removed.
    
    Returns:
        str: The cleaned string with tags removed and proper spacing maintained.
    """
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string")

    # Regex pattern to match tags (anything between < and >, including nested tags)
    cleaned_string = re.sub(r'<[^>]+>', ' ', input_string)

    # Remove any extra spaces that may have been left after removing tags
    cleaned_string = re.sub(r'\s+', ' ', cleaned_string).strip()

    return cleaned_string
