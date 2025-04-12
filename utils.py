import bcrypt

def verify_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode(), hashed_password.encode())
