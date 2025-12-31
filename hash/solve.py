import itertools
import struct
import time
from collections import defaultdict

def toy_hash(data):
    """Implementação Python exata da função ToyHash do Go."""
    h = 0x9747b28c
    for b in data:
        h ^= b
        h = (h * 0x45d9f3b) & 0xffffffff  # Emulação de multiplicação de 32 bits
        h = ((h << 13) | (h >> 19)) & 0xffffffff  # Rotação de 32 bits
        h ^= 0x27100001
        h &= 0xffffffff  # Manter dentro de 32 bits
    return h

def find_collision_bruteforce(max_length=5):
    """
    Tenta encontrar colisões por força bruta.
    Limita o comprimento para tornar viável.
    """
    print("Procurando colisões por força bruta...")
    seen = {}
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    # Testar strings curtas primeiro
    for length in range(1, max_length + 1):
        print(f"Testando strings de comprimento {length}...")
        count = 0
        
        for chars_tuple in itertools.product(chars, repeat=length):
            s = ''.join(chars_tuple)
            h = toy_hash(s.encode('ascii'))
            
            if h in seen:
                s2 = seen[h]
                if s != s2:  # Garantir que são diferentes
                    print(f"Colisão encontrada!")
                    print(f"  Hash: 0x{h:08x}")
                    print(f"  String 1: '{s2}'")
                    print(f"  String 2: '{s}'")
                    return s2, s
            
            seen[h] = s
            
            count += 1
            if count % 100000 == 0:
                print(f"  Testadas {count} strings...")
    
    print("Nenhuma colisão encontrada na busca por força bruta.")
    return None, None

def find_collision_birthday_attack(max_length=10, num_strings=100000):
    """
    Usa o ataque do aniversário para encontrar colisões.
    Mais eficiente que força bruta completa.
    """
    print("Usando ataque do aniversário...")
    import random
    import string
    
    # Gerar strings aleatórias
    hashes = {}
    
    for i in range(num_strings):
        # Gerar string aleatória de comprimento variável
        length = random.randint(3, max_length)
        s = ''.join(random.choice(string.ascii_letters + string.digits) 
                   for _ in range(length))
        h = toy_hash(s.encode('ascii'))
        
        if h in hashes:
            s2 = hashes[h]
            if s != s2:
                print(f"Colisão encontrada após {i+1} tentativas!")
                print(f"  Hash: 0x{h:08x}")
                print(f"  String 1: '{s2}'")
                print(f"  String 2: '{s}'")
                return s2, s
        
        hashes[h] = s
        
        if (i + 1) % 10000 == 0:
            print(f"  Geradas {i+1} strings...")
    
    print(f"Nenhuma colisão encontrada em {num_strings} tentativas.")
    return None, None

def analyze_hash_function():
    """Analisa propriedades da função hash."""
    print("Analisando a função ToyHash...")
    
    # Testar algumas strings básicas
    test_strings = [
        "a", "b", "ab", "ba", "abc", "cba",
        "hello", "world", "test", "1234"
    ]
    
    print("\nHash de algumas strings de teste:")
    for s in test_strings:
        h = toy_hash(s.encode('ascii'))
        print(f"  '{s}' -> 0x{h:08x}")
    
    # Verificar se pequenas mudanças produzem grandes diferenças
    print("\nVerificando mudanças pequenas:")
    base = "hello"
    base_hash = toy_hash(base.encode('ascii'))
    print(f"  '{base}' -> 0x{base_hash:08x}")
    
    for i in range(ord('a'), ord('z')):
        s = base + chr(i)
        h = toy_hash(s.encode('ascii'))
        diff = h ^ base_hash
        print(f"  '{s}' -> 0x{h:08x} (diff: 0x{diff:08x})")

def find_collision_manual():
    """
    Tenta encontrar colisões manualmente usando propriedades matemáticas.
    A função usa operações XOR e multiplicação que podem permitir
    encontrar pares que se cancelam.
    """
    print("\nTentando encontrar colisões analiticamente...")
    
    # A função hash tem a forma:
    # h = ((h ^ b) * k1) rot13 ^ k2
    # Podemos tentar encontrar b1 e b2 tais que:
    # ((h ^ b1) * k1) rot13 ^ k2 = ((h ^ b2) * k1) rot13 ^ k2
    
    # Primeiro, vamos testar strings de um caractere
    print("Testando colisões de um caractere...")
    char_hashes = {}
    for i in range(32, 127):  # Caracteres ASCII imprimíveis
        s = chr(i)
        h = toy_hash(s.encode('ascii'))
        if h in char_hashes:
            s2 = char_hashes[h]
            print(f"Colisão encontrada!")
            print(f"  Hash: 0x{h:08x}")
            print(f"  '{s2}' e '{s}'")
            return s2, s
        char_hashes[h] = s
    
    # Agora testar pares de caracteres
    print("Testando colisões de dois caracteres...")
    seen = {}
    for i in range(32, 127):
        for j in range(32, 127):
            s = chr(i) + chr(j)
            h = toy_hash(s.encode('ascii'))
            if h in seen:
                s2 = seen[h]
                if s != s2:
                    print(f"Colisão encontrada!")
                    print(f"  Hash: 0x{h:08x}")
                    print(f"  '{s2}' e '{s}'")
                    return s2, s
            seen[h] = s
    
    return None, None

def find_collision_advanced(max_len=6):
    """
    Busca avançada por colisões usando múltiplas estratégias.
    """
    import random
    import string
    
    print("Busca avançada por colisões...")
    
    # Tabela hash para armazenar hashes já vistos
    hash_table = {}
    
    # Gerar strings sistematicamente
    chars = string.ascii_letters + string.digits
    
    # Estratégia 1: Strings que diferem por um caractere especial
    print("Estratégia 1: Strings similares...")
    base_strings = ["a", "test", "hello", "123", "abc", "xyz"]
    
    for base in base_strings:
        for i in range(32, 127):
            for pos in range(len(base) + 1):
                # Inserir caractere em posição diferente
                s1 = base[:pos] + chr(i) + base[pos:]
                # Modificar um caractere
                if pos < len(base):
                    s2 = base[:pos] + chr((i + 1) % 128) + base[pos+1:]
                
                h1 = toy_hash(s1.encode('ascii'))
                if h1 in hash_table:
                    s_prev = hash_table[h1]
                    if s1 != s_prev:
                        print(f"Colisão encontrada com estratégia 1!")
                        print(f"  Hash: 0x{h1:08x}")
                        print(f"  '{s_prev}' e '{s1}'")
                        return s_prev, s1
                hash_table[h1] = s1
    
    # Estratégia 2: Strings aleatórias
    print("Estratégia 2: Strings aleatórias...")
    random.seed(42)  # Seed fixa para reproducibilidade
    
    for attempt in range(1000000):
        length = random.randint(3, max_len)
        s = ''.join(random.choice(chars) for _ in range(length))
        h = toy_hash(s.encode('ascii'))
        
        if h in hash_table:
            s_prev = hash_table[h]
            if s != s_prev:
                print(f"Colisão encontrada após {attempt+1} tentativas!")
                print(f"  Hash: 0x{h:08x}")
                print(f"  '{s_prev}' e '{s}'")
                return s_prev, s
        
        hash_table[h] = s
        
        if (attempt + 1) % 100000 == 0:
            print(f"  {attempt+1} tentativas...")
    
    return None, None

# Função principal
def main():
    print("=" * 60)
    print("DESAFIO: ENCONTRAR COLISÕES NO TOYHASH")
    print("=" * 60)
    
    # Primeiro, vamos analisar a função
    analyze_hash_function()
    
    print("\n" + "=" * 60)
    print("BUSCANDO COLISÕES...")
    print("=" * 60)
    
    # Tentar diferentes métodos
    methods = [
        ("Busca manual", find_collision_manual),
        ("Busca avançada", lambda: find_collision_advanced(max_len=5)),
    ]
    
    for method_name, method_func in methods:
        print(f"\nTentando método: {method_name}")
        s1, s2 = method_func()
        if s1 and s2:
            print(f"\n✓ COLISÃO ENCONTRADA!")
            print(f"String 1: '{s1}'")
            print(f"String 2: '{s2}'")
            print(f"Ambos produzem hash: 0x{toy_hash(s1.encode('ascii')):08x}")
            
            # Verificar
            h1 = toy_hash(s1.encode('ascii'))
            h2 = toy_hash(s2.encode('ascii'))
            if h1 == h2 and s1 != s2:
                print("✓ Verificação bem-sucedida!")
                return s1, s2
    
    print("\nNenhum método encontrou colisão. Tentando busca exaustiva...")
    
    # Busca exaustiva para strings muito curtas
    s1, s2 = find_collision_bruteforce(max_length=4)
    if s1 and s2:
        return s1, s2
    
    print("\nTentando ataque do aniversário...")
    s1, s2 = find_collision_birthday_attack(max_length=6, num_strings=200000)
    if s1 and s2:
        return s1, s2
    
    print("\nNão foi possível encontrar colisão com os métodos atuais.")
    return None, None

if __name__ == "__main__":
    s1, s2 = main()
    
    if s1 and s2:
        print("\n" + "=" * 60)
        print("RESULTADO FINAL:")
        print("=" * 60)
        print("Duas strings ASCII diferentes com o mesmo hash:")
        print(f"'{s1}'")
        print(f"'{s2}'")
        print(f"\nAmbas produzem: 0x{toy_hash(s1.encode('ascii')):08x}")
    else:
        print("Não foi possível encontrar colisão.")