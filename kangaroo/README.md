# kangaroo
Find PrivateKey of corresponding Pubkey(s) using Pollard Kangaroo algo 

# Usage for GUI
- python kangui.py
- 
![image](https://github.com/Mizogg/kangaroo/assets/88630056/4cee328d-ea9e-442a-8ac9-089335c845c2)

# Usage
- python kangaroo.py

- Public key for puzzle 160 = 02e0a8b039282faf6fe0fd769cfbc4b6b4cf8758ba68220eac420e32b91ddfa673
- Range for puzzle 160  = 8000000000000000000000000000000000000000:ffffffffffffffffffffffffffffffffffffffff
```
(base) C:\anaconda3>python kangaroo.py
[+] Starting CPU Kangaroo.... Please Wait
[+] Working on Pubkey: 0452b1af31d67e6a83ec7931c148f56b0755ce40c836f20c6fe2b6da612c89cf3e2d22dceb73a2648739bfc45c9a305e385a5c1fbeea35a8f946fd78c9fc67a615
[+] Using  [Number of CPU Threads: 7] [DP size: 10] [MaxStep: 1]
[+] ............................................
[+] Scanning Range  0x935da71d7350734c3472fe305fef82ab8aca644fb : 0x935da71d7350734c3472fe305fff82ab8aca644fa
[+] [646.03 TeraKeys/s][Kang 7168][Count 2^27.34/2^29.07][Elapsed 09s][Dead 0][RAM 19.8MB/44.9MB]
============== KEYFOUND ==============
Kangaroo FOUND PrivateKey : 0x00000000000000000000000935da71d7350734c3472fe305fef82ab8aca644fb
======================================
Program Finished
```
