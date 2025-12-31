p = 313358211674631157072171768972715667299
q = 313358211674631157072171768972715667353
e = 65537

# ciphertext em hex
c_hex = "8aa19e1eb0360830c4292d2e724e1bee234fed1186b18c638c2928feb99dca68"

# módulo
n = p * q

# phi de n
phi = (p - 1) * (q - 1)

# inverso modular de e
d = pow(e, -1, phi)

# converter ciphertext para inteiro
c = int(c_hex, 16)

# desencriptação RSA
m = pow(c, d, n)

# converter para ASCII
plaintext = m.to_bytes((m.bit_length() + 7) // 8, byteorder="big")

print(plaintext.decode())
