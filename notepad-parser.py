import os
import glob
from termcolor import colored


# Get %LOCALAPPDATA% for Local Machine
app_data_directory = os.environ['LOCALAPPDATA']
# Location of cache
relative_path = r"Packages\Microsoft.WindowsNotepad_8wekyb3d8bbwe\LocalState\TabState"
# join machine-specific dir. with relative path
complete_path = os.path.join(app_data_directory,relative_path)
print(colored("Application Cache Full Path ->","blue"),
      colored(complete_path,"green"))

# find all filenames that end with '.bin' in the target directory
target_pattern = os.path.join(complete_path,"*.bin")
list_of_bin_filepaths = glob.glob(target_pattern)


# filter out unstable ".bin"
target_paths = []
for path in list_of_bin_filepaths:
    if path.endswith('.0.bin') or path.endswith('.1.bin'):
        continue
    target_paths.append(path)
del list_of_bin_filepaths


terminal_size = os.get_terminal_size()
terminal_width = int(terminal_size[0])


for path in target_paths:
    print("-" * terminal_width)
    cache_file_name = os.path.basename(path)
    print(colored("Cache File Name ->","light_blue"),
          colored(cache_file_name,"green"))
    
    fobj = open(path, 'rb')
    cache_data = fobj.read()
    # NP.. -> Notepad Cache Header
    notepad_cache_header = cache_data[0:3]
    is_saved_file = cache_data[3]
    delimiter_start = 0
    delimiter_end = 0

    if is_saved_file:
        # byte set to 1
        print(colored("SAVED FILE",'red'))

        # Extract File Name
        length_of_filename = cache_data[4]
        # compensate for byte form
        filename_end_marker = 5 + length_of_filename * 2
        file_name = cache_data[5:filename_end_marker]
        file_name = file_name.decode('utf-16')
        file_name = "\"" + file_name + "\""
        print(colored("[FILENAME]: ","blue"),colored(file_name, "green"))

        # find location of select bytes after the filename
        delimiter_start = cache_data[filename_end_marker:].index(b"\x00\x01")
        delimiter_end = cache_data[filename_end_marker:].index(b"\x01\x00\x00\x00")
        # adjust the found index which is relative to nd of filename 
        # to be relative to the start of the file 
        delimiter_start += filename_end_marker
        delimiter_end += filename_end_marker
    
    else:
        print(colored("UNSAVED FILE",'red'))
        delimiter_start = cache_data[0:].index(b"\x00\x01")
        delimiter_end = cache_data[0:].index(b"\x01\x00\x00\x00")
    

    # print(f"{delimiter_start=}"," ",f"{delimiter_end=}")

    # to get the data marker that is used to add fixed bytes after the extension
    # and just before the first byte of the actual data
    orig_file_data_marker = cache_data[delimiter_start+2:delimiter_end]
    orig_file_data_marker = orig_file_data_marker[:len(orig_file_data_marker)//2]
    
    # get start index of original file data
    i = delimiter_end + 4 + len(orig_file_data_marker)
    # remove trailing bytes
    j = len(cache_data)-5
    original_file_content = cache_data[i:j]
    original_file_content = original_file_content.decode('utf-16le')
    lines = original_file_content.splitlines()

    
    print(colored("[CONTENT]","blue"))
    for line in lines:
        print(colored(line,"light_green"))
    
    print(colored("[EOF]","red"))
    print("-" * terminal_width)
    fobj.close() 
