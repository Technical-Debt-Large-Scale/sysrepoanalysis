import os
import shutil
import json

def create_empty_file(path):
    with open(path, 'a') as file: 
        os.utime(path, None)
    return file

def delete_file(path): 
    if os.path.exists(path):
        os.remove(path)
    else:
        raise RuntimeError(f'The file {path} does not exists!')

def user_directory(path_repositories, user_id):
    user_path = path_repositories + '/' + str(user_id)

    if os.path.exists(user_path):
        return user_path
    else: 
        os.makedirs(user_path)
        return user_path   

def save_dictionary_in_json_file(name, user_id, my_dictionary, path_repositories): 
        try: 
            singleName = name + ".json"
            #Create the user directory if not existe
            temp_path = user_directory(path_repositories, user_id)
            fileName =  temp_path + '/' + singleName
            with open(fileName, 'w', encoding="utf-8") as jsonFile:
                json.dump(my_dictionary, jsonFile)
            print(f'The file {singleName} was saved with success!')
        except Exception as e:
            print(f'Error when try to save the json file: {e}')