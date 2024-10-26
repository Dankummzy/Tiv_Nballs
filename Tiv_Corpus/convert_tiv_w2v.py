import re

def change_format(file_name):
    """Convert initial file with word2vec features to standard format."""
    line_array = []
    current_word = None
    current_features = []

    # Open the initial file
    with open(file_name, 'r', encoding='utf-8') as initial_file:
        for line in initial_file:
            # Remove newline characters and unnecessary whitespace
            line = line.replace('\n', '').strip()

            # Check if line contains a word with features
            if "[" in line:
                # Remove the opening bracket and split by spaces
                line = line.replace('[', '').strip()
                parts = line.split()

                # The first part is the word, the rest are the features
                word = parts[1]  # Skip the index
                features = parts[2:]  # Get features after the word

                # If we have a previous word, append its features to line_array
                if current_word is not None:
                    formatted_line = f"{current_word} " + " ".join(current_features)
                    line_array.append(formatted_line + "\n")
                
                # Update current word and features
                current_word = word
                current_features = features

            elif "]" in line:
                # Handle lines with a closing bracket
                line = line.replace(']', '').strip()
                features = line.split()
                current_features.extend(features)  # Append features to current word's list

            else:
                # Handle any other line (if necessary, else this can be omitted)
                if line:  # Only append non-empty lines
                    features = line.split()
                    current_features.extend(features)  # Append features to current word's list

        # Append the last word and its features after the loop
        if current_word is not None:
            formatted_line = f"{current_word} " + " ".join(current_features)
            line_array.append(formatted_line + "\n")

    return line_array

def write_to_output_file(lines, file_name):
    """Write the formatted lines to the output file."""
    with open(file_name, 'w', encoding='utf-8') as file:  
        file.writelines(lines)  # Write lines directly

if __name__ == "__main__":
    w2v_file = r"C:\Users\user\Desktop\software\WSD\Tiv_Nballs\Tiv_Corpus\data\standardized_tiv_corpus.tsv" 
    output_w2v_file = "tiv_w2v.txt"  # Name of output file with w2v features
    formatted_line = change_format(w2v_file)
    write_to_output_file(formatted_line, output_w2v_file)
