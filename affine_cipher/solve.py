# Solução direta e final
def mod_inverse(a, m=26):
    """Encontra o inverso multiplicativo de a mod m."""
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def affine_decrypt_simple(ciphertext, a, b):
    """Decifra usando cifra Afim."""
    a_inv = mod_inverse(a)
    if a_inv is None:
        return None
    
    result = []
    for char in ciphertext:
        if 'A' <= char <= 'Z':
            x = ord(char) - ord('A')
            y = (a_inv * (x - b)) % 26
            result.append(chr(y + ord('A')))
        else:
            result.append(char)
    return ''.join(result)

# Texto cifrado
cipher = "ATTUNK XKGYVP UG TVAC_ATTUNK_V0RUKNKTL543ZA"

print("Texto cifrado:", cipher)
print()

# Valores possíveis para a (coprimos com 26)
valid_a = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

# Para cada combinação a,b, testar
for a in valid_a:
    for b in range(26):
        plain = affine_decrypt_simple(cipher, a, b)
        if plain:
            # Verificar se faz sentido
            # Procurar por palavras comuns ou padrões
            if 'THE' in plain or 'AND' in plain or 'IS' in plain:
                print(f"a={a:2d}, b={b:2d}: {plain}")

print("\n" + "="*60)

# Vamos focar no padrão "ATTUNK" que se repete
# Se "ATTUNK" for uma palavra comum, como "AFFINE"
print("Focando no padrão 'ATTUNK' -> 'AFFINE':")
# ATTUNK em números: A=0, T=19, T=19, U=20, N=13, K=10
# AFFINE em números: A=0, F=5, F=5, I=8, N=13, E=4

# Usando A->A: (a*0 + b) mod 26 = 0 => b = 0
# Usando N->N: (a*13 + 0) mod 26 = 13 => a*13 ≡ 13 mod 26

# Com b=0, testar valores de a
print("\nTestando com b=0:")
for a in valid_a:
    plain = affine_decrypt_simple(cipher, a, 0)
    if plain:
        print(f"a={a:2d}: {plain}")

print("\n" + "="*60)

# Outra hipótese: "ATTUNK" -> "SECRET"
# SECRET: S=18, E=4, C=2, R=17, E=4, T=19
print("Testando hipótese 'ATTUNK' -> 'SECRET':")
# Sistema: 
# (a*18 + b) mod 26 = 0  (S->A)
# (a*4 + b) mod 26 = 19  (E->T)

# Resolvendo: subtraindo as equações: (a*14) mod 26 = 7
print("Resolvendo 14a ≡ 7 mod 26...")
solutions = []
for a in range(26):
    if (14 * a) % 26 == 7:
        solutions.append(a)
print(f"Valores possíveis para a: {solutions}")

for a in solutions:
    if a in valid_a:
        # b = 0 - a*18 mod 26
        b = (-a * 18) % 26
        plain = affine_decrypt_simple(cipher, a, b)
        if plain:
            print(f"a={a}, b={b}: {plain}")

print("\n" + "="*60)
print("BUSCA EXAUSTIVA COM FILTRO INTELIGENTE")

# Buscar por textos que contêm palavras-chave esperadas
keywords = ['FLAG', 'CIPHER', 'AFFINE', 'SECRET', 'MESSAGE', 'TEXT']

best_results = []
for a in valid_a:
    for b in range(26):
        plain = affine_decrypt_simple(cipher, a, b)
        if plain:
            # Verificar se parece inglês
            upper_plain = plain.upper()
            
            # Pontuação baseada em:
            score = 0
            
            # 1. Presença de palavras comuns
            common_words = ['THE', 'AND', 'IS', 'IN', 'TO', 'OF', 'A']
            for word in common_words:
                if word in upper_plain:
                    score += 10
            
            # 2. Presença de palavras-chave do desafio
            for keyword in keywords:
                if keyword in upper_plain:
                    score += 20
            
            # 3. Padrão de repetição (ATTUNK aparece 2x no cifrado)
            # Se a palavra que veio de ATTUNK aparecer 2x
            words = upper_plain.split()
            if len(words) > 0:
                first_word = words[0]
                if upper_plain.count(first_word) >= 2:
                    score += 15
            
            if score > 0:
                best_results.append((score, a, b, plain))

# Ordenar por pontuação
best_results.sort(reverse=True)

print("\nTop 5 resultados:")
for i, (score, a, b, plain) in enumerate(best_results[:5]):
    print(f"{i+1}. Score={score:3d}, a={a:2d}, b={b:2d}: {plain}")

print("\n" + "="*60)
print("ANÁLISE DO PADRÃO '_ATTUNK_'")

# No texto cifrado temos: ... TVAC_ATTUNK_ ...
# Isso provavelmente se torna: ... _AFFINE_ ou ... _CIPHER_
# O underscore é mantido, então só as letras são transformadas

# Vamos analisar "TVAC" que vem antes de "_ATTUNK_"
# Se ATTUNK -> AFFINE, então TVAC deve ser algo como "THIS" ou "WITH"

print("\nSupondo ATTUNK -> AFFINE:")
print("Testando combinações que mapeiam ATTUNK para AFFINE...")

# ATTUNK (0,19,19,20,13,10) -> AFFINE (0,5,5,8,13,4)
# Temos 6 equações. Vamos resolver para a e b.

# Das equações:
# Para A->A: (a*0 + b) mod 26 = 0 => b = 0
# Para T->F (1): (a*19 + 0) mod 26 = 5 => 19a ≡ 5 mod 26
# Para T->F (2): mesma equação
# Para U->I: (a*20 + 0) mod 26 = 8 => 20a ≡ 8 mod 26
# Para N->N: (a*13 + 0) mod 26 = 13 => 13a ≡ 13 mod 26
# Para K->E: (a*10 + 0) mod 26 = 4 => 10a ≡ 4 mod 26

# Vamos resolver 19a ≡ 5 mod 26
print("Resolvendo 19a ≡ 5 mod 26...")
solutions_19 = []
for a in range(26):
    if (19 * a) % 26 == 5:
        solutions_19.append(a)
print(f"Soluções: {solutions_19}")

# Agora verificar quais também satisfazem 13a ≡ 13 mod 26
valid_solutions = []
for a in solutions_19:
    if (13 * a) % 26 == 13:
        valid_solutions.append(a)
print(f"Soluções que também satisfazem 13a ≡ 13 mod 26: {valid_solutions}")

print("\nTestando essas soluções:")
for a in valid_solutions:
    if a in valid_a:  # a deve ser coprimo com 26
        b = 0
        plain = affine_decrypt_simple(cipher, a, b)
        if plain:
            print(f"a={a}, b={b}: {plain}")