import codecs
import regex
import re

def clean_text(text):
    """
    Clean input text by removing unnecessary special characters,
    correcting line breaks, and preserving meaningful symbols.
    """
    # Remove unwanted special characters like underscores and specific symbols
    text = re.sub(r'[_]+', ' ', text)  # Replace underscores with space
    text = re.sub(r'[ˆ]+', '', text)  # Remove 'ˆ' symbols
    text = re.sub(r'[^\w\s.,“”‘’—–\-]', '', text)  # Remove unwanted punctuation, but keep common ones
    text = re.sub(r'\d+', '', text)  # Remove digits

    # Normalize line breaks: replace multiple newlines with a single one
    text = re.sub(r'\n+', '\n', text)
    
    # Correct spacing around punctuation
    text = re.sub(r'\s*([.,“”‘’—–\-])\s*', r' \1 ', text)  # Normalize spaces around specific punctuation

    # Remove extra spaces
    text = re.sub(r'\s{2,}', ' ', text)  # Replace multiple spaces with a single space
    
    # Strip leading and trailing spaces
    return text.strip()

def sentence_segment(text):
    """
    Segment a paragraph into sentences based on Tiv punctuation rules.
    """
    # Use generic segmentation or modify for Tiv-specific punctuation if needed
    sentences = regex.split(r"([.!?])?[\n]+|[.!?] ", text)
    return sentences

def word_segment(sent):
    """
    Tokenize a sentence into words.
    """
    words = sent.split()  # Basic tokenization by splitting on spaces
    return words

def build_corpus(input_file, output_file, min_words=10):
    """
    Process the corpus from a text file, clean, segment, and store it.
    """
    with codecs.open(input_file, 'r', 'utf-8') as fin, codecs.open(output_file, 'w', 'utf-8') as fout:
        i = 1
        for line in fin:
            text = line.strip()
            if text:
                try:
                    cleaned_text = clean_text(text)
                    sentences = sentence_segment(cleaned_text)
                    for sent in sentences:
                        if sent:
                            words = word_segment(sent)
                            if len(words) > min_words:  # Only store sentences with more than `min_words`
                                fout.write(" ".join(words) + "\n")
                except Exception as e:
                    print(f"Error processing line {i}: {e}")
            i += 1
    print("Corpus building complete.")

if __name__ == "__main__":
    input_file = r"C:\Users\user\Desktop\software\WSD\nball4tree\Tiv_Corpus\data\tiv_corpus.txt"  
    output_file = r"C:\Users\user\Desktop\software\WSD\nball4tree\Tiv_Corpus\data\built_tiv_corpus.txt"
    build_corpus(input_file, output_file)
