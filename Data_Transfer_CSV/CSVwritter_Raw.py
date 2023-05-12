import os
import csv
from collections import Counter

def write_to_csv(directory, common_words):
    # Create a Counter to store word frequencies
    word_counter = Counter()

    # get a list of all the files in the directory
    files = os.listdir(directory)

    # filter the list to include only text files
    txt_files = [f for f in files if f.endswith('.txt')]

    # sort the list of text files based on the number in the filename
    txt_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

    # Read the meta.csv file and create a dictionary to store the President and Date information for each file
    meta_info = {}
    with open(os.path.join(directory, "meta.csv"), "r") as meta_file:
        reader = csv.reader(meta_file)
        #headers = next(reader)  # skip header row
        for row in reader:
            meta_info[row[0]] = {"President": row[1], "Date": row[2]}

    # Loop over each file in the directory
    for filename in txt_files:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as f:
            # Open the file
            # Loop over each line in the file
            for line in f:
                # Split the line into words
                words = line.strip().split()
                # Update the word counter with the words from this line
                word_counter.update(words)

    # Get the most common words from the list and their counts
    most_common_words = [word for word, _ in word_counter.most_common() if word in common_words]

    # Create a dictionary to store the data to be written to the CSV file
    data = {}
    # Loop over each file in the directory
    for filename in txt_files:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as f:
            # Loop over each line in the file
            for i, line in enumerate(f):
                # Split the line into words
                words = line.strip().split()
                # Loop over each of the most common words
                for word in most_common_words:
                    # Check if the word appears in this line
                    if word in words:
                        # Add this line to the data dictionary
                        if word not in data:
                            data[word] = {"count": 0, "sentences": []}
                        data[word]["count"] += 1
                        data[word]["sentences"].append((line.strip(), i, filename))
                        #print(str(word) + " instace: " + str(data[word]["count"]))

 # Loop over each of the most common words and their sentences
    # Create a dictionary to store the number of lines in each file
    num_lines = {}
    # Loop over each file in the directory
    for filename in txt_files:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as f:
            # Count the number of lines in the file
            num_lines[filename] = sum(1 for _ in f)
    
    # Create a list to store the data to be written to the CSV file
    rows = []
    rows.append(["Target", "Sentence", "Line Number","Total Lines", "File Name", "Instance", "Total Instance", "President", "Date"])
    
    # Loop over each of the most common words and their sentences
    for word in most_common_words:
        instanceCount = 0
        if word in data:
            for sentence, sentence_number, filename in data[word]["sentences"]:
                instanceCount += 1
                # Check if the file name exists in the meta_info dictionary and extract the President and Date information if it does
                if filename in meta_info:
                    president = meta_info[filename]["President"]
                    date = meta_info[filename]["Date"]
                else:
                    president = ""
                    date = ""
                # Append the total number of lines in the file to the row
                total_lines = num_lines[filename]
                rows.append([word, sentence, sentence_number+1, total_lines, filename, instanceCount, data[word]["count"], president, date])


    # Write the data to the CSV file
    with open("common_sentences.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)



# Example usage
directory = os.path.abspath(os.path.join("./", "TargetData"))
print("Data written to common_sentences.csv")


common_words = ['government', 'people', 'us', 'world', 'states', 'nation', 'shall', 'country', 'one', 'peace', 'new', 'power', 
                'america', 'public', 'time', 'you', 'citizens', 'constitution', 'me', 'united', 'under', 'nations', 'union',
                  'freedom', 'free', 'war', 'american', 'made', 'national', 'men', 'good', 'make', 'life', 'years', 'spirit', 
                  'rights', 'law', 'justice', 'laws', 'congress', 'your', 'fellow', 'right', 'work', 'liberty', 'duty', 'hope',
                    'interests', 'state', 'god']
write_to_csv(directory, common_words)


