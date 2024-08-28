## Windows 11 Forensics - `Notepad Cache Parser`
 - Windows 11 stores data of unclosed tabs of the Notepad Application in `.bin` cache files
 - This script parses the `.bin` cache files of the application and extracts the original filename and content.
 - Usage
    ![image](https://github.com/user-attachments/assets/7f48c6f8-97f7-4494-8b74-041ced7578f2)

### Working
 - Raw Hex - *UNSAVED* file
   ![image](https://github.com/user-attachments/assets/187fbecc-edde-4f10-ae60-e75d6257d7a9)
 - Raw Hex - *SAVED* file
    - length of filename - index:4
    - extract filename - index:5 + length of filename * 2
      [multiplied by 2 to account for alternating `null` byte]
    - There seems to be a starting delimiter after the random bytes "\x00\x01".
    - The ending delimiter is of the format "\x01\x00\x00\x00".
    NOTE - this is common for both saved and unsaved files.
    - Between both these delimiters, there is a data marker that is half the length of the text data marker.
        - The text data marker is present at after the ".txt" extension and right before the first byte of text data.
    - NOTE - The length of the marker varies from one bin file to another, it might differ by file size.
        - To find index of starting delimiter:
            - cache_data[0:].index("\x00\x01")
        - To find index of ending delimiter:
            - cache_data[0:].index("\x01\x00\x00\x00")
        - To get file marker contents:
            - cache_data[startDelimit+2:endDelimit]
        - To get the starting index of the actual file data:
            - cache_data[endDelimit+4+len(fileMarker)]

   ![image](https://github.com/user-attachments/assets/71d57911-e38d-4727-b23f-4103a31acb65)

**note** :  the notepad application must be closed for the content of unsaved cache to be also parsed
