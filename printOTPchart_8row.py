import os
from base64 import b64decode

base_slk = "SUQ7UFdYTDtOO0UNClA7UEdlbmVyYWwNClA7UDANClA7UDAuMDANClA7UCMsIyMwDQpQO1AjLCMjMC4wMA0KUDtQIywjIzA7O1wtIywjIzANClA7UCMsIyMwOztbUmVkXVwtIywjIzANClA7UCMsIyMwLjAwOztcLSMsIyMwLjAwDQpQO1AjLCMjMC4wMDs7W1JlZF1cLSMsIyMwLjAwDQpQO1AiXCIjLCMjMDs7XC0iXCIjLCMjMA0KUDtQIlwiIywjIzA7O1tSZWRdXC0iXCIjLCMjMA0KUDtQIlwiIywjIzAuMDA7O1wtIlwiIywjIzAuMDANClA7UCJcIiMsIyMwLjAwOztbUmVkXVwtIlwiIywjIzAuMDANClA7UDAlDQpQO1AwLjAwJQ0KUDtQMC4wMEUrMDANClA7UCMjMC4wRSswDQpQO1AjXCA/Lz8NClA7UCNcID8/Lz8/DQpQO1B5eXl5L21tL2RkDQpQO1BkZC9tbW0veXkNClA7UGRkL21tbQ0KUDtQbW1tL3l5DQpQO1BoOm1tXCBBTS9QTQ0KUDtQaDptbTpzc1wgQU0vUE0NClA7UGg6bW0NClA7UGg6bW06c3MNClA7UHl5eXkvbW0vZGRcIGg6bW0NClA7UG1tOnNzDQpQO1BtbTpzcy4wDQpQO1BADQpQO1BbaF06bW06c3MNClA7UF8tIlwiKiAjLCMjMF8tOztcLSJcIiogIywjIzBfLTs7Xy0iXCIqICItIl8tOztfLUBfLQ0KUDtQXy0qICMsIyMwXy07O1wtKiAjLCMjMF8tOztfLSogIi0iXy07O18tQF8tDQpQO1BfLSJcIiogIywjIzAuMDBfLTs7XC0iXCIqICMsIyMwLjAwXy07O18tIlwiKiAiLSI/P18tOztfLUBfLQ0KUDtQXy0qICMsIyMwLjAwXy07O1wtKiAjLCMjMC4wMF8tOztfLSogIi0iPz9fLTs7Xy1AXy0NClA7UFwkIywjIzBfKTs7XChcJCMsIyMwXCkNClA7UFwkIywjIzBfKTs7W1JlZF1cKFwkIywjIzBcKQ0KUDtQXCQjLCMjMC4wMF8pOztcKFwkIywjIzAuMDBcKQ0KUDtQXCQjLCMjMC4wMF8pOztbUmVkXVwoXCQjLCMjMC4wMFwpDQpQO1BtbS9kZC95eQ0KUDtQeXl5eSKz4iJcIG1tIr/5IlwgZGQiwM8iDQpQO1BoIr3DIlwgbW0iutAiDQpQO1BoIr3DIlwgbW0iutAiXCBzcyLDyiINClA7UHl5eXki0rQiXCBtbSLqxSJcIGRkIuztIg0KUDtQbW0vZGQNClA7UHl5eXlcL21tXC9kZA0KUDtQeXl5eS9tbS9kZA0KUDtQbW0iv/kiXCBkZCLAzyINClA7UFtSZWRdWz0wXUdlbmVyYWwNClA7UFtSZWRdWzw+MF1HZW5lcmFsDQpQO0a1uL/yO00yMjANClA7RrW4v/I7TTIyMA0KUDtGtbi/8jtNMjIwDQpQO0a1uL/yO00yMjANClA7RbW4v/I7TTIyMA0KUDtFtbi/8jtNMTYwDQpQO0W1uL/yO00yMDANCkY7UDA7REcwRzg7TTI3MA0KQjtZMTAwMDtYNjtEMCAwIDk5OSA1DQpPO0w7RjtEO1YwO0s0NztUMDtHMTAwIDAuMDAxDQpGO1cxIDQgNg0KRjtXNSA1IDExDQpGO1AwO0ZHMEM7U003O0MxDQpGO1AwO0ZHMEM7U003O0MyDQpGO1AwO0ZHMEM7U003O0MzDQpGO1AwO0ZHMEM7U003O0M0DQpGO1AwO0ZHMEM7U003O0M1DQpGO1AwO0ZHMEM7U003O0M2DQpDO1kxO1gxO0siuLa18CINCkM7WDI7SyK52igxLzQpIg0KRjtQNDg7RkcwQztYMw0KQztLIjEvMTYiDQpDO1g0O0siwKfEoSINCkM7WDU7SyK1v8DbIg0KQztYNjtLIre5uqcosebAzCkiDQpDO1kyO1gxO0siaW50Ig0KQztYMjtLImVudCINCkM7WDM7SyJpbnQiDQpDO1g0O0siaW50Ig0KQztYNTtLImVudW0obixzLGMsZCxyKSINCkM7WDY7SyJpbnQiDQo="

slk = b64decode(base_slk)

# Global variable to store the name of the SM file
sm_name = ""

def open_sm():
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
    
    notes = [note.replace("\n", "") for note in data[27:]]
    madi_section = []
    madis = []
    
    for note in notes:
        
        if note == "," or note == ";":
            
            madis.append(madi_section)
            madi_section = []
            
        else:
            
            madi_section.append(note)
    
    return madis

def convert_sm_slk(notes):
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
    
    # In ra tất cả các notes
    for note in all_notes:
        print(note['pos0'], note['pos1'], note['pos2'], note['num_note'], note['enum'], note['value'])
        #print(note['column6']): vị trí của C lẻ/chẵn
def main():
    
    data_sm = open_sm()
    notes = extract_notes(data_sm)
    convert_sm_slk(notes)

main()
