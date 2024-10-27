# Tiv Nballs Embeddings
This repository provides code and resources for training and testing nball embeddings on Tiv language data. The main goal was to generate word embeddings and test their neighbor relationships, providing insights into the semantic clustering of Tiv words. For the full implementation, including setup and evaluation, visit the original nball4tree repository.

# Installation
First install Python

```
git clone https://github.com/gnodisnait/nball4tree.git
cd nball4tree
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Training and Evaluating Tiv Nball Embeddings

## Step 1: Prepare Datasets and Resources
Corpus Source: The New Testament Bible in Tiv, available here (https://www.jw.org/en/library/bible/?contentLanguageFilter=tiv).
Word Vectors: Generated using Word2Vec on the cleaned and segmented Tiv corpus.
Python Packages: PyMuPDF, Gensim, Regex, and NLTK.

## Step 2: Training the Tiv Nball Embeddings
After preparing the Tiv corpus, run the following command to train the embeddings:

python nball.py --train_nball nball.txt --w2v tiv_w2v.txt --ws_child children.dat_no_duplicates --ws_catcode catcode.dat_no_duplicates --log log.txt
Adjustments: Set uma.n.0 as the first child in the main_training_process.py file.
Line 418: child0 = 'uma.n.0'
Line 517: def make_DC_for_first_level_children(root="*root*", firstChild='uma.n.0', ...)
Line 564: make_DC_for_first_level_children(root=root, firstChild='uma.n.0', ...)

This training process constructs Tiv language embeddings within a semantic tree structure.

## Step 3: Testing Tiv Nballs by Observing Neighboring Words
The following tests were conducted to observe the semantic clustering of word embeddings:

Test Word: zwa.n.0 (mouth)

python nball.py --neighbors zwa.n.0 --ball nballs2.txt --num 6
Result: Closest neighbors were zwa.n.1, ityough.n.1, tso.n.0, ityough.n.0, tso.n.1, and ku.n.0.


Test Word: atetan.n.0 (afternoon)

python nball.py --neighbors atetan.n.0 --ball nballs2.txt --num 6
Result: Closest neighbors were aikighe.n.0 (evening), va.n.0 (come), yem.n.0 (go), uma.n.0 (life), and tema.n.0 (sit).


Test Word: tse.n.0 (mature/old)

python nball.py --neighbors tse.n.0 --ball nballs2.txt --num 6
Result: Closest neighbors were ku.n.0 (death), yem.n.0 (go), kwagh.n.0 (thing), yange.n.0 (light), va.n.0 (come), and uma.n.0 (life).


Test Word: yem.n.0 (go)

python nball.py --neighbors yem.n.0 --ball nballs2.txt --num 6
Result: Closest neighbors were va.n.0 (come), yange.n.0 (light), iv.n.0 (full), uma.n.0 (life), ku.n.0 (death), and kwagh.n.0 (thing).

For detailed on the tivwordnet database, refer to this repository: (https://github.com/Dankummzy/tivwordnet).

Credits: https://github.com/valerie94/russian_nballs/