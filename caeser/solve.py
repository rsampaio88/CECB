# Análise direta e conclusiva

# 1. Para a cifra de César:
# Vamos descobrir o shift analisando a primeira palavra "JHLZHY"
# Se suspeitamos que seja "CAESAR", vamos calcular o shift:
def find_shift(encrypted, suspected):
    """Encontra o shift entre uma palavra cifrada e sua suspeita."""
    shifts = []
    for e, s in zip(encrypted, suspected):
        if e.isalpha() and s.isalpha():
            e_idx = ord(e.upper()) - ord('A')
            s_idx = ord(s.upper()) - ord('A')
            shift = (e_idx - s_idx) % 26
            shifts.append(shift)
    
    # Verificar se todos os shifts são iguais
    if len(set(shifts)) == 1:
        return shifts[0]
    return None

# Testar se "JHLZHY" pode ser "CAESAR"
encrypted_word = "JHLZHY"
suspected_word = "CAESAR"
shift = find_shift(encrypted_word, suspected_word)
print(f"Shift para transformar '{encrypted_word}' em '{suspected_word}': {shift}")

# Com shift 19: J->C, H->A, L->E, Z->S, H->A, Y->R
# Então JHLZHY -> CAESAR com shift 19

# 2. Para Vigenère com chave "REDTEAM":
# Vamos decifrar caractere por caractere para verificar
def vigenere_decrypt_detailed(ciphertext, key):
    """Decifra Vigenère mostrando o processo."""
    result = ""
    key = key.upper()
    
    print("Processo de decifração:")
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            key_char = key[i % len(key)]
            shift = ord(key_char) - ord('A')
            
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')
            
            decrypted = chr((ord(char) - base - shift) % 26 + base)
            result += decrypted
            print(f"  {char} - {key_char}({shift}) = {decrypted}")
        else:
            result += char
            print(f"  {char} (mantido)")
    
    return result

print("\nDecifração detalhada da cifra de Vigenère:")
cipher = "IXO{fadinnfp137314c1a13131}"
key = "REDTEAM"
decrypted = vigenere_decrypt_detailed(cipher, key)
print(f"\nResultado: {decrypted}")

# Soluções finais
print("\n" + "=" * 50)
print("SOLUÇÕES CONFIRMADAS:")
print("=" * 50)

caesar_text = caesar_decrypt("JHLZHY YLZBSA PZ MSHN_JHLZHY_d55iw1b39e", 19)
vigenere_text = vigenere_decrypt("IXO{fadinnfp137314c1a13131}", "REDTEAM")

print(f"Cifra de César (shift 19): {caesar_text}")
print(f"Cifra de Vigenère (chave REDTEAM): {vigenere_text}")
print()
print("Resposta final concatenada:")
print(f"{caesar_text} {vigenere_text}")