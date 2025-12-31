# Solução usando otimização matemática
import math

p = 1222023965506290853
g = 5
A = 528522703702450282
B = 566132874237330265

# Usaremos o algoritmo baby-step giant-step que é O(sqrt(n))
# em vez de O(n) da força bruta

def discrete_log(g, h, p, max_n):
    """Encontra x tal que g^x ≡ h (mod p) usando baby-step giant-step."""
    m = int(math.isqrt(max_n)) + 1
    
    # Baby steps: calcular g^j para j = 0...m-1
    baby_steps = {}
    gj = 1
    for j in range(m):
        baby_steps[gj] = j
        gj = (gj * g) % p
    
    # Calcular g^(-m)
    gm_inv = pow(g, -m, p)  # g^(-m) mod p
    
    # Giant steps
    gamma = h
    for i in range(m):
        if gamma in baby_steps:
            j = baby_steps[gamma]
            x = i * m + j
            if x <= max_n:
                return x
        gamma = (gamma * gm_inv) % p
    
    return None

print("Usando algoritmo baby-step giant-step...")
print("Encontrando a...")
a = discrete_log(g, A, p, 2**22)
print(f"a = {a}")

print("\nEncontrando b...")
b = discrete_log(g, B, p, 2**22)
print(f"b = {b}")

if a and b:
    # Segredo compartilhado = g^(ab) mod p = A^b mod p = B^a mod p
    secret1 = pow(A, b, p)
    secret2 = pow(B, a, p)
    
    print(f"\nSegredo compartilhado:")
    print(f"A^b mod p = {secret1}")
    print(f"B^a mod p = {secret2}")
    
    if secret1 == secret2:
        print(f"✓ Segredo verificado!")
        print(f"\nRESPOSTA FINAL: {secret1}")
    else:
        print("✗ Erro: segredos diferentes")
else:
    print("Não foi possível encontrar os expoentes.")