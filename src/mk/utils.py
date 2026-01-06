import json

def save_data(file_path, data):

    """Save a list of dictionaries to the json file

    Args:
    file-path (str) : The path to the file where the dat should be saved .
    data (list[dict]): The list of dictionaries to sav. If None or empty, an empty 
    list will be saved.
    """
    if not data:
        data = []

    #Save the list of directories to the file
    with open(file_path, 'w') as file:
              json.dump(data, file, indent = 4)

def load_data(file_path):
    data = []
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
            
    except FileNotFoundError:
        return data
    
def get_line_delimiter():
     delimiter = "=========="
     
     return delimiter
