# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 2025

@author: Wilson & Trương Kỳ Anh QN
"""

from base64 import b64decode
import os

base_slk = "SUQ7UENBTENPT08zMg0KQztYMTtZMTtLIk1BREkiDQpDO1gyO1kxO0siMS80Ig0KQztYMztZMTtLIjEvMTYiDQpDO1g0O1kxO0siQmVhdFRpbWUiDQpDO1g1O1kxO0siVHlwZSINCkM7WDY7WTE7SyJMZXZlbCINCkM7WDE7WTI7SyJpbnQiDQpDO1gyO1kyO0siaW50Ig0KQztYMztZMjtLImludCINCkM7WDQ7WTI7SyJpbnQiDQpDO1g1O1kyO0siZW51bShuLHMsYyxkLHIpIg0KQztYNjtZMjtLImludCINCg0KDQo="
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

from bisect import bisect_left, bisect_right

def convert_sm_to_slk(notes):
    # Khởi tạo biến output là một list rỗng
    output = [] 
    
    resolution = 4
    note_position = [0, 0, 0]
    dictionary = {0: "n", 1: "c", 2: "s", 3: "n", 4: "c", 5: "s", 6: "d", 7: "r"}
    
    c_count = 0  # Đếm số lượng 'c' đã xuất hiện (toàn file)
    all_notes = []
    current_chain = []  # list indices của c ODD trong all_notes
    pending_c_indices = []
    pending_local_ns = []

    for madi_section in notes:
        num_rows_madi = len(madi_section)
        # Sửa: Tránh chia cho 0 nếu num_rows_madi là 0
        note_increment = int(resolution / (num_rows_madi / 4)) if num_rows_madi > 0 else 0

        for row_note in madi_section:
            num_note = (note_position[0] * 16) + (note_position[1] * 4) + note_position[2]

            for lane in range(len(row_note)):
                char = row_note[lane]

                if char != "0":
                    enum_old = None
                    column6 = "0"

                    if char == "1":
                        enum_old = dictionary.get(lane)
                    elif char == "M":
                        enum_old = "c"
                    elif char == "2":
                        enum_old = "s"
                    elif char == "3":
                        enum_old = "d"
                    elif char == "4":
                        enum_old = "r"

                    if enum_old:
                        if enum_old == "c":
                            c_count += 1
                            column6 = "ODD" if c_count % 2 == 1 else "EVEN"
                        all_notes.append({
                            'pos0': note_position[0],
                            'pos1': note_position[1],
                            'pos2': note_position[2],
                            'num_note': num_note,
                            'lane': lane,
                            'enum': enum_old,
                            'column6': column6,
                            'value': 0
                        })

            # Cập nhật vị trí
            note_position[2] += note_increment
            while note_position[2] >= resolution:
                note_position[2] -= resolution
                note_position[1] += 1
                if note_position[1] >= 4:
                    note_position[1] = 0
                    note_position[0] += 1

    # Bây giờ xử lý chains để tính value cho c ODD
    for idx, note in enumerate(all_notes):
        if note['enum'] == "c" and note['column6'] == "ODD":
            current_chain.append(idx)
        elif note['enum'] == "s":
            if current_chain or pending_c_indices:
                # Tính local_ns cho current_chain nếu có
                local_ns = []
                if current_chain:
                    chain_len = len(current_chain)
                    local_ns = [0] * chain_len
                    for i in range(chain_len):
                        start_idx = current_chain[i] + 1
                        if i < chain_len - 1:
                            end_idx = current_chain[i + 1]
                        else:
                            end_idx = idx  # vị trí của s
                        for j in range(start_idx, end_idx):
                            if all_notes[j]['enum'] == "n":
                                local_ns[i] += 1

                # Kết hợp với pending
                full_c = pending_c_indices + current_chain
                full_local = pending_local_ns + local_ns
                total_n = sum(full_local)
                # Tính value
                if len(full_c) == 1:
                    value = total_n
                    all_notes[full_c[0]]['value'] = value
                else:
                    for k in range(len(full_c)):
                        remaining_n = full_local[k]
                        value = remaining_n * 100 + total_n
                        all_notes[full_c[k]]['value'] = value
                # Reset
                pending_c_indices = []
                pending_local_ns = []
                current_chain = []
        elif note['enum'] == "c" and note['column6'] == "EVEN":
            if current_chain:
                # Tính local_ns cho current_chain với end_idx = idx (c EVEN)
                chain_len = len(current_chain)
                local_ns = [0] * chain_len
                for i in range(chain_len):
                    start_idx = current_chain[i] + 1
                    if i < chain_len - 1:
                        end_idx = current_chain[i + 1]
                    else:
                        end_idx = idx  # vị trí của c EVEN
                    for j in range(start_idx, end_idx):
                        if all_notes[j]['enum'] == "n":
                            local_ns[i] += 1
                # Thêm vào pending
                pending_c_indices.extend(current_chain)
                pending_local_ns.extend(local_ns)
                # Reset current
                current_chain = []

    # Nếu còn pending hoặc current_chain sau cùng, có thể set value=0
    if pending_c_indices or current_chain:
        # Ví dụ set 0, hoặc tùy logic, nhưng ở đây giả sử không cần
        pass
    
    # Set value for EVEN by copying from nearest previous ODD
    last_odd_value = 0
    for note in all_notes:
        if note['enum'] == "c" and note['column6'] == "ODD":
            last_odd_value = note['value']
        elif note['enum'] == "c" and note['column6'] == "EVEN":
            note['value'] = last_odd_value
    
    # In ra tất cả các notes và lưu vào output
    for note in all_notes:
        # Sửa lỗi: Truyền một list/tuple các giá trị vào append
        output.append([note['pos0'], note['pos1'], note['pos2'], note['num_note'], note['enum'], note['value']])
        #print(note['column6']): vị trí của C lẻ/chẵn
        
    # Hàm này cần trả về danh sách các note đã chuyển đổi
    return output
    
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
