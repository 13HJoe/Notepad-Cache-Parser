import os
import glob

app_data_dir = os.environ['LOCALAPPDATA']
#Variable stores the Path to \AppData\Local (Unique to each machine/user)
directory_relative = r"Packages\Microsoft.WindowsNotepad_8wekyb3d8bbwe\LocalState\TabState"
#don't add \Packages otherwise os.join will assume \Packages to be an absolute path
full_path = os.path.join(app_data_dir, directory_relative)
print(f"{full_path=}")

#to print all bin files in required directory
list_of_bin_files = glob.glob(os.path.join(full_path,'*.bin'))

for path in list_of_bin_files:
    if path.endswith('.0.bin') or path.endswith('.1.bin'):
        continue
    print("-"*80)
    #to print file names instead of file path -> use os.path.basename
    filename = os.path.basename(path)
    print(f"{filename=}")
    #print raw contents
    '''
    with open(path, 'rb') as file_pointer:
        contents = file_pointer.read()
        print(contents)
    '''
    with open(path, 'rb') as file_pointer:
        contents = file_pointer.read()

        magic_bytes = contents[0:3]
        is_saved_file = contents[3]
        #print(f'{magic_bytes=}')
        print(f'{is_saved_file=}')


        if is_saved_file:#byte set to 01
            print("Saved File")
            #length of filename = contents on the 4th byte
            length_of_filename = contents[4]
            filename_ending = 5+length_of_filename*2
            print(f"{length_of_filename}")
            file_name = contents[5:5+(length_of_filename*2)] #we are mulitplying by 2 to account for null hex bytes in every other location
            print(file_name.decode('utf-16'))

            #Contents of file
            delimiter_start = contents[filename_ending:].index(b"\x00\x01")
            #print(f"{delimiter_start=}")
            delimiter_end = contents[filename_ending:].index(b"\x01\x00\x00\x00")
            #print(f"{delimiter_end=}")

            delimiter_start += filename_ending #this value is index difference between actual index of \x00\x01
            delimiter_end += filename_ending   #to get the actual index(that corresponds to the file) and length of filename
            #print(f"{delimiter_start=}")
            #print(f"{delimiter_end=}")
            file_marker = contents[delimiter_start+2:delimiter_end]
            print(f"{file_marker=}")
            file_marker = file_marker[:len(file_marker)//2]

            #print(len(file_marker))
            #print("start index->",delimiter_end+4+len(file_marker))

            original_file_contents = contents[delimiter_end+4+len(file_marker):-5]
            original_file_contents = original_file_contents.decode('utf-16')
            print(original_file_contents)

            #print(data.decode('utf-16'))
        else:
            print("Not Saved File")

            delimiter_start = contents[0:].index(b"\x00\x01")
            delimiter_end = contents[0:].index(b"\x01\x00\x00\x00")

            print(f"{delimiter_start=}")
            print(f"{delimiter_end=}")

            file_marker = contents[delimiter_start+2:delimiter_end]
            file_marker = file_marker[:len(file_marker)//2]

            original_file_contents = contents[delimiter_end+4+len(file_marker):-5]
            print(original_file_contents.decode('utf-16'))
            #data = contents[:-5]
            #print(data.decode('utf-16'))
        print("-"*80)
