class Blake:
    def __init__(self, hashbitlen=256):
        self.hashbitlen = hashbitlen
        self.chain = {}
        self.count = 0
        self.Init()

    def Init(self):
        if ((self.hashbitlen == 224) or (self.hashbitlen == 256)):
            if (self.hashbitlen == 224):
                self.chain = {
                  0xC1059ED8, 0x367CD507,
                  0x3070DD17, 0xF70E5939,
                  0xFFC00B31, 0x68581511,
                  0x64F98FA7, 0xBEFA4FA4
                }
            else:
                self.chain = {0x6A09E667, 0xBB67AE85,
                  0x3C6EF372, 0xA54FF53A,
                  0x510E527F, 0x9B05688C,
                  0x1F83D9AB, 0x5BE0CD19}

        elif ((self.hashbitlen == 384) or (self.hashbitlen == 512)):
            if (self.hashbitlen == 384):
                self.chain = {0xCBBB9D5DC1059ED8, 0x629A292A367CD507,
                      0x9159015A3070DD17, 0x152FECD8F70E5939,
                      0x67332667FFC00B31, 0x8EB44A8768581511,
                      0xDB0C2E0D64F98FA7, 0x47B5481DBEFA4FA4}
            else:
                self.chain = {0x6A09E667F3BCC908, 0xBB67AE8584CAA73B,
                      0x3C6EF372FE94F82B, 0xA54FF53A5F1D36F1,
                      0x510E527FADE682D1, 0x9B05688C2B3E6C1F,
                      0x1F83D9ABFB41BD6B, 0x5BE0CD19137E2179}
        else:
            raise ValueError("Invalid hashbitlen")

    def Hash(self, data):
        self.data = data

if __name__ == '__main__':
    blake = Blake(67)
