# coding: utf-8
import nltk
import codecs
import numpy as np
import gensim

# Define the path to your Tiv corpus
corpus_file = r"C:\Users\user\Desktop\software\WSD\Tiv_Nballs\Tiv_Corpus\data\built_tiv_corpus.txt"

# Parameters for Word2Vec
vector_size = 100
window_size = 5
vocab_size = 10000
num_negative = 5

def get_min_count(sents):
    '''
    Args:
      sents: A list of lists. E.g., [["I", "am", "a", "boy", "."], ["You", "are", "a", "girl", "."]]
     
    Returns:
      min_count: A uint. Should be set as the parameter value of word2vec `min_count`.   
    '''
    from itertools import chain
     
    fdist = nltk.FreqDist(chain.from_iterable(sents))
    min_count = fdist.most_common(vocab_size)[-1][1]  # the count of the top-kth word
    return min_count

def make_wordvectors():
    print("Making sentences as list...")
    sents = []
    try:
        with codecs.open(corpus_file, 'r', 'utf-8') as fin:
            for line in fin:
                words = line.split()
                sents.append(words)
    except FileNotFoundError:
        print(f"Error: The file {corpus_file} does not exist.")
        return

    print("Making word vectors...")
    min_count = get_min_count(sents)
    model = gensim.models.Word2Vec(sents, vector_size=vector_size, min_count=min_count,
                                   negative=num_negative, 
                                   window=window_size)

    # Save the model
    model.save(corpus_file.replace('.txt', '.bin'))

    # Save the word vectors to a TSV file
    with codecs.open(corpus_file.replace('.txt', '.tsv'), 'w', 'utf-8') as fout:
        for i, word in enumerate(model.wv.index_to_key):
            fout.write(f"{i}\t{word}\t{np.array_str(model.wv[word])}\n")

if __name__ == "__main__":
    make_wordvectors()
    print("Done")
