import os
import re

# set directory path
directory = os.path.abspath(os.path.join("./", "TargetData"))

# iterate through all files in the directory
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    
    # check if file is a text file
    if filepath.endswith('.txt'):
        
        # read file contents
        with open(filepath, 'r') as f:
            file_contents = f.read()
        
        # remove line spaces and place each sentence on its own line
        file_contents = re.sub(r'\n|\r|\r\n', ' ', file_contents) # replace any existing line breaks with spaces
        file_contents = re.sub(r'\s*([.?!])\s*', r'\1\n', file_contents) # place each sentence on its own line
        
        # write updated contents back to file
        with open(filepath, 'w') as f:
            f.write(file_contents)
