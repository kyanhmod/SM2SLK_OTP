# SM2SLK_OTP
Source code to convert .sm file type to .slk file for One-Two Party mode of Audition Dance Online game.

1. Structure of sm file this tool support:
    In Arrow Vortex select dance-couple when creating a sm.
   
    Layout keys (thanks nongginga :D):
    
    player | npc | other data
   
    1 n    | 4 n | 7 d
   
    2 c    | 5 c | 8 r
   
    3 s    | 6 s |
    
   n: note;
   c: change;
   s: space (ingame that will be "go!" or "yeah!");
   d: dance;
   r: reset;
   
   n, c, s, d, r are in the slk and are already decrypted
   
3. How to using this tool?
    Download .py file, run cmd at place you put this tool, type py sm2slkOTP.py, select file and you already have slk file for One-Two Party mode.

Special thanks to RT and nongginga
