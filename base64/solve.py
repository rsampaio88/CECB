# Solução completa e simplificada
import base64

encoded = "VGpJeGRVMUhiRzFqUjJoM1lWUkNlbVJYWkhoalYzTXlUVWRqTkdOcVRuaGxSRmt6WlZReFZWUkdWbFJTVmtwbVZFVkdUMU5WV1QwPQ=="

# Camada 1
layer1 = base64.b64decode(encoded)  # TjIxdU1HbR1j2M3YURCemVXYWpoY3MyeTVVZGjNGn1TunhSRmt6WlZReFZW...
layer1_str = layer1.decode('latin-1')

# Camada 2  
layer2 = base64.b64decode(layer1_str)  # N21uMG1HmQxjZjNkVEJ6ZlhjakhYM3k5VWRoNE5vdFNOa3haTFN4Vl...
layer2_str = layer2.decode('latin-1')

# Camada 3
layer3 = base64.b64decode(layer2_str)  # m7n0mGQcf3dTBzfXcjHX3y9Udh4NotSNkxZLSxV...

final_message = layer3.decode('utf-8')
print(final_message)
