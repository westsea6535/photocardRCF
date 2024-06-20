import os

input_folder = './data/photocard/test'

# Get the list of files in the input folder
file_list = os.listdir(input_folder)

# Create a new .txt file with the same name as the original file
new_file_name = 'test.txt'
new_file_path = f'./data/{new_file_name}'

# Loop through each file in the list
with open(new_file_path, 'w') as file:
    for file_name in file_list:
        # Save the file name as a .txt file
        file.write(f'photocard/test/{file_name}\n')