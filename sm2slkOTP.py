# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 2024

@author: Wilson & Trương Kỳ Anh QN
"""

from base64 import b64decode
import os

base_slk = "SUQ7UFdYTDtOO0UNClA7UEdlbmVyYWwNClA7UDANClA7UDAuMDANClA7UCMsIyMwDQpQO1AjLCMjMC4wMA0KUDtQIywjIzA7O1wtIywjIzANClA7UCMsIyMwOztbUmVkXVwtIywjIzANClA7UCMsIyMwLjAwOztcLSMsIyMwLjAwDQpQO1AjLCMjMC4wMDs7W1JlZF1cLSMsIyMwLjAwDQpQO1AiXCIjLCMjMDs7XC0iXCIjLCMjMA0KUDtQIlwiIywjIzA7O1tSZWRdXC0iXCIjLCMjMA0KUDtQIlwiIywjIzAuMDA7O1wtIlwiIywjIzAuMDANClA7UCJcIiMsIyMwLjAwOztbUmVkXVwtIlwiIywjIzAuMDANClA7UDAlDQpQO1AwLjAwJQ0KUDtQMC4wMEUrMDANClA7UCMjMC4wRSswDQpQO1AjXCA/Lz8NClA7UCNcID8/Lz8/DQpQO1B5eXl5L21tL2RkDQpQO1BkZC9tbW0veXkNClA7UGRkL21tbQ0KUDtQbW1tL3l5DQpQO1BoOm1tXCBBTS9QTQ0KUDtQaDptbTpzc1wgQU0vUE0NClA7UGg6bW0NClA7UGg6bW06c3MNClA7UHl5eXkvbW0vZGRcIGg6bW0NClA7UG1tOnNzDQpQO1BtbTpzcy4wDQpQO1BADQpQO1BbaF06bW06c3MNClA7UF8tIlwiKiAjLCMjMF8tOztcLSJcIiogIywjIzBfLTs7Xy0iXCIqICItIl8tOztfLUBfLQ0KUDtQXy0qICMsIyMwXy07O1wtKiAjLCMjMF8tOztfLSogIi0iXy07O18tQF8tDQpQO1BfLSJcIiogIywjIzAuMDBfLTs7XC0iXCIqICMsIyMwLjAwXy07O18tIlwiKiAiLSI/P18tOztfLUBfLQ0KUDtQXy0qICMsIyMwLjAwXy07O1wtKiAjLCMjMC4wMF8tOztfLSogIi0iPz9fLTs7Xy1AXy0NClA7UFwkIywjIzBfKTs7XChcJCMsIyMwXCkNClA7UFwkIywjIzBfKTs7W1JlZF1cKFwkIywjIzBcKQ0KUDtQXCQjLCMjMC4wMF8pOztcKFwkIywjIzAuMDBcKQ0KUDtQXCQjLCMjMC4wMF8pOztbUmVkXVwoXCQjLCMjMC4wMFwpDQpQO1BtbS9kZC95eQ0KUDtQeXl5eSKz4iJcIG1tIr/5IlwgZGQiwM8iDQpQO1BoIr3DIlwgbW0iutAiDQpQO1BoIr3DIlwgbW0iutAiXCBzcyLDyiINClA7UHl5eXki0rQiXCBtbSLqxSJcIGRkIuztIg0KUDtQbW0vZGQNClA7UHl5eXlcL21tXC9kZA0KUDtQeXl5eS9tbS9kZA0KUDtQbW0iv/kiXCBkZCLAzyINClA7UFtSZWRdWz0wXUdlbmVyYWwNClA7UFtSZWRdWzw+MF1HZW5lcmFsDQpQO0a1uL/yO00yMjANClA7RrW4v/I7TTIyMA0KUDtGtbi/8jtNMjIwDQpQO0a1uL/yO00yMjANClA7RbW4v/I7TTIyMA0KUDtFtbi/8jtNMTYwDQpQO0W1uL/yO00yMDANCkY7UDA7REcwRzg7TTI3MA0KQjtZMTAwMDtYNjtEMCAwIDk5OSA1DQpPO0w7RjtEO1YwO0s0NztUMDtHMTAwIDAuMDAxDQpGO1cxIDQgNg0KRjtXNSA1IDExDQpGO1AwO0ZHMEM7U003O0MxDQpGO1AwO0ZHMEM7U003O0MyDQpGO1AwO0ZHMEM7U003O0MzDQpGO1AwO0ZHMEM7U003O0M0DQpGO1AwO0ZHMEM7U003O0M1DQpGO1AwO0ZHMEM7U003O0M2DQpDO1kxO1gxO0siuLa18CINCkM7WDI7SyK52igxLzQpIg0KRjtQNDg7RkcwQztYMw0KQztLIjEvMTYiDQpDO1g0O0siwKfEoSINCkM7WDU7SyK1v8DbIg0KQztYNjtLIre5uqcosebAzCkiDQpDO1kyO1gxO0siaW50Ig0KQztYMjtLImludCINCkM7WDM7SyJpbnQiDQpDO1g0O0siaW50Ig0KQztYNTtLImVudW0obixzLGMsZCxyKSINCkM7WDY7SyJpbnQiDQo="
#base_slk = "SUQ7UENBTENPT08zMg0KQztYMTtZMTtLIk1BREkiDQpDO1gyO1kxO0siMS80Ig0KQztYMztZMTtLIjEvMTYiDQpDO1g0O1kxO0siQmVhdFRpbWUiDQpDO1g1O1kxO0siVHlwZSINCkM7WDY7WTE7SyJMZXZlbCINCkM7WDE7WTI7SyJpbnQiDQpDO1gyO1kyO0siaW50Ig0KQztYMztZMjtLImludCINCkM7WDQ7WTI7SyJpbnQiDQpDO1g1O1kyO0siZW51bShuLHMsYyxkLHIpIg0KQztYNjtZMjtLImludCINCg0KDQo="
# This line should contain the base64 encoded data for the output format

slk = b64decode(base_slk)  # Decodes the base64 data

# Global variable to store the name of the SM file
sm_name = ""

def open_sm_file():
    """
    Function to open and read the SM file.
    """
    global sm_name
    
    # List all files in the current directory
    file_list = os.listdir()
    sm_names = []
    
    # Filter out files with .sm extension
    for file in file_list:
        if file.endswith(".sm"):
            name, extension = os.path.splitext(file)
            sm_names.append(name)
            
    # If there are SM files, display them for selection
    if sm_names:
        for sm_number in range(len(sm_names)):
            print("["+str(sm_number+1)+"] "+sm_names[sm_number]+".sm")
            
    else:
        print("No .sm files to convert")
        exit()
        
    # Prompt user to choose an SM file to convert
    sm_num = int(input("\nChoose the file to convert [number]: "))
    sm_name = sm_names[sm_num-1]
    
    # Attempt to read the selected SM file with a specified encoding
    with open(sm_name+".sm", "r", encoding='utf-8') as file:
        lines = file.readlines()
     
    return lines

def extract_notes(data):
    """
    Extracts notes from the provided data, removing newlines and splitting based on commas or semicolons.
    """
    notes = [note.replace("\n", "") for note in data[27:]]  # Extract notes starting from line 27 (assuming specific format)
    section_madi = []
    madis = []
    for note in notes:
        if note == "," or note == ";":
            madis.append(section_madi)
            section_madi = []
        else:
            section_madi.append(note)
    return madis

def convert_sm_to_slk(notes):
    """
    Converts the extracted notes (SM format) to a format suitable for the target SLK file.
    This function currently prints the conversion details but doesn't create an output file.
    """
    resolution = 4
    note_position = [0, 0, 0]
    dictionary = {0: "n", 1: "c", 2: "s", 3: "n", 4: "c", 5: "s", 6: "d", 7: "r"}  # Mapping for note values

    output_data = []
    between_c_and_s = 0
    last_c_position = -1  # Keep track of the last "c" position for updates

    for section_madi in notes:
        number_of_madi_rows = len(section_madi)
        note_increment = int(resolution / (number_of_madi_rows / 4))

        for note_row in section_madi:
            note_number = (note_position[0] * 16) + (note_position[1] * 4) + note_position[2]
            if note_row != "00000000":
                for note in range(len(note_row)):
                    if note_row[note] == "1":
                        enum = dictionary.get(note)

                        if enum == "n":
                            if last_c_position != -1:
                                between_c_and_s += 1

                        if enum == "c" or enum == "d":
                            if enum == "c":
                                if last_c_position != -1:
                                    output_data[last_c_position] = output_data[last_c_position][:-1] + (between_c_and_s,)
                                last_c_position = len(output_data)
                            output_data.append((note_position[0], note_position[1], note_position[2], note_number, enum, 0))
                            between_c_and_s = 0  # Reset the counter for new "c" or "d"
                        elif enum == "s":
                            if last_c_position != -1:
                                # Update the last "c" entry with the count of "n" letters
                                output_data[last_c_position] = output_data[last_c_position][:-1] + (between_c_and_s,)
                                last_c_position = -1  # Reset last_c_position as "s" ends the counting
                            between_c_and_s = 0  # Reset counter after "s"
                            output_data.append((note_position[0], note_position[1], note_position[2], note_number, enum, 0))
                        else:
                            output_data.append((note_position[0], note_position[1], note_position[2], note_number, enum, 0))

            note_position[2] += note_increment
            if note_position[2] == resolution:
                note_position[2] = 0
                note_position[1] += 1
            if note_position[1] == 4:
                note_position[1] = 0
                note_position[0] += 1

    # Post-process for remaining "c" notes without "s"
    if last_c_position != -1:
        output_data[last_c_position] = output_data[last_c_position][:-1] + (between_c_and_s,)

    return output_data  # Return the converted notes

def save_notes(converted_notes):
    """
    Function to save the converted notes to an SLK file.
    """
    row_c = 3
    
    with open(sm_name+".slk", "wb") as f:
        f.write(slk)
        
        for row in converted_notes:
            store_value = "C;Y{};".format(row_c)
            
            for value in range(len(row)):
                if store_value == "":
                    store_value = "C;"
                    
                if value >= 4:
                    store_value += 'X{};K"{}"\r\n'.format(value+1, row[value])
                else:
                    store_value += 'X{};K{}\r\n'.format(value+1, row[value])
                    
                f.write(bytes(store_value, "utf-8"))
                store_value = ""
            
            row_c += 1
        
        f.write(bytes("E\r\n", "utf-8"))

def main():
    """
    Calls the functions to open the file, extract notes, and convert them.
    """
    data_sm = open_sm_file()
    notes = extract_notes(data_sm)
    converted_notes = convert_sm_to_slk(notes)
    save_notes(converted_notes)

if __name__ == "__main__":
    main()
