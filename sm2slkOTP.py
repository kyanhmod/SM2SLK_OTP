# -*- coding: utf-8 -*-
"""
sm2slk_8col - Chuyên chuyển đổi StepMania (.sm) <-> Audition (.slk) DẠNG 8 CỘT (OTP)
Created by Wilson & Truong Ky Anh QN (TKAQN)
"""

import os
import sys
import re
from base64 import b64decode
import tkinter as tk
from tkinter import messagebox, filedialog

BASE_SLK_HEADER_B64 = (
    "SUQ7UENBTENPT08zMg0KQztYMTtZMTtLIk1BREkiDQpDO1gyO1kxO0siMS80Ig0K"
    "QztYMztZMTtLIjEvMTYiDQpDO1g0O1kxO0siQmVhdFRpbWUiDQpDO1g1O1kxO0si"
    "VHlwZSINCkM7WDY7WTE7SyJMZXZlbCINCkM7WDE7WTI7SyJpbnQiDQpDO1gyO1ky"
    "O0siaW50Ig0KQztYMztZMjtLImludCINCkM7WDQ7WTI7SyJpbnQiDQpDO1g1O1ky"
    "O0siZW51bShuLHMsYyxkLHIpIg0KQztYNjtZMjtLImludCINCg0KDQo="
)
SLK_HEADER = b64decode(BASE_SLK_HEADER_B64)


# ---------------------------------------------------------------------------
# SM Parsing
# ---------------------------------------------------------------------------
def extract_notes_8col(lines):
    notes_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("#NOTES:"):
            notes_idx = i
            break

    if notes_idx == -1:
        raw_notes = lines[27:]
    else:
        colon_count = 0
        raw_notes = []
        found_start = False
        for line in lines[notes_idx:]:
            if not found_start:
                colon_count += line.count(":")
                if colon_count >= 6:
                    found_start = True
                    parts = line.split(":")
                    if len(parts) > 6:
                        raw_notes.append(":".join(parts[6:]))
            else:
                raw_notes.append(line)

    section_madi, madis = [], []
    for line in raw_notes:
        s = line.strip()
        if not s or s.startswith("//"):
            continue
        if s == "," or s == ";":
            madis.append(section_madi)
            section_madi = []
            if s == ";":
                break
        else:
            section_madi.append(s)

    if section_madi:
        madis.append(section_madi)

    return madis


# ---------------------------------------------------------------------------
# SM -> SLK (8 Cột OTP)
# ---------------------------------------------------------------------------
def convert_sm_to_slk_8col(notes):
    resolution = 4
    note_position = [0, 0, 0]
    dictionary = {0: "n", 1: "c", 2: "s", 3: "n", 4: "c", 5: "s", 6: "d", 7: "r"}
    all_notes = []

    for madi_section in notes:
        num_rows_madi = len(madi_section)
        note_increment = int(resolution / (num_rows_madi / 4)) if num_rows_madi > 0 else 0
        for row_note in madi_section:
            num_note = (note_position[0] * 16) + (note_position[1] * 4) + note_position[2]
            for lane, char in enumerate(row_note):
                if char != "0":
                    enum_old = None
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
                        all_notes.append({
                            'pos0': note_position[0],
                            'pos1': note_position[1],
                            'pos2': note_position[2],
                            'num_note': num_note,
                            'lane': lane,
                            'enum': enum_old,
                            'column6': "PENDING" if enum_old == "c" else "",
                            'value': 0
                        })
            note_position[2] += note_increment
            while note_position[2] >= resolution:
                note_position[2] -= resolution
                note_position[1] += 1
                if note_position[1] >= 4:
                    note_position[1] = 0
                    note_position[0] += 1

    # Xử lý c trước d
    for i in range(len(all_notes) - 1):
        if all_notes[i]['enum'] == 'c' and all_notes[i+1]['enum'] == 'd':
            all_notes[i]['column6'] = "IGNORED_CD"
            all_notes[i]['value'] = 0

    c_count = 0
    for note in all_notes:
        if note['enum'] == 'c' and note['column6'] == "PENDING":
            c_count += 1
            note['column6'] = "ODD" if c_count % 2 == 1 else "EVEN"

    current_chain = []
    pending_c_indices = []
    pending_local_ns = []
    d_values_pool = []

    for idx, note in enumerate(all_notes):
        if note['enum'] == "c" and note['column6'] == "ODD":
            current_chain.append(idx)
        elif note['enum'] == "s":
            if current_chain or pending_c_indices:
                local_ns = []
                if current_chain:
                    chain_len = len(current_chain)
                    local_ns = [0] * chain_len
                    for i in range(chain_len):
                        start_idx = current_chain[i] + 1
                        end_idx = current_chain[i + 1] if i < chain_len - 1 else idx
                        for j in range(start_idx, end_idx):
                            if all_notes[j]['enum'] == "n":
                                local_ns[i] += 1

                full_c = pending_c_indices + current_chain
                full_local = pending_local_ns + local_ns
                total_n = sum(full_local)
                if len(full_c) == 1:
                    all_notes[full_c[0]]['value'] = total_n
                else:
                    for k in range(len(full_c)):
                        all_notes[full_c[k]]['value'] = full_local[k] * 100 + total_n

                last_odd_val = all_notes[full_c[-1]]['value']
                d_values_pool.append(last_odd_val % 100 if last_odd_val > 11 else last_odd_val)
                pending_c_indices = []
                pending_local_ns = []
                current_chain = []
        elif note['enum'] == "c" and note['column6'] == "EVEN":
            if current_chain:
                chain_len = len(current_chain)
                local_ns = [0] * chain_len
                for i in range(chain_len):
                    start_idx = current_chain[i] + 1
                    end_idx = current_chain[i + 1] if i < chain_len - 1 else idx
                    for j in range(start_idx, end_idx):
                        if all_notes[j]['enum'] == "n":
                            local_ns[i] += 1
                pending_c_indices.extend(current_chain)
                pending_local_ns.extend(local_ns)
                current_chain = []
        elif note['enum'] == 'd':
            note['value'] = d_values_pool.pop(0) if d_values_pool else 0
        elif note['enum'] == 'r':
            d_values_pool.clear()

    last_odd_value = 0
    for note in all_notes:
        if note['enum'] == "c" and note['column6'] == "ODD":
            last_odd_value = note['value']
        elif note['enum'] == "c" and note['column6'] == "EVEN":
            note['value'] = last_odd_value

    output = []
    for note in all_notes:
        output.append([note['pos0'], note['pos1'], note['pos2'], note['num_note'], note['enum'], note['value']])
    return output


def format_slk(converted_notes):
    out = bytearray(SLK_HEADER)
    row_c = 3
    for row in converted_notes:
        store_value = "C;Y{};".format(row_c)
        for value in range(len(row)):
            if store_value == "":
                store_value = "C;"
            if value >= 4:
                store_value += 'X{};K"{}"\r\n'.format(value + 1, row[value])
            else:
                store_value += 'X{};K{}\r\n'.format(value + 1, row[value])
            out.extend(store_value.encode("utf-8"))
            store_value = ""
        row_c += 1
    out.extend(b"E\r\n")
    return bytes(out)


# ---------------------------------------------------------------------------
# SLK -> SM (8 Cột OTP)
# ---------------------------------------------------------------------------
def parse_slk(slk_content):
    all_notes = []
    current_row = {}
    last_y = None
    max_madi = 0

    lines = slk_content.splitlines()
    for line in lines:
        line = line.strip()
        m_y = re.search(r'Y(\d+)', line)
        if m_y:
            y = int(m_y.group(1))
            if y != last_y:
                if 'madi' in current_row:
                    all_notes.append(current_row)
                    max_madi = max(max_madi, current_row['madi'])
                current_row = {}
                last_y = y
        m_x = re.search(r'X(\d+);K"?([^"]+)"?', line)
        if m_x:
            col = int(m_x.group(1))
            val = m_x.group(2)
            if col == 1: current_row['madi'] = int(val)
            elif col == 2: current_row['p1'] = int(val)
            elif col == 3: current_row['p2'] = int(val)
            elif col == 4: current_row['beat'] = int(val)
            elif col == 5: current_row['type'] = val
            elif col == 6: current_row['level'] = int(val)

    if 'madi' in current_row:
        all_notes.append(current_row)
        max_madi = max(max_madi, current_row['madi'])

    return all_notes, max_madi


def detect_defaults_for_slk(slk_path):
    base_dir = os.path.dirname(slk_path)
    base_file = os.path.splitext(os.path.basename(slk_path))[0]
    song_name = base_file[4:] if base_file.startswith("12P_") else base_file

    music_file = f"{song_name}.ogg"
    if base_dir and os.path.exists(base_dir):
        for fname in os.listdir(base_dir):
            if fname.lower().endswith((".ogg", ".mp3", ".wav")):
                music_file = fname
                break

    bpm = "120"
    m_bpm = re.search(r'\((\d+(?:\.\d+)?)\)', base_dir or "")
    if m_bpm:
        bpm = m_bpm.group(1)

    if base_dir:
        orig_sm = os.path.join(base_dir, f"{song_name}.sm")
        if os.path.exists(orig_sm):
            try:
                with open(orig_sm, "r", encoding="utf-8") as f:
                    c = f.read()
                m_title = re.search(r'#TITLE:([^;]*);', c, re.IGNORECASE)
                if m_title and m_title.group(1).strip() and m_title.group(1).strip().lower() != "unknown":
                    song_name = m_title.group(1).strip()
                m_mus = re.search(r'#MUSIC:([^;]*);', c, re.IGNORECASE)
                if m_mus and m_mus.group(1).strip():
                    music_file = m_mus.group(1).strip()
                m_b = re.search(r'#BPMS:0\.000=([0-9.]+)', c, re.IGNORECASE)
                if m_b:
                    bpm = m_b.group(1)
            except Exception:
                pass

    return song_name, music_file, bpm


def convert_slk_to_sm_8col(slk_path, title=None, music_file=None, bpm=None):
    with open(slk_path, "r", encoding="utf-8") as f:
        slk_content = f.read()

    all_notes, max_madi = parse_slk(slk_content)
    total_madis = max_madi + 1

    chart_type = "dance-otp"
    empty_row = "00000000"

    for i in range(len(all_notes) - 1):
        if all_notes[i]['type'] == 'c' and all_notes[i+1]['type'] == 'd':
            all_notes[i]['is_cd'] = True
        else:
            all_notes[i]['is_cd'] = False
    if all_notes:
        all_notes[-1]['is_cd'] = False

    valid_c_count = 0
    current_actor = "player"
    for n in all_notes:
        ntype = n['type']
        if ntype == 'c':
            if not n.get('is_cd', False):
                valid_c_count += 1
                current_actor = "player" if (valid_c_count % 2 == 1) else "npc"
            else:
                current_actor = "player"
            n['actor'] = current_actor
        else:
            n['actor'] = current_actor

    for n in all_notes:
        ntype = n['type']
        actor = n['actor']
        if ntype == 'r': lane = 7
        elif ntype == 'd': lane = 6
        elif actor == 'player':
            if ntype == 'n': lane = 0
            elif ntype == 'c': lane = 1
            elif ntype == 's': lane = 2
        else:
            if ntype == 'n': lane = 3
            elif ntype == 'c': lane = 4
            elif ntype == 's': lane = 5
        n['lane'] = lane

    notes_by_madi = {}
    for n in all_notes:
        notes_by_madi.setdefault(n['madi'], []).append(n)

    madis = []
    for madi_idx in range(total_madis):
        notes = notes_by_madi.get(madi_idx, [])
        if not notes:
            row_count = 4
        else:
            p2s = [n['p2'] for n in notes]
            if any(p2 % 2 != 0 for p2 in p2s):
                row_count = 16
            elif any(p2 != 0 for p2 in p2s):
                row_count = 8
            else:
                row_count = 4

        rows = [empty_row] * row_count
        step = 16 // row_count
        for n in notes:
            idx_16 = n['p1'] * 4 + n['p2']
            row_idx = idx_16 // step
            r_chars = list(rows[row_idx])
            r_chars[n['lane']] = '1'
            rows[row_idx] = "".join(r_chars)
        madis.append(rows)

    base_file = os.path.splitext(os.path.basename(slk_path))[0]
    def_song_name = base_file[4:] if base_file.startswith("12P_") else base_file

    final_title = title if title else def_song_name
    final_music = music_file if music_file else f"{def_song_name}.ogg"

    bpm_fmt = "120.000"
    if bpm:
        try:
            bpm_fmt = f"{float(bpm):.3f}"
        except ValueError:
            bpm_fmt = str(bpm)

    sm_header = (
        f"#TITLE:{final_title};\n"
        f"#SUBTITLE:;\n"
        f"#ARTIST:;\n"
        f"#TITLETRANSLIT:;\n"
        f"#SUBTITLETRANSLIT:;\n"
        f"#ARTISTTRANSLIT:;\n"
        f"#GENRE:;\n"
        f"#CREDIT:;\n"
        f"#MUSIC:{final_music};\n"
        f"#BANNER:;\n"
        f"#BACKGROUND:;\n"
        f"#CDTITLE:;\n"
        f"#SAMPLESTART:0.000;\n"
        f"#SAMPLELENGTH:0.000;\n"
        f"#SELECTABLE:YES;\n"
        f"#OFFSET:0.000;\n"
        f"#BPMS:0.000={bpm_fmt};\n"
        f"#STOPS:;\n"
        f"#BGCHANGES:;\n"
        f"#FGCHANGES:;\n"
        f"//--------------- {chart_type} -  ----------------\n"
        f"#NOTES:\n"
        f"     {chart_type}:\n"
        f"     :\n"
        f"     Beginner:\n"
        f"     1:\n"
        f"     0,0,0,0,0:\n"
    )

    measure_texts = ["\n".join(m) for m in madis]
    return sm_header + "\n,\n".join(measure_texts) + "\n;\n"


# ---------------------------------------------------------------------------
# High-Level Actions
# ---------------------------------------------------------------------------
def do_convert_sm_to_slk_8col(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    madis = extract_notes_8col(lines)
    converted = convert_sm_to_slk_8col(madis)
    slk_bytes = format_slk(converted)

    dir_name = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    out_filename = f"12P_{base_name}.slk"
    out_path = os.path.join(dir_name, out_filename) if dir_name else out_filename

    with open(out_path, "wb") as f:
        f.write(slk_bytes)

    return out_path


def do_convert_slk_to_sm_8col(file_path, title=None, music_file=None, bpm=None):
    dir_name = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    song_name = base_name[4:] if base_name.startswith("12P_") else base_name

    sm_content = convert_slk_to_sm_8col(file_path, title=title, music_file=music_file, bpm=bpm)
    out_filename = f"{song_name}.sm"
    out_path = os.path.join(dir_name, out_filename) if dir_name else out_filename

    with open(out_path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(sm_content)

    return out_path


# ---------------------------------------------------------------------------
# Metadata Dialog
# ---------------------------------------------------------------------------
class MetadataDialog8Col(tk.Toplevel):
    def __init__(self, parent, default_title, default_music, default_bpm, base_dir):
        super().__init__(parent)
        self.title("Cài đặt thông tin bài hát (SLK → SM 8 Cột)")
        self.result = None
        self.base_dir = base_dir
        self.resizable(False, False)
        self.configure(bg="#F8F9FA")
        self.transient(parent)
        self.grab_set()

        w, h = 430, 275
        px = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        py = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{px}+{py}")

        font_label = ("Segoe UI Semibold", 9)
        font_entry = ("Segoe UI", 10)
        font_btn = ("Segoe UI", 9)

        frame = tk.Frame(self, bg="#F8F9FA", padx=20, pady=15)
        frame.pack(fill="both", expand=True)

        # Title
        lbl_t = tk.Label(frame, text="Tên bài hát (Title):", font=font_label, bg="#F8F9FA", anchor="w")
        lbl_t.pack(fill="x")
        self.ent_title = tk.Entry(frame, font=font_entry)
        self.ent_title.insert(0, default_title)
        self.ent_title.pack(fill="x", pady=(2, 10))

        # Music file
        lbl_m = tk.Label(frame, text="Tên file nhạc (Music - ví dụ song.ogg):", font=font_label, bg="#F8F9FA", anchor="w")
        lbl_m.pack(fill="x")
        m_frame = tk.Frame(frame, bg="#F8F9FA")
        m_frame.pack(fill="x", pady=(2, 10))
        self.ent_music = tk.Entry(m_frame, font=font_entry)
        self.ent_music.insert(0, default_music)
        self.ent_music.pack(side="left", fill="x", expand=True)
        btn_browse_music = tk.Button(m_frame, text="Chọn...", font=font_btn, relief="groove", padx=8, command=self.on_browse_audio)
        btn_browse_music.pack(side="right", padx=(6, 0))

        # BPM
        lbl_b = tk.Label(frame, text="Tốc độ bài hát (BPM - ví dụ 140 hoặc 145):", font=font_label, bg="#F8F9FA", anchor="w")
        lbl_b.pack(fill="x")
        self.ent_bpm = tk.Entry(frame, font=font_entry)
        self.ent_bpm.insert(0, str(default_bpm))
        self.ent_bpm.pack(fill="x", pady=(2, 16))

        # Buttons
        b_frame = tk.Frame(frame, bg="#F8F9FA")
        b_frame.pack(fill="x")
        btn_ok = tk.Button(
            b_frame, text="Chuyển đổi", font=font_btn, bg="#28A745", fg="white",
            activebackground="#218838", relief="flat", padx=16, pady=5, cursor="hand2", command=self.on_ok
        )
        btn_ok.pack(side="right", padx=(8, 0))
        btn_cancel = tk.Button(
            b_frame, text="Hủy", font=font_btn, bg="#6C757D", fg="white",
            activebackground="#5A6268", relief="flat", padx=16, pady=5, cursor="hand2", command=self.on_cancel
        )
        btn_cancel.pack(side="right")

        self.bind("<Return>", lambda e: self.on_ok())
        self.bind("<Escape>", lambda e: self.on_cancel())
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.ent_bpm.focus_set()
        self.wait_window(self)

    def on_browse_audio(self):
        f = filedialog.askopenfilename(
            initialdir=self.base_dir,
            title="Chọn file nhạc audio",
            filetypes=[("Audio files", "*.ogg;*.mp3;*.wav"), ("All files", "*.*")]
        )
        if f:
            self.ent_music.delete(0, tk.END)
            self.ent_music.insert(0, os.path.basename(f))

    def on_ok(self):
        bpm_str = self.ent_bpm.get().strip()
        try:
            bpm_val = float(bpm_str)
            if bpm_val <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "BPM phải là một con số hợp lệ lớn hơn 0 (ví dụ: 140 hoặc 145)!", parent=self)
            self.ent_bpm.focus_set()
            return

        music_str = self.ent_music.get().strip()
        if not music_str:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên file nhạc!", parent=self)
            self.ent_music.focus_set()
            return

        title_str = self.ent_title.get().strip() or "unknown"
        self.result = {
            "title": title_str,
            "music": music_str,
            "bpm": f"{bpm_val:.3f}"
        }
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()


# ---------------------------------------------------------------------------
# GUI 8 Cột
# ---------------------------------------------------------------------------
class SM2SLK8ColApp:
    def __init__(self, root):
        self.root = root
        self.root.title("sm2slk - 8 Cột (OTP)")
        self.root.geometry("380x260")
        self.root.resizable(False, False)

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - 380) // 2
        y = (sh - 260) // 2
        self.root.geometry(f"380x260+{x}+{y}")
        self.root.configure(bg="#F8F9FA")

        font_title = ("Segoe UI Semibold", 13)
        font_btn = ("Segoe UI", 10)
        font_foot = ("Segoe UI", 9)

        frame = tk.Frame(self.root, bg="#F8F9FA", padx=20, pady=16)
        frame.pack(fill="both", expand=True)

        lbl_title = tk.Label(frame, text="Audition 8-Cột (OTP) Converter", font=font_title, bg="#F8F9FA", fg="#212529")
        lbl_title.pack(pady=(0, 4))

        lbl_sub = tk.Label(frame, text="Chuyển đổi 2 chiều StepMania (.sm) ⇄ SLK (.slk)", font=("Segoe UI", 9), bg="#F8F9FA", fg="#6C757D")
        lbl_sub.pack(pady=(0, 14))

        btn_sm2slk = tk.Button(
            frame, text="1. Chuyển SM → SLK (8 Cột OTP)",
            font=font_btn, bg="#28A745", fg="white", activebackground="#218838",
            relief="flat", padx=10, pady=7, cursor="hand2",
            command=self.on_sm_to_slk
        )
        btn_sm2slk.pack(fill="x", pady=5)

        btn_slk2sm = tk.Button(
            frame, text="2. Chuyển SLK → SM (8 Cột OTP)",
            font=font_btn, bg="#17A2B8", fg="white", activebackground="#138496",
            relief="flat", padx=10, pady=7, cursor="hand2",
            command=self.on_slk_to_sm
        )
        btn_slk2sm.pack(fill="x", pady=5)

        btn_help = tk.Button(
            frame, text="Hướng dẫn (Help)",
            font=font_btn, bg="#6C757D", fg="white", activebackground="#5A6268",
            relief="flat", padx=10, pady=4, cursor="hand2",
            command=self.show_help
        )
        btn_help.pack(fill="x", pady=5)

        footer = tk.Label(self.root, text="Created by Wilson & Truong Ky Anh QN (TKAQN)", font=font_foot, bg="#F8F9FA", fg="#ADB5BD")
        footer.place(relx=0.5, rely=0.96, anchor="center")

    def on_sm_to_slk(self):
        fpath = filedialog.askopenfilename(
            title="Chọn file StepMania 8 cột (.sm)",
            filetypes=[("StepMania files", "*.sm"), ("All files", "*.*")]
        )
        if not fpath:
            return
        try:
            out_path = do_convert_sm_to_slk_8col(fpath)
            messagebox.showinfo(
                "Thành công",
                f"Đã chuyển đổi thành công (8 cột OTP)!\n\nĐã lưu: {os.path.basename(out_path)}"
            )
        except PermissionError:
            messagebox.showerror(
                "Lỗi",
                "Không thể lưu file! Vui lòng đóng file nếu đang mở bằng chương trình khác rồi thử lại."
            )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã có lỗi xảy ra:\n{str(e)}")

    def on_slk_to_sm(self):
        fpath = filedialog.askopenfilename(
            title="Chọn file Audition SLK (.slk)",
            filetypes=[("SLK files", "*.slk"), ("All files", "*.*")]
        )
        if not fpath:
            return

        def_title, def_music, def_bpm = detect_defaults_for_slk(fpath)
        base_dir = os.path.dirname(fpath)

        dlg = MetadataDialog8Col(self.root, def_title, def_music, def_bpm, base_dir)
        if not dlg.result:
            return

        try:
            out_path = do_convert_slk_to_sm_8col(
                fpath,
                title=dlg.result["title"],
                music_file=dlg.result["music"],
                bpm=dlg.result["bpm"]
            )
            messagebox.showinfo(
                "Thành công",
                f"Đã chuyển đổi thành công (8 cột OTP)!\n\n"
                f"Bài hát: {dlg.result['title']}\n"
                f"File nhạc: {dlg.result['music']}\n"
                f"BPM: {dlg.result['bpm']}\n\n"
                f"Đã lưu: {os.path.basename(out_path)}"
            )
        except PermissionError:
            messagebox.showerror(
                "Lỗi",
                "Không thể lưu file! Vui lòng đóng file nếu đang mở bằng chương trình khác rồi thử lại."
            )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã có lỗi xảy ra:\n{str(e)}")

    def show_help(self):
        help_text = (
            "Audition SM ⇄ SLK Converter (Phiên bản 8 Cột - OTP)\n\n"
            "Chức năng:\n"
            "1. SM → SLK (8 cột):\n"
            "   - Trong Arrow Vortex, chọn kiểu chart 'dance-couple' hoặc 'dance-otp'.\n"
            "   - Player: 0 (n), 1 (c), 2 (s)\n"
            "   - NPC:    3 (n), 4 (c), 5 (s)\n"
            "   - Khác:   6 (d), 7 (r)\n"
            "   - File xuất ra có tiền tố '12P_<tên_bài>.slk'.\n\n"
            "2. SLK → SM (8 cột):\n"
            "   - Cho phép điền/chọn file nhạc (.ogg) và tốc độ BPM chuẩn xác.\n"
            "   - Xuất ra file '<tên_bài>.sm' chuẩn Audition OTP.\n\n"
            "Tác giả: Wilson & Trương Kỳ Anh QN (TKAQN)"
        )
        messagebox.showinfo("Hướng dẫn sử dụng", help_text)


def main():
    if len(sys.argv) > 1:
        inp = sys.argv[1]
        if not os.path.exists(inp):
            print(f"File not found: {inp}")
            sys.exit(1)
        ext = os.path.splitext(inp)[1].lower()
        if ext == ".sm":
            out_p = do_convert_sm_to_slk_8col(inp)
            print(f"Converted {inp} -> {out_p} (8 columns)")
        elif ext == ".slk":
            def_title, def_music, def_bpm = detect_defaults_for_slk(inp)
            bpm_arg = sys.argv[2] if len(sys.argv) > 2 else def_bpm
            music_arg = sys.argv[3] if len(sys.argv) > 3 else def_music
            title_arg = sys.argv[4] if len(sys.argv) > 4 else def_title
            out_p = do_convert_slk_to_sm_8col(inp, title=title_arg, music_file=music_arg, bpm=bpm_arg)
            print(f"Converted {inp} -> {out_p} (8 columns, BPM: {bpm_arg}, Music: {music_arg})")
        else:
            print(f"Unsupported file extension: {ext}")
            sys.exit(1)
    else:
        root = tk.Tk()
        app = SM2SLK8ColApp(root)
        root.mainloop()


if __name__ == "__main__":
    main()
