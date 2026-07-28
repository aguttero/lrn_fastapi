import bcrypt

sample_password = "_test_1234"
print (f"Sample pwd= {sample_password}")
print (f"bin first char ={sample_password[0]} ")
print ("* - * - *")

# Hash a password for the first time, with a randomly-generated salt
# hashed = bcrypt.hashpw(sample_password, bcrypt.gensalt())
# hashed= b'$2b$12$FfgBxeRTeBR9E/oalqYxlOG.nBsunXefo0mdVs3DVjg1ZsIPyxzra'
hashed= b'$2b$12$CR75YN6O8BHRUD5uSTvraeqRnqHPAN.9ncRY.OyJdphN5hJxhYBke'

print (f"hashed pwd var type= {type(hashed)}")
print (f"hashed pwd= {hashed}")

 # Check that a unhashed password matches one that has previously been hashed
if bcrypt.checkpw(sample_password, hashed):
    print("It Matches!")
else:
    print("It Does not Match :(")


def hash_user_password(plain_password: str) -> str:
    # 1. Encode text to bytes (bcrypt strictly requires byte strings)
    password_bytes = plain_password.encode('utf-8')

    # 2. Generate a salt with a modern cost factor (12 is the production standard)
    salt = bcrypt.gensalt(rounds=12)

    # 3. Hash the password and decode the resulting bytes to a UTF-8 string for DB storage
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_user_password(plain_password: str, stored_hash: str) -> bool:
    # Convert string inputs back to bytes for verification
    password_bytes = plain_password.encode('utf-8')
    hash_bytes = stored_hash.encode('utf-8')

    # Securely verify (avoids timing attacks)
    return bcrypt.checkpw(password_bytes, hash_bytes)
