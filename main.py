class Blake:
    def __init__(self, hashbitlen=256, salt=0x0000000000000000000000000000000000000000000000000000000000000000):
        self.hash_bit_len = hashbitlen
        self.arch = 32 if self.hash_bit_len <= 256 else 64
        self.mask = 0xFFFFFFFF if self.arch == 32 else 0xFFFFFFFFFFFFFFFF
        self.block_size = 64 if self.arch == 32 else 128
        
        self.salt = salt
        self.count = 0x0
        self.buffer = bytearray()
        self.nullt = False # For padding blocks with no data
        
        self.perm = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],
            [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],
            [7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8],
            [9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13],
            [2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9],
            [12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11],
            [13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10],
            [6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5],
            [10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],
            [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],
            [7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8],
            [9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13],
            [2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9],
            [12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11],
            [13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10],
            [6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5],
            [10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0]
        ]
        self.Init()

    # Set up initial values and constants
    def Init(self):
        # 224- and 256-bit versions (32-bit words)
        if self.hash_bit_len == 224 or self.hash_bit_len == 256:
            # IVs
            if self.hash_bit_len == 224:
                self.hash = [
                    0xC1059ED8, 0x367CD507, 
                    0x3070DD17, 0xF70E5939,
                    0xFFC00B31, 0x68581511, 
                    0x64F98FA7, 0xBEFA4FA4
                    ]
            else:
                self.hash = [
                    0x6A09E667, 0xBB67AE85, 
                    0x3C6EF372, 0xA54FF53A,
                    0x510E527F, 0x9B05688C, 
                    0x1F83D9AB, 0x5BE0CD19
                    ]
            # constants for 32-bit word
            self.c = [
                0x243F6A88, 0x85A308D3, 
                0x13198A2E, 0x03707344,
                0xA4093822, 0x299F31D0, 
                0x082EFA98, 0xEC4E6C89,
                0x452821E6, 0x38D01377, 
                0xBE5466CF, 0x34E90C6C,
                0xC0AC29B7, 0xC97C50DD, 
                0x3F84D5B5, 0xB5470917
                ]
        # 384- and 512-bit versions (64-bit words)
        elif self.hash_bit_len == 384 or self.hash_bit_len == 512:
            # IVs
            if self.hash_bit_len == 384:
                self.hash = [
                    0xCBBB9D5DC1059ED8, 0x629A292A367CD507,
                    0x9159015A3070DD17, 0x152FECD8F70E5939,
                    0x67332667FFC00B31, 0x8EB44A8768581511,
                    0xDB0C2E0D64F98FA7, 0x47B5481DBEFA4FA4]
            else:
                self.hash = [
                    0x6A09E667F3BCC908, 0xBB67AE8584CAA73B,
                    0x3C6EF372FE94F82B, 0xA54FF53A5F1D36F1,
                    0x510E527FADE682D1, 0x9B05688C2B3E6C1F,
                    0x1F83D9ABFB41BD6B, 0x5BE0CD19137E2179]
            # constants for 64-bit word
            self.c = [
                0x243F6A8885A308D3, 0x13198A2E03707344, 
                0xA4093822299F31D0, 0x082EFA98EC4E6C89,
                0x452821E638D01377, 0xBE5466CF34E90C6C, 
                0xC0AC29B7C97C50DD, 0x3F84D5B5B5470917,
                0x9216D5D98979FB1B, 0xD1310BA698DFB5AC, 
                0x2FFD72DBD01ADFB7, 0xB8E1AFED6A267E96,
                0xBA7C9045F12C7F99, 0x24A19947B3916CF7, 
                0x0801F2E2858EFC16, 0x636920D871574E69]
        else:
            raise ValueError("Invalid hashbitlen")

    # Buffers data and sends blocks through compress()
    def Update(self, data: bytes):
        self.buffer.extend(data)
        
        while len(self.buffer) >= self.block_size:
            block = self.buffer[:self.block_size]
            self.buffer = self.buffer[self.block_size:]
            self.count += self.block_size * 8
            self.compress(block)

    # The actual hash function for a block
    def compress(self, block):
        word_size = 4 if self.arch == 32 else 8
        shift = 32 if self.arch == 32 else 64
        
        self.m = [0] * 16
        for i in range(16):
            self.m[i] = int.from_bytes(block[i * word_size : (i + 1) * word_size], byteorder='big')

        salt_0 = (self.salt >> (shift * 3)) & self.mask
        salt_1 = (self.salt >> (shift * 2)) & self.mask
        salt_2 = (self.salt >> shift) & self.mask
        salt_3 = self.salt & self.mask
        
        # If nullt is true, we act like the counter is 0 for this padding block
        t_0 = (self.count & self.mask) if not self.nullt else 0
        t_1 = ((self.count >> shift) & self.mask) if not self.nullt else 0

        v = [
            self.hash[0], self.hash[1], self.hash[2], self.hash[3],
            self.hash[4], self.hash[5], self.hash[6], self.hash[7],
            salt_0 ^ self.c[0], salt_1 ^ self.c[1], salt_2 ^ self.c[2], salt_3 ^ self.c[3],
            t_0 ^ self.c[4], t_0 ^ self.c[5], t_1 ^ self.c[6], t_1 ^ self.c[7]
        ]

        rounds = 14 if self.arch == 32 else 16 # Updated round counts
        for r in range(rounds):
            self.G(v, 0, 4, 8, 12, 0, r)
            self.G(v, 1, 5, 9, 13, 1, r)
            self.G(v, 2, 6, 10, 14, 2, r)
            self.G(v, 3, 7, 11, 15, 3, r)
            self.G(v, 0, 5, 10, 15, 4, r)
            self.G(v, 1, 6, 11, 12, 5, r)
            self.G(v, 2, 7, 8, 13, 6, r)
            self.G(v, 3, 4, 9, 14, 7, r)

        self.hash[0] ^= v[0] ^ v[8] ^ salt_0
        self.hash[1] ^= v[1] ^ v[9] ^ salt_1
        self.hash[2] ^= v[2] ^ v[10] ^ salt_2
        self.hash[3] ^= v[3] ^ v[11] ^ salt_3
        self.hash[4] ^= v[4] ^ v[12] ^ salt_0
        self.hash[5] ^= v[5] ^ v[13] ^ salt_1
        self.hash[6] ^= v[6] ^ v[14] ^ salt_2
        self.hash[7] ^= v[7] ^ v[15] ^ salt_3

    # Does padding on the remaining data, hashes and returns the final hash
    def Final(self):
        total_bits = self.count + len(self.buffer) * 8
        self.count = total_bits
        
        msg_bytes_left = len(self.buffer)
        
        #'1' bit (0x80)
        self.buffer.append(0x80)
        
        length_size = 8 if self.arch == 32 else 16
        pad_len = self.block_size - (len(self.buffer) + length_size)
        
        if pad_len < 0:
            # Not enough space for length, pad out this block, make a new one
            pad_len += self.block_size
            
        self.buffer.extend(bytearray(pad_len))
        
        # Add the final marker before the length
        if self.hash_bit_len in (256, 512):
            self.buffer[-1] ^= 0x01
        
        self.buffer.extend(total_bits.to_bytes(length_size, byteorder='big'))
        
        # Compress the remaining block(s)
        while len(self.buffer) >= self.block_size:
            block = self.buffer[:self.block_size]
            self.buffer = self.buffer[self.block_size:]
            
            if msg_bytes_left <= 0:
                self.nullt = True
                
            self.compress(block)
            
            msg_bytes_left -= self.block_size

        word_size = 4 if self.arch == 32 else 8
        result_bytes = b"".join(h.to_bytes(word_size, byteorder='big') for h in self.hash)
        
        # Truncate if using 224 or 384
        return result_bytes[:self.hash_bit_len // 8].hex()

    # Helper function for hashing small amounts of data
    def Hash(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.Update(data)
        return self.Final()

    def G(self, v, a, b, c, d, i, r):
        def rot(n, rotations):
            return self.mask & ((n >> rotations) | (n << (self.arch - rotations)))

        # Different rotations on different architectures
        r1, r2, r3, r4 = (16, 12, 8, 7) if self.arch == 32 else (32, 25, 16, 11)

        v[a] = (v[a] + v[b] + (self.m[self.perm[r][2 * i]] ^ self.c[self.perm[r][2 * i + 1]])) & self.mask
        v[d] = rot(v[d] ^ v[a], r1)
        v[c] = (v[c] + v[d]) & self.mask
        v[b] = rot(v[b] ^ v[c], r2)

        v[a] = (v[a] + v[b] + (self.m[self.perm[r][2 * i + 1]] ^ self.c[self.perm[r][2 * i]])) & self.mask
        v[d] = rot(v[d] ^ v[a], r3)
        v[c] = (v[c] + v[d]) & self.mask
        v[b] = rot(v[b] ^ v[c], r4)

if __name__ == '__main__':
    blake = Blake(384)
    result = blake.Hash("The quick brown fox jumps over the lazy dog")
    print(f"Hash: {result}")