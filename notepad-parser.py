import os
import glob
from termcolor import colored

app_data_dir = os.environ['LOCALAPPDATA'] #Variable stores the Path to \AppData\Local (Unique to each machine/user)
directory_relative = r"Packages\Microsoft.WindowsNotepad_8wekyb3d8bbwe\LocalState\TabState" #don't add \Packages otherwise os.join will assume \Packages to be an absolute path ("r" signifies raw path) 
Full_path = os.path.join(app_data_dir, directory_relative) 
print(colored("Application Cache Full Path=","blue"),colored(Full_path,"green"))
#to get all bin files in required directory
list_of_bin_files = glob.glob(os.path.join(Full_path,'*.bin')) #glob.glob allows for search for pathnames matching a specfied pattern

for path in list_of_bin_files:
    if path.endswith('.0.bin') or path.endswith('.1.bin'): #unstable; not of concern
        continue
    print("-"*80) 
    
    #to print file names instead of file path -> use os.path.basename
    cache_filename = os.path.basename(path)
    print(colored("Binary Cache Filename=","light_blue"),colored(cache_filename,"green"))
    with open(path, 'rb') as file_pointer:
        contents = file_pointer.read()
        magic_bytes = contents[0:3] #NP.. -> Notepad Cache Header
        is_saved_file = contents[3]
        delimiter_start = 0
        delimiter_end = 0
        if is_saved_file:   #byte set to 01
            print(colored("SAVED FILE",'red'))
            length_of_filename = contents[4]    #length of filename = contents on the 4th byte
            filename_ending = 5+length_of_filename*2
            print("Length of filename:",length_of_filename)
            file_name = contents[5:filename_ending]     #we are mulitplying by 2 to account for null hex bytes in every other location
            file_name = file_name.decode('utf-16')
            file_name += "\""
            print(colored("Filename: \"","blue"),colored(file_name,'green')) #print contents of file
            delimiter_start = contents[filename_ending:].index(b"\x00\x01")
            delimiter_end = contents[filename_ending:].index(b"\x01\x00\x00\x00")
            delimiter_start += filename_ending
            delimiter_end += filename_ending
        else:
            print(colored("UNSAVED FILE",'red'))
            delimiter_start = contents[0:].index(b"\x00\x01")
            delimiter_end = contents[0:].index(b"\x01\x00\x00\x00")

        print(f"{delimiter_start=}","  ",f"{delimiter_end=}")
        file_marker = contents[delimiter_start+2:delimiter_end]
        file_marker = file_marker[:len(file_marker)//2]
        i = delimiter_end+4+len(file_marker)
        j = len(contents)-5
        print(f"{i=}","",f"{j=}")
        original_file_contents = contents[i:-5]
        lines =  original_file_contents.decode('utf-16le')
        lines = lines.splitlines()
        print("->","START OF FILE CONTENT")
        for line in lines:
            print(colored(line,"light_cyan"))
        print("->","EOF")
        print("-"*80)
