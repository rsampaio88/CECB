import binascii

c1 = binascii.unhexlify("adaca0a74acd61fe238b4ca5102c8437dd6843b7fff87a45a63652a06d")
p1 = "HEADER: version=1; status=ok\n".encode('ascii')
c2 = binascii.unhexlify("b7aad5bc5dda189103ab6c8914379c3b8f3f56beb2fe745ced3f0aa85390ef09f4fe")

# Como c2 é mais longo que c1, só podemos recuperar até len(c1)
result = bytearray()
for i in range(len(c1)):
    result.append(c2[i] ^ c1[i] ^ p1[i % len(p1)])

print("Mensagem secreta recuperada:")
print(result.decode('ascii'))