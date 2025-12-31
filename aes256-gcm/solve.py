import binascii

# Dados fornecidos
nonce_hex = "1e246736fb2295e37f14c027"
aad_hex = ""
known_plaintext_ascii = '{"type":"notice","msg":"service status: OK"}'
ciphertext1_hex = "4f33d255154763ac46fbbf4ba940bf8311952461f59e6f85c8ea7c75fc7f58641f01ab98f9d5105df4e9b39c"
tag1_hex = "e8c230f21c0be84e7c1091053cddd204"
ciphertext2_hex = "6754e57e20761ed127d88f49ab40bd920b82337de8c4349fd8e1636aa4"
tag2_hex = "4fecdfc3f850cf709ff9aee6b8fef441"

# Converter para bytes
ciphertext1 = binascii.unhexlify(ciphertext1_hex)
ciphertext2 = binascii.unhexlify(ciphertext2_hex)
known_plaintext = known_plaintext_ascii.encode('ascii')

# Garantir que os ciphertexts têm o mesmo comprimento para a operação XOR
# Usaremos o comprimento do ciphertext2 (que é o mais curto)
min_len = min(len(ciphertext1), len(ciphertext2))

# Truncar os dados para o comprimento mínimo
ciphertext1_trunc = ciphertext1[:min_len]
ciphertext2_trunc = ciphertext2[:min_len]
known_plaintext_trunc = known_plaintext[:min_len]

# Passo 1: Recuperar o keystream usando o texto plano conhecido e ciphertext1
# C = P ⊕ keystream, então keystream = C ⊕ P
keystream = bytes([ciphertext1_trunc[i] ^ known_plaintext_trunc[i] for i in range(min_len)])

# Passo 2: Usar o keystream para recuperar o texto plano desconhecido do ciphertext2
# P2 = C2 ⊕ keystream
unknown_plaintext = bytes([ciphertext2_trunc[i] ^ keystream[i] for i in range(min_len)])

# Tentar decodificar como ASCII
try:
    unknown_plaintext_ascii = unknown_plaintext.decode('ascii')
    print("Texto plano recuperado (ASCII):")
    print(unknown_plaintext_ascii)
    
    # Mostrar também a representação hexadecimal
    print("\nTexto plano recuperado (hex):")
    print(binascii.hexlify(unknown_plaintext).decode('ascii'))
    
except UnicodeDecodeError:
    # Se não for ASCII puro, mostrar em hex
    print("Texto plano recuperado não é ASCII puro:")
    print(binascii.hexlify(unknown_plaintext).decode('ascii'))
    
    # Tentar interpretar como string com possíveis caracteres especiais
    print("\nTentativa de interpretação como string (pode conter caracteres não imprimíveis):")
    print(repr(unknown_plaintext.decode('latin-1')))

# Verificação adicional: mostrar alguns bytes do keystream para referência
print(f"\nPrimeiros 16 bytes do keystream recuperado: {binascii.hexlify(keystream[:16]).decode('ascii')}")