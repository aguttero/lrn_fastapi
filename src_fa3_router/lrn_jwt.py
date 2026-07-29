import jwt

SECRET_01 = "3ad1d79be2cf2be4f56a15be94eb4c6e429ce8e9878fa6807908ac30a0df731d"
SECRET_02 = "supersecret"
ALGORITHM = "HS256"

# Run in shell to obtain key
# Genera una cadena aleatoria de 64 caracteres hexadecimales (que representan 32 bytes de datos criptográficamente seguros)
# Openssl herramienta de línea de comandos de OpenSSL para funciones criptográficas.
# rand  utilice su generador de números pseudoaleatorios criptográficamente fuerte (CSPRNG).
# - hex formatea salida a hex
# 32 especifica numero de bytes de aleatoriedad a generar (1byte = 2 char hexa)
# openssl rand -hex 32

encoded_jwt = jwt.encode({"some": "payload"}, SECRET_01, algorithm="HS256")

decoded_jwt = jwt.decode(encoded_jwt, SECRET_01, algorithms=["HS256"])

print (f"encoded_jwt= {encoded_jwt}")
print (f"decoded_jwt= {decoded_jwt}")
