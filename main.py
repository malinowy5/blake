import numpy as np

class Blake:
    def __init__(self, hashbitlen=256, salt=0x0000000000000000000000000000000000000000000000000000000000000000):
        self.hashbitlen = hashbitlen
        self.count = 0x0
        self.salt = salt
        self.perm = np.array([
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
        ])
        self.Init()

    def Init(self):
        # 224- and 256-bit versions (32-bit words)
        if ((self.hashbitlen == 224) or (self.hashbitlen == 256)):
            # IVs
            if (self.hashbitlen == 224):
                self.hash = np.array([
                  0xC1059ED8, 0x367CD507,
                  0x3070DD17, 0xF70E5939,
                  0xFFC00B31, 0x68581511,
                  0x64F98FA7, 0xBEFA4FA4
                ])
            else:
                self.hash = np.array([
                  0x6A09E667, 0xBB67AE85,
                  0x3C6EF372, 0xA54FF53A,
                  0x510E527F, 0x9B05688C,
                  0x1F83D9AB, 0x5BE0CD19])
            # constants for 32-bit word
            self.c = np.array([
                0x243F6A88, 0x85A308D3,
                0x13198A2E, 0x03707344,
                0xA4093822, 0x299F31D0,
                0x082EFA98, 0xEC4E6C89,
                0x452821E6, 0x38D01377,
                0xBE5466CF, 0x34E90C6C,
                0xC0AC29B7, 0xC97C50DD,
                0x3F84D5B5, 0xB5470917
            ])
        # 384- and 512-bit versions (64-bit words)
        elif ((self.hashbitlen == 384) or (self.hashbitlen == 512)):
            # IVs
            if (self.hashbitlen == 384):
                self.hash = np.array([
                      0xCBBB9D5DC1059ED8, 0x629A292A367CD507,
                      0x9159015A3070DD17, 0x152FECD8F70E5939,
                      0x67332667FFC00B31, 0x8EB44A8768581511,
                      0xDB0C2E0D64F98FA7, 0x47B5481DBEFA4FA4])
            else:
                self.hash = np.array([
                      0x6A09E667F3BCC908, 0xBB67AE8584CAA73B,
                      0x3C6EF372FE94F82B, 0xA54FF53A5F1D36F1,
                      0x510E527FADE682D1, 0x9B05688C2B3E6C1F,
                      0x1F83D9ABFB41BD6B, 0x5BE0CD19137E21790])
            # constants for 64-bit word
            self.c = np.array([
                0x243F6A8885A308D3, 0x13198A2E03707344,
                0xA4093822299F31D0, 0x082EFA98EC4E6C89,
                0x452821E638D01377, 0xBE5466CF34E90C6C,
                0xC0AC29B7C97C50DD, 0x3F84D5B5B5470917,
                0x9216D5D98979FB1B, 0xD1310BA698DFB5AC,
                0x2FFD72DBD01ADFB7, 0xB8E1AFED6A267E96,
                0xBA7C9045F12C7F99, 0x24A19947B3916CF7,
                0x0801F2E2858EFC16, 0x636920D871574E69
            ])
        else:
            raise ValueError("Invalid hashbitlen")

    def Update(self):
        self.block = 0

        salt_0 = self.sub_bytes(self.salt, 0, 4)
        salt_1 = self.sub_bytes(self.salt, 4, 8)
        salt_2 = self.sub_bytes(self.salt, 8, 16)
        salt_3 = self.sub_bytes(self.salt, 16, 32)

        while int(self.block * self.hashbitlen / 8) <= self.data_len:
            self.count += 512
            t_0 = self.sub_bytes(self.count, 0, 4)
            t_1 = self.sub_bytes(self.count, 4, 8)

            self.m = np.empty(16)

            for i in range(16):
                self.m[i] = self.sub_bytes(self.data, int(self.block*self.hashbitlen/8)+i*4, int(self.block*self.hashbitlen/8)+(i+1)*4)

            self.hash = np.array([
                self.hash[0], self.hash[1], self.hash[2], self.hash[3],
                self.hash[4], self.hash[5], self.hash[6], self.hash[7],
                salt_0 ^ self.c[0], salt_1 ^ self.c[1], salt_2 ^ self.c[2], salt_3 ^ self.c[3],
                t_0 ^ self.c[4], t_0 ^ self.c[5], t_1 ^ self.c[6], t_1 ^ self.c[7]
            ])
            self.block += 1
            break

    def Hash(self, data):
        self.data_len = len(data)
        self.data = int.from_bytes(data.encode("utf-8"), byteorder='big')
        print(self.data)
        self.Update()

    def G(self, a, b, c, d, i):
        def rot(n, rotations, width=32):
            return (2 ** width - 1) & (n >> rotations | n << (width - rotations))

        self.hash[a] = (self.hash[a] + self.hash[b] + (self.m[self.perm[2 * i]] ^ self.c[self.perm[2 * i + 1]])) & 0xFFFFFFFF
        self.hash[d] = rot(self.hash[d] ^ self.hash[a], 16)
        self.hash[c] = (self.hash[c] + self.hash[d]) & 0xFFFFFFFF
        self.hash[b] = rot(self.hash[b] ^ self.hash[c], 12)

        self.hash[a] = (self.hash[a] + self.hash[b] + (self.m[self.perm[2 * i + 1]] ^ self.c[self.perm[2 * i]])) & 0xFFFFFFFF
        self.hash[d] = rot(self.hash[d] ^ self.hash[a], 8)
        self.hash[c] = (self.hash[c] + self.hash[d]) & 0xFFFFFFFF
        self.hash[b] = rot(self.hash[b] ^ self.hash[c], 7)


    def sub_bytes(self, i, start=0, end=0):
        i_str = hex(i)[2:]
        if len(i_str) < end * 2:i_str = i_str.zfill(end * 2)
        i_sub = i_str[-end * 2: len(i_str) - start * 2] if end > 0 else i_str[:len(i_str) - start * 2]
        return int(i_sub or '0', 16)

    def __str__(self):
        format_hex = np.vectorize(lambda x: hex(x))
        hex_dane = format_hex(self.hash)
        return np.array2string(np.array(hex_dane).reshape(4, 4), separator=', ', formatter={'str_kind': lambda x: x})

if __name__ == '__main__':
    blake = Blake(256)
    blake.Hash("abcde")
