def rail_fence_decrypt(ciphertext, rails=3):
    """
    Decifra texto usando a cifra Rail Fence.
    
    A cifra Rail Fence escreve o texto em zigue-zague através de múltiplos trilhos.
    Exemplo com 3 trilhos:
      A       E       I
        B   D   F   H
          C       G
    
    Para decifrar, precisamos reconstruir o padrão dos trilhos.
    """
    n = len(ciphertext)
    
    # Primeiro, precisamos calcular quantos caracteres vão em cada trilho
    # O padrão para 3 trilhos se repete a cada 4 caracteres (2*(rails-1))
    cycle = 2 * (rails - 1)  # Para 3 rails: 2*(3-1) = 4
    
    # Calcular tamanho de cada trilho
    full_cycles = n // cycle
    remainder = n % cycle
    
    # Distribuir caracteres nos trilhos
    rail_lengths = [0] * rails
    
    # Para cada ciclo completo
    rail_lengths[0] = full_cycles  # Primeiro trilho tem 1 caractere por ciclo
    for i in range(1, rails - 1):
        rail_lengths[i] = 2 * full_cycles  # Trilhos do meio têm 2 caracteres por ciclo
    rail_lengths[rails - 1] = full_cycles  # Último trilho tem 1 caractere por ciclo
    
    # Adicionar caracteres restantes
    for i in range(remainder):
        if i < rails:
            rail_lengths[i] += 1
        else:
            rail_lengths[2 * rails - 2 - i] += 1
    
    # Reconstruir os trilhos
    rails_text = []
    start = 0
    for length in rail_lengths:
        rails_text.append(ciphertext[start:start+length])
        start += length
    
    # Reconstruir o texto plano
    plaintext = []
    rail_ptrs = [0] * rails
    direction = 1  # 1 para baixo, -1 para cima
    current_rail = 0
    
    for i in range(n):
        plaintext.append(rails_text[current_rail][rail_ptrs[current_rail]])
        rail_ptrs[current_rail] += 1
        
        # Mover para o próximo trilho
        current_rail += direction
        
        # Mudar direção se atingir o topo ou fundo
        if current_rail == 0 or current_rail == rails - 1:
            direction = -direction
    
    return ''.join(plaintext)

def rail_fence_decrypt_manual(ciphertext, rails=3):
    """
    Outra implementação do deciframento Rail Fence.
    """
    n = len(ciphertext)
    
    # Criar matriz vazia
    fence = [['' for _ in range(n)] for _ in range(rails)]
    
    # Preencher com marcadores para o padrão
    row = 0
    col = 0
    direction = 1
    
    for i in range(n):
        fence[row][col] = '*'
        col += 1
        
        row += direction
        if row == 0 or row == rails - 1:
            direction = -direction
    
    # Preencher com o texto cifrado
    index = 0
    for r in range(rails):
        for c in range(n):
            if fence[r][c] == '*':
                fence[r][c] = ciphertext[index]
                index += 1
    
    # Ler na ordem correta
    result = []
    row = 0
    col = 0
    direction = 1
    
    for i in range(n):
        result.append(fence[row][col])
        col += 1
        
        row += direction
        if row == 0 or row == rails - 1:
            direction = -direction
    
    return ''.join(result)

def analyze_rail_fence(ciphertext):
    """
    Analisa o texto cifrado para tentar determinar o número de trilhos.
    """
    print(f"Texto cifrado: '{ciphertext}'")
    print(f"Comprimento: {len(ciphertext)} caracteres")
    print()
    
    # Tentar diferentes números de trilhos (de 2 a 10)
    print("Tentando diferentes números de trilhos:")
    for rails in range(2, 11):
        plaintext = rail_fence_decrypt(ciphertext, rails)
        
        # Avaliar se parece texto legível
        # Verificar porcentagem de caracteres alfabéticos e espaços
        alpha_count = sum(1 for c in plaintext if c.isalpha() or c.isspace() or c in '.,!?_-')
        alpha_ratio = alpha_count / len(plaintext)
        
        # Verificar se contém palavras comuns
        common_words = ['THE', 'AND', 'IS', 'IN', 'TO', 'OF', 'A', 'THAT', 'IT']
        upper_plain = plaintext.upper()
        word_score = sum(1 for word in common_words if word in upper_plain)
        
        print(f"  Rails={rails}: {plaintext[:50]}... (alpha={alpha_ratio:.2f}, words={word_score})")

# Texto cifrado fornecido
ciphertext = "R CET GINcq5uALFNERSL SFA_ALEC_llu1zlznIE UILRFEtefu"

print("DESAFIO: CIFRA RAIL FENCE (3 RAILS)")
print("=" * 70)

# Primeiro, vamos limpar e analisar o texto
print(f"Texto cifrado original: '{ciphertext}'")
print(f"Comprimento: {len(ciphertext)} caracteres")
print()

# Remover espaços? Não, espaços podem ser parte da mensagem
# Vamos manter tudo como está

# Método 1: Usando função de deciframento
print("Método 1: Deciframento direto com 3 rails")
plaintext1 = rail_fence_decrypt(ciphertext, 3)
print(f"Resultado: '{plaintext1}'")
print()

# Método 2: Usando implementação alternativa
print("Método 2: Implementação alternativa")
plaintext2 = rail_fence_decrypt_manual(ciphertext, 3)
print(f"Resultado: '{plaintext2}'")
print()

# Verificar se os métodos produzem o mesmo resultado
if plaintext1 == plaintext2:
    print("✓ Ambos os métodos produzem o mesmo resultado")
else:
    print("✗ Os métodos produzem resultados diferentes")
    print(f"  Método 1: '{plaintext1}'")
    print(f"  Método 2: '{plaintext2}'")

# Análise do resultado
print("\n" + "=" * 70)
print("ANÁLISE DO TEXTO DECIFRADO")
print("=" * 70)

print(f"Texto decifrado: '{plaintext1}'")
print()

# Verificar características
print("Características do texto decifrado:")
print(f"  - Comprimento: {len(plaintext1)} caracteres")
print(f"  - Letras maiúsculas: {sum(1 for c in plaintext1 if c.isupper())}")
print(f"  - Letras minúsculas: {sum(1 for c in plaintext1 if c.islower())}")
print(f"  - Dígitos: {sum(1 for c in plaintext1 if c.isdigit())}")
print(f"  - Espaços: {sum(1 for c in plaintext1 if c.isspace())}")
print(f"  - Caracteres especiais: {sum(1 for c in plaintext1 if not (c.isalnum() or c.isspace()))}")
print()

# Tentar identificar padrões ou palavras
print("Palavras identificadas:")
words = plaintext1.split()
for word in words:
    # Verificar se a palavra parece ser uma palavra em inglês
    alpha_only = ''.join(c for c in word if c.isalpha())
    if len(alpha_only) >= 3:
        print(f"  '{word}'")

# Vamos tentar diferentes interpretações
# Talvez o texto precise ser limpo ou processado de forma diferente
print("\n" + "=" * 70)
print("TENTATIVAS ADICIONAIS")
print("=" * 70)

# Tentativa 1: Remover todos os espaços primeiro, depois decifrar
print("Tentativa 1: Remover espaços antes de decifrar")
cipher_no_spaces = ''.join(c for c in ciphertext if not c.isspace())
plaintext_no_spaces = rail_fence_decrypt(cipher_no_spaces, 3)
print(f"Cifrado sem espaços: '{cipher_no_spaces}'")
print(f"Decifrado sem espaços: '{plaintext_no_spaces}'")
print()

# Tentativa 2: Converter tudo para maiúsculas primeiro
print("Tentativa 2: Converter para maiúsculas antes de decifrar")
cipher_upper = ciphertext.upper()
plaintext_upper = rail_fence_decrypt(cipher_upper, 3)
print(f"Cifrado em maiúsculas: '{cipher_upper}'")
print(f"Decifrado em maiúsculas: '{plaintext_upper}'")
print()

# Tentativa 3: Tentar com 2 ou 4 rails para ver se faz mais sentido
print("Tentativa 3: Testar com número diferente de rails")
for rails in [2, 4, 5]:
    plaintext_test = rail_fence_decrypt(ciphertext, rails)
    print(f"  Rails={rails}: '{plaintext_test[:60]}...'")
print()

# Vamos analisar visualmente o padrão de Rail Fence
print("=" * 70)
print("ANÁLISE VISUAL DO PADRÃO RAIL FENCE")
print("=" * 70)

# Mostrar como o texto seria distribuído nos trilhos
def visualize_rail_fence(text, rails=3):
    """Visualiza o padrão Rail Fence."""
    n = len(text)
    # Criar matriz
    fence = [['.' for _ in range(n)] for _ in range(rails)]
    
    # Preencher padrão
    row = 0
    direction = 1
    for col in range(n):
        fence[row][col] = text[col]
        row += direction
        if row == 0 or row == rails - 1:
            direction = -direction
    
    # Imprimir
    for r in range(rails):
        print(f"Trilho {r}: ", end="")
        for c in range(n):
            print(f"{fence[r][c]} ", end="")
        print()

print("\nVisualização do padrão com o texto cifrado:")
visualize_rail_fence(ciphertext, 3)

print("\n" + "=" * 70)
print("DECIFRAMENTO PASSO A PASSO")
print("=" * 70)

# Vamos fazer o deciframento passo a passo manualmente
print("\nPasso 1: Calcular comprimentos dos trilhos")
n = len(ciphertext)
rails = 3
cycle = 2 * (rails - 1)  # 4

full_cycles = n // cycle  # ciclos completos
remainder = n % cycle     # caracteres restantes

print(f"  Comprimento total: {n}")
print(f"  Ciclo (padrão que se repete): {cycle} caracteres")
print(f"  Ciclos completos: {full_cycles}")
print(f"  Caracteres restantes: {remainder}")
print()

# Calcular quantos caracteres em cada trilho
rail_counts = [0] * rails
rail_counts[0] = full_cycles  # Primeiro trilho: 1 por ciclo
rail_counts[1] = 2 * full_cycles  # Segundo trilho: 2 por ciclo  
rail_counts[2] = full_cycles  # Terceiro trilho: 1 por ciclo

# Adicionar restantes
for i in range(remainder):
    if i < rails:
        rail_counts[i] += 1
    else:
        rail_counts[2 * rails - 2 - i] += 1

print(f"  Caracteres por trilho: {rail_counts}")
print()

# Separar o texto cifrado nos trilhos
print("Passo 2: Separar texto cifrado nos trilhos")
start = 0
rail_texts = []
for i, count in enumerate(rail_counts):
    rail_text = ciphertext[start:start+count]
    rail_texts.append(rail_text)
    print(f"  Trilho {i}: '{rail_text}' ({count} caracteres)")
    start += count
print()

# Reconstruir texto plano
print("Passo 3: Reconstruir texto plano")
plaintext_chars = []
rail_pointers = [0, 0, 0]
direction = 1  # 1 = para baixo, -1 = para cima
current_rail = 0

for i in range(n):
    plaintext_chars.append(rail_texts[current_rail][rail_pointers[current_rail]])
    rail_pointers[current_rail] += 1
    
    # Mover para próximo trilho
    current_rail += direction
    
    # Inverter direção se necessário
    if current_rail == 0 or current_rail == rails - 1:
        direction = -direction

result = ''.join(plaintext_chars)
print(f"  Texto plano reconstruído: '{result}'")
print()

# Vamos também tentar o processo inverso para verificação
print("Passo 4: Verificação (cifrando o resultado)")
def rail_fence_encrypt(plaintext, rails=3):
    """Cifra texto usando Rail Fence."""
    fence = [['' for _ in range(len(plaintext))] for _ in range(rails)]
    
    # Preencher padrão
    row = 0
    direction = 1
    for col in range(len(plaintext)):
        fence[row][col] = plaintext[col]
        row += direction
        if row == 0 or row == rails - 1:
            direction = -direction
    
    # Ler por linhas
    cipher = []
    for r in range(rails):
        for c in range(len(plaintext)):
            if fence[r][c]:
                cipher.append(fence[r][c])
    
    return ''.join(cipher)

# Verificar se cifrando o resultado obtemos o texto original
cipher_check = rail_fence_encrypt(result, 3)
print(f"  Cifrando o resultado: '{cipher_check}'")
print(f"  Texto cifrado original: '{ciphertext}'")

if cipher_check == ciphertext:
    print("  ✓ VERIFICAÇÃO BEM-SUCEDIDA!")
else:
    print("  ✗ A verificação falhou")
    print(f"  Diferença: '{cipher_check}' vs '{ciphertext}'")
    
    # Mostrar onde estão as diferenças
    print("  Comparação caractere por caractere:")
    for i in range(min(len(cipher_check), len(ciphertext))):
        if cipher_check[i] != ciphertext[i]:
            print(f"    Posição {i}: '{cipher_check[i]}' != '{ciphertext[i]}'")

print("\n" + "=" * 70)
print("RESULTADO FINAL")
print("=" * 70)

# Baseado na análise, o resultado mais provável é:
final_result = result
print(f"Texto plano recuperado: '{final_result}'")

# Vamos ver se podemos melhorar a legibilidade
print("\nTentando melhorar formatação:")
# Talvez haja padrões como "FLAG{" ou similar
if "FLAG" in final_result.upper():
    print("  Contém 'FLAG'")
if "CTF" in final_result.upper():
    print("  Contém 'CTF'")

# Mostrar em diferentes formatos
print(f"\nEm maiúsculas: '{final_result.upper()}'")
print(f"Em minúsculas: '{final_result.lower()}'")

# Vamos tentar uma abordagem final mais simples
print("\n" + "=" * 70)
print("SOLUÇÃO SIMPLIFICADA")
print("=" * 70)

# Implementação final simples
def decrypt_rail_fence_simple(cipher, rails=3):
    """Deciframento simples de Rail Fence."""
    n = len(cipher)
    
    # Calcular tamanho de cada trilho
    cycle = 2 * (rails - 1)
    full = n // cycle
    rem = n % cycle
    
    sizes = [full] * rails
    for i in range(1, rails-1):
        sizes[i] = 2 * full
    
    for i in range(rem):
        if i < rails:
            sizes[i] += 1
        else:
            sizes[2*rails-2-i] += 1
    
    # Extrair trilhos
    rails_text = []
    pos = 0
    for size in sizes:
        rails_text.append(cipher[pos:pos+size])
        pos += size
    
    # Reconstruir
    result = []
    pointers = [0] * rails
    row = 0
    down = True
    
    for _ in range(n):
        result.append(rails_text[row][pointers[row]])
        pointers[row] += 1
        
        if down:
            row += 1
            if row == rails - 1:
                down = False
        else:
            row -= 1
            if row == 0:
                down = True
    
    return ''.join(result)

# Aplicar
simple_result = decrypt_rail_fence_simple(ciphertext, 3)
print(f"Texto decifrado: '{simple_result}'")