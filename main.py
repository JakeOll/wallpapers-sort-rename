import os
import json

# Main variables
directory = os.path.dirname(os.path.abspath(__file__))
prefix = ''
data_filename = 'data.json'
main_files = [os.path.basename(__file__), data_filename]

# General set up
    # if data.json don't exist, set up default values for rename 
if not os.path.exists(data_filename):
    with open(data_filename, 'w') as datafile:
        json.dump({'renamed_files': [], 'last_number': 1, 'max_digits': 0}, datafile)

# Main function
def rename_files():
    # Open the file with read and write permissions
    with open(data_filename, 'r+') as datafile:
        data = json.load(datafile)
        last_number = data['last_number']
        new_max = len_digits()

        # If the number of digits is different it will rename from scratch
        if new_max != data['max_digits']:
            last_number, data['renamed_files'] = 1, []
        
        # All files that we don't want to rename will be here
        data['renamed_files'].extend(main_files)
        new_files = [f for f in os.listdir(directory) if f not in data['renamed_files']]
        renamed_files = []

        # Renaming files
        for file in new_files:
            old_name = os.path.join(directory, file)
            extension = os.path.splitext(file)[-1]
            serial_number = str(last_number).zfill(new_max)
            basename = f'{prefix}_{serial_number}{extension}'
            new_name = os.path.join(directory, basename)
            os.rename(old_name, new_name)
            renamed_files.append(basename)
            last_number += 1
        
        # Save new data for the next execution
        data['last_number'] = last_number
        data['renamed_files'].extend(renamed_files)
        data['max_digits'] = new_max
        update_data(data)
        

def len_digits():
    # Take the number of files to rename and pass to string and know how many digits will have
    return len(str(len([f for f in os.listdir(directory)if not f.endswith(('.py', 'data.json', '.git', '.gitattributes', 'README.md'))])))

def update_data(data):
    # Save new data in JSON file
    with open(data_filename, "w") as datafile:
        json.dump(data, datafile)


if __name__ == '__main__':
    # print(main_files) for debug purposes
    rename_files()
