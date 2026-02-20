# Solução final simplificada
import math

ciphertext_hex = "4a8766a085e6f6f08be35790d399cd752b82cf63911340685bda3ad84a682ffb80cb69a57ba695a94177d6503f213079168a1cd5c3f4df393e3b6ffe37f7e8287a38bb1e9202f95a6801be80285ebc656bacc2b"
c = int(ciphertext_hex, 16)
def integer_cube_root(n):
    low = 0
    high = 1
    while high ** 3 < n:
        high *= 2
    
    while low <= high:
        mid = (low + high) // 2
        mid_cubed = mid ** 3
        
        if mid_cubed < n:
            low = mid + 1
        elif mid_cubed > n:
            high = mid - 1
        else:
            return mid
    
    return None


m = integer_cube_root(c)


byte_length = (m.bit_length() + 7) // 8
message_bytes = m.to_bytes(byte_length, 'big')

print(f"hex: {message_bytes.hex()}")
    
plaintext = message_bytes.decode('ascii')
print(f"ASCII: '{plaintext}'")
  