# -*- coding: utf-8 -*-
import re
from collections import Counter

class Tokenizer:
    '''Class for tokenizing Hindi text'''

    # Define suffixes and default stopwords as class variables
    suffixes = {
        1: ["ो", "े", "ू", "ु", "ी", "ि", "ा"],
        2: ["कर", "ाओ", "िए", "ाई", "ाए", "ने", "नी", "ना", "ते", "ीं",
            "ती", "ता", "ाँ", "ां", "ों", "ें"],
        3: ["ाकर", "ाइए", "ाईं", "ाया", "ेगी", "ेगा", "ोगी", "ोगे",
            "ाने", "ाना", "ाते", "ाती", "ाता", "तीं", "ाओं", "ाएं",
            "ुओं", "ुएं", "ुआं"],
        4: ["ाएगी", "ाएगा", "ाओगी", "ाओगे", "एंगी", "ेंगी", "एंगे",
            "ेंगे", "ूंगी", "ूंगा", "ातीं", "नाओं", "नाएं", "ताओं",
            "ताएं", "ियाँ", "ियों", "ियां"],
        5: ["ाएंगी", "ाएंगे", "ाऊंगी", "ाऊंगा", "ाइयाँ", "ाइयों",
            "ाइयां"],
    }

    default_stopwords = set([
        'के', 'का', 'है', 'और', 'से', 'को', 'की', 'पर', 'कि', 'यह', 'इस',
        'था', 'हैं', 'हूं', 'मैं', 'तो', 'ही', 'जो', 'अपने', 'ने', 'थे',
        'था', 'था', 'वह', 'आप', 'सबसे', 'द्वारा', 'लिए', 'हुई', 'भी', 'में',
        'किया', 'सकता', 'दो', 'वे', 'होता', 'वर्ग', 'जा', 'कहते', 'जब',
        'तक', 'नहीं', 'बनी', 'अब', 'और', 'कर', 'गया'
    ])

    def __init__(self, text=None):
        self.text = text if text is not None else ''
        self.sentences = []
        self.tokens = []
        self.stemmed_words = []
        self.final_tokens = []
        if self.text:
            self.clean_text()

    def read_from_file(self, filename):
        '''Reads text from a file and cleans it'''
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.text = f.read()
                self.clean_text()
        except FileNotFoundError:
            print(f"File {filename} not found.")
            self.text = ''
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            self.text = ''

    def clean_text(self):
        '''Cleans the text by removing digits and punctuation, but keeps sentence delimiters'''
        text = self.text
        # Remove digits
        text = re.sub(r'\d+', '', text)
        # Remove punctuation marks except sentence delimiters
        punctuation = r'[,()"\'“”‘’—\-:;!?|]'
        text = re.sub(punctuation, '', text)
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text)
        self.text = text.strip()

    def generate_sentences(self):
        '''Generates a list of sentences from the text'''
        # Split on '।' or '.'
        self.sentences = re.split(r'[।\.]', self.text)
        # Remove any empty sentences
        self.sentences = [sentence.strip() for sentence in self.sentences if sentence.strip()]

    def print_sentences(self, sentences=None):
        '''Prints the sentences'''
        sentences = sentences if sentences is not None else self.sentences
        for sentence in sentences:
            print(sentence)

    def remove_only_space_words(self):
        '''Removes tokens that are only spaces'''
        self.tokens = [tok for tok in self.tokens if tok.strip()]

    def hyphenated_tokens(self):
        '''Splits hyphenated tokens into separate tokens'''
        new_tokens = []
        for token in self.tokens:
            if '-' in token:
                new_tokens.extend(token.split('-'))
            else:
                new_tokens.append(token)
        self.tokens = new_tokens

    def tokenize(self):
        '''Tokenizes the text into words'''
        if not self.sentences:
            self.generate_sentences()
        tokens = []
        for sentence in self.sentences:
            word_list = sentence.split()
            tokens.extend(word_list)
        self.tokens = tokens
        self.remove_only_space_words()
        self.hyphenated_tokens()

    def print_tokens(self, tokens_list=None):
        '''Prints the tokens'''
        tokens_list = tokens_list if tokens_list is not None else self.tokens
        for token in tokens_list:
            print(token)

    def tokens_count(self):
        '''Returns the number of tokens'''
        return len(self.tokens)

    def sentence_count(self):
        '''Returns the number of sentences'''
        return len(self.sentences)

    def len_text(self):
        '''Returns the length of the text'''
        return len(self.text)

    def concordance(self, word):
        '''Finds sentences containing the specified word'''
        if not self.sentences:
            self.generate_sentences()
        return [sentence for sentence in self.sentences if word in sentence]

    def generate_freq_dict(self):
        '''Generates a frequency dictionary of tokens'''
        if not self.tokens:
            self.tokenize()
        return Counter(self.tokens)

    def print_freq_dict(self, freq):
        '''Prints the frequency dictionary'''
        for token, count in freq.items():
            print(f"{token}: {count}")

    def generate_stem_words(self, word):
        '''Stems the word by removing common suffixes'''
        for L in range(5, 0, -1):
            if len(word) > L + 1:
                for suf in self.suffixes[L]:
                    if word.endswith(suf):
                        return word[:-L]
        return word

    def generate_stem_dict(self):
        '''Returns a dictionary of stemmed words for each token'''
        if not self.tokens:
            self.tokenize()
        stem_dict = {}
        self.stemmed_words = []
        for token in self.tokens:
            stem = self.generate_stem_words(token)
            stem_dict[token] = stem
            self.stemmed_words.append(stem)
        return stem_dict

    def remove_stop_words(self, stopwords_file=None):
        '''Removes stop words from the stemmed words'''
        if not self.stemmed_words:
            self.generate_stem_dict()
        stopwords = set()
        if stopwords_file:
            try:
                with open(stopwords_file, 'r', encoding='utf-8') as f:
                    stopwords = set(line.strip() for line in f)
            except FileNotFoundError:
                print(f"Stopwords file {stopwords_file} not found. Using default stopwords.")
        if not stopwords:
            stopwords = self.default_stopwords
        tokens = [word for word in self.stemmed_words if word not in stopwords]
        self.final_tokens = tokens
        return tokens

if __name__ == "__main__":
    sample_text = '''वाशिंगटन: दुनिया के सबसे शक्तिशाली देश के राष्ट्रपति बराक ओबामा ने प्रधानमंत्री नरेंद्र मोदी के संदर्भ में टाइम पत्रिका में लिखा नरेंद्र मोदी ने अपने बाल्यकाल में अपने परिवार की सहायता करने के लिए अपने पिता की चाय बेचने में मदद की थी। आज वह दुनिया के सबसे बड़े लोकतंत्र के नेता हैं और गरीबी से प्रधानमंत्री तक की उनकी जिंदगी की कहानी भारत के उदय की गतिशीलता और क्षमता को परिलक्षित करती है।'''

    tokenizer = Tokenizer(sample_text)
    tokenizer.generate_sentences()
    # tokenizer.print_sentences()
    tokenizer.tokenize()
    # tokenizer.print_tokens()
    freq_dict = tokenizer.generate_freq_dict()
    # tokenizer.print_freq_dict(freq_dict)
    concordance_sentences = tokenizer.concordance('मोदी')
    # tokenizer.print_sentences(concordance_sentences)
    stem_dict = tokenizer.generate_stem_dict()
    # for original, stemmed in stem_dict.items():
    #     print(f"{original} -> {stemmed}")
    final_tokens = tokenizer.remove_stop_words()
    tokenizer.print_tokens(tokenizer.final_tokens)
    print(f"Sentence count: {tokenizer.sentence_count()}")
    print(f"Token count: {tokenizer.tokens_count()}")
    print(f"Text length: {tokenizer.len_text()}")
