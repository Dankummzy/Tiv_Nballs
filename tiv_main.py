import sqlite3

# Connect to Tiv WordNet SQLite database
def connect_to_tiv_db():
    conn = sqlite3.connect('tiv_database/tivwordnet.db')
    return conn

# Fetch synsets for a given word
def get_synsets(word, cursor):
    cursor.execute("SELECT * FROM synsets WHERE lemma=?", (word,))
    return cursor.fetchall()

# Fetch hypernyms for a given synset (parent relationships)
def get_hypernyms(synset_id, cursor):
    cursor.execute("SELECT * FROM hypernyms WHERE sid=?", (synset_id,))
    return cursor.fetchall()

# Fetch hyponyms for a given synset (child relationships)
def get_hyponyms(synset_id, cursor):
    cursor.execute("SELECT * FROM hyponyms WHERE sid=?", (synset_id,))
    return cursor.fetchall()

# Create the index file based on Tiv wordnet and handle missing words
def create_index_file():
    conn = connect_to_tiv_db()
    cursor = conn.cursor()
    
    index_file = open("idx.dat", "w", encoding="utf-8")
    w2v_file = open("Tiv_Corpus/tiv_w2v.txt", encoding="utf-8")
    missing_words_file = open("missing_words.txt", "w", encoding="utf-8")  # Log missing words
    
    idx = 2  # start with index 2 because index 1 is reserved for *root*
    idx_dict = {}
    word_dict = {}
    
    for line in w2v_file:
        line = line.split(" ")
        word = line[0]
        
        # Try to fetch synsets for the word
        synsets = get_synsets(word, cursor)
        
        if len(synsets) > 0:
            num_of_sense = 0  # Counter for word senses
            for syn in synsets:
                synset_id, synset_word, definition = syn[:3]  # Adjust based on DB structure
                index_file.write(f"{idx} {synset_word} {num_of_sense} {definition}\n")
                
                if synset_word not in word_dict:
                    word_dict[synset_word] = []
                
                word_dict[synset_word].append(idx)
                idx_dict[idx] = definition
                idx += 1
                num_of_sense += 1
        else:
            # If the word is not found in the Tiv WordNet, log it
            missing_words_file.write(f"{word}\n")
            print(f"Word not found in WordNet: {word}")

    index_file.close()
    w2v_file.close()
    missing_words_file.close()
    conn.close()
    
    return word_dict, idx_dict

# Find parents (hypernyms) for each word sense
def find_parents(word_dict, idx_dict):
    conn = connect_to_tiv_db()
    cursor = conn.cursor()
    
    parent_dict = {}
    i2w = {}  # Maps index to word.n.sense format
    idx_file = open("idx.dat", 'r', encoding="utf-8")

    for line in idx_file:
        l_array = line.split(" ")
        idx = l_array[0]
        if idx.isdigit():
            word = l_array[1]
            syn_num = l_array[2]
            i2w[int(idx)] = f"{word}.n.{syn_num}"
            synsets = get_synsets(word, cursor)
            if len(synsets) > 0:
                synset_id = synsets[int(syn_num)][0]  # Adjust based on DB structure
                for hypernym in get_hypernyms(synset_id, cursor):
                    hypernym_id = hypernym[1]
                    parent_synset = cursor.execute("SELECT * FROM synsets WHERE synset_id=?", (hypernym_id,)).fetchone()
                    parent_word = parent_synset[1]
                    parent_definition = parent_synset[2]

                    if parent_word in word_dict:
                        for i in word_dict[parent_word]:
                            if idx_dict[i] == parent_definition:
                                parent_dict[int(idx)] = i

    idx_file.close()
    conn.close()
    return parent_dict, i2w


def find_children(parent_dict):
    child_dict = {}
    for i in idx_dict:
        word = i2w[i]
        child_dict[word] = [] #create array of children for each word_sense
    for par in parent_dict:
        word_idx = par
        word = i2w[word_idx]
        parent_idx = parent_dict[par]
        parent_word = i2w[parent_idx] #get parent word
        if word not in child_dict[parent_word]:
            child_dict[parent_word].append(word) #write word to the children list of it's parent
    return child_dict

def add_parent(idx): #function which returns index of the parent
    if idx in parent_dict:
        return parent_dict[idx]
    else:
        return 1

def make_catcode_file(idx_dict):
    catcode_file = open("catcode.dat", "w", encoding="utf-8")
    for i in idx_dict:
        word = i2w[i]
        catcode_file.write(word) #write word to file
        idx = i
        parents = []
        while idx != 1: #recursively get parents
            p_idx = add_parent(idx)
            parents.append(p_idx)
            idx = p_idx
        parents = parents[::-1] #inverse the order from the root to leaves
        length = len(parents)
        array = [0] * (17 - length)
        parents.extend(array) #get missing zeros to get the standard 17-length format
        for p in parents:
            catcode_file.write(" " + str(p))
        catcode_file.write("\n")
    catcode_file.close()

def delete_repititions(file_name): #in wordnet some words in synset repeat, which causes duplication in file. This function deletes duplicate lines of given file
    with open(file_name, 'r', encoding="utf-8") as source_file:
        lines = []
        for line in source_file:
            if line not in lines:
                lines.append(line)
        new_file = open(file_name + "_no_duplicates", 'w', encoding="utf-8")
        new_file.writelines(lines)
        new_file.close()
    source_file.close()

def create_word_sense_children_file(i2w, child_dict, idx_dict, parent_dict):
    word_sense_children_file = open("children.dat", "w", encoding="utf-8")
    child_dict["*root*"] = []  # add root for the correct format
    for i in idx_dict:
        if i not in parent_dict:  # word has no parent
            if i2w[i] not in child_dict["*root*"]:  # and not in the children of root yet
                child_dict["*root*"].append(i2w[i])  # add it to the children of root
    word_sense_children_file.write("*root*")
    for c in child_dict["*root*"]:
        word_sense_children_file.write(" " + c)
    word_sense_children_file.write("\n")
    for i in idx_dict:
        word = i2w[i]
        word_sense_children_file.write(word)
        for c in child_dict[word]:
            word_sense_children_file.write(" " + c)
        word_sense_children_file.write("\n")  # write children of word in one line
    word_sense_children_file.close()

if __name__ == "__main__":
    word_dict, idx_dict = create_index_file()
    parent_dict, i2w = find_parents(word_dict, idx_dict)
    child_dict = find_children(parent_dict)
    make_catcode_file(idx_dict)
    delete_repititions("catcode.dat")
    create_word_sense_children_file(i2w, child_dict, idx_dict, parent_dict)
    delete_repititions("children.dat")
