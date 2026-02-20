# Solução usando otimização matemática
import math

p = 1222023965506290853
g = 5
A = 528522703702450282
B = 566132874237330265

def discrete_log(g, h, p, max_n):
    # x  g^x ≡ h (mod p) 
    m = int(math.isqrt(max_n)) + 1

    baby_steps = {}
    gj = 1
    for j in range(m):
        baby_steps[gj] = j
        gj = (gj * g) % p
    
    gm_inv = pow(g, -m, p)  # g^(-m) mod p
    
    gamma = h
    for i in range(m):
        if gamma in baby_steps:
            j = baby_steps[gamma]
            x = i * m + j
            if x <= max_n:
                return x
        gamma = (gamma * gm_inv) % p
    
    return None

a = discrete_log(g, A, p, 2**22)
print(f"a = {a}")

b = discrete_log(g, B, p, 2**22)
print(f"b = {b}")


secret1 = pow(A, b, p)
secret2 = pow(B, a, p)
    
print(f"A^b mod p = {secret1}")
print(f"B^a mod p = {secret2}")
    
if secret1 == secret2:
    print(f"match")
    print(f"flag : {secret1}")
