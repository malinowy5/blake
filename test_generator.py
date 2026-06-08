from main import Blake

def generate_kat():
    with open("kat_py.txt", "w") as f:
        # Same sequence as in the c code
        msg = bytes([i % 256 for i in range(130)])
        
        for length in range(130):
            test_msg = msg[:length]
            
            result = Blake(256).Hash(test_msg)
            
            f.write(f"Len = {length * 8}\n")
            f.write(f"Msg = {test_msg.hex().upper() if length > 0 else '00'}\n")
            f.write(f"MD = {result.upper()}\n\n")
            
    print("kat_py.txt generated.")

def generate_mct():
    with open("mct_py.txt", "w") as f:
        seed = b"\x00" * 32
        f.write(f"Seed = {seed.hex().upper()}\n\n")
        
        for j in range(100):
            MD = [seed, seed, seed]
            
            for i in range(3, 1003):
                message = MD[i-3] + MD[i-2] + MD[i-1]
                
                new_hash_hex = Blake(256).Hash(message)
                MD.append(bytes.fromhex(new_hash_hex))
            
            checkpoint = MD[1002]
            f.write(f"COUNT = {j}\n")
            f.write(f"MD = {checkpoint.hex().upper()}\n\n")
            
            seed = checkpoint
            
    print("mct_py.txt generated.")

if __name__ == '__main__':
    generate_kat()
    generate_mct()