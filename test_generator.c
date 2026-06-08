#include <stdio.h>
#include <stdint.h>
#include <string.h>

void blake256_hash(uint8_t *out, const uint8_t *in, uint64_t inlen);

void generate_kat() {
    FILE *f = fopen("kat_c.txt", "w");
    uint8_t msg[130];
    uint8_t out[32];
    
    for(int i = 0; i < 130; i++) {
        msg[i] = (uint8_t)i;
    }

    for(int len = 0; len <= 129; len++) {
        blake256_hash(out, msg, len);
        
        fprintf(f, "Len = %d\n", len * 8);
        fprintf(f, "Msg = ");
        if (len == 0) {
            fprintf(f, "00");
        } else {
            for(int i = 0; i < len; i++) {
                fprintf(f, "%02X", msg[i]);
            }
        }
        fprintf(f, "\nMD = ");
        for(int i = 0; i < 32; i++) {
            fprintf(f, "%02X", out[i]);
        }
        fprintf(f, "\n\n");
    }
    fclose(f);
    printf("kat_c.txt generated.\n");
}

void generate_mct() {
    FILE *f = fopen("mct_c.txt", "w");
    uint8_t MD[1003][32];
    uint8_t seed[32];
    
    memset(seed, 0, 32);

    fprintf(f, "Seed = ");
    for(int i = 0; i < 32; i++) fprintf(f, "%02X", seed[i]);
    fprintf(f, "\n\n");

    for(int j = 0; j < 100; j++) {
        memcpy(MD[0], seed, 32);
        memcpy(MD[1], seed, 32);
        memcpy(MD[2], seed, 32);

        for(int i = 3; i < 1003; i++) {
            uint8_t message[96];
            memcpy(message, MD[i-3], 32);
            memcpy(message + 32, MD[i-2], 32);
            memcpy(message + 64, MD[i-1], 32);
            
            blake256_hash(MD[i], message, 96);
        }

        memcpy(seed, MD[1002], 32);
        fprintf(f, "COUNT = %d\n", j);
        fprintf(f, "MD = ");
        for(int i = 0; i < 32; i++) fprintf(f, "%02X", seed[i]);
        fprintf(f, "\n\n");
    }
    fclose(f);
    printf("mct_c.txt generated.\n");
}

int main() {
    generate_kat();
    generate_mct();
    return 0;
}