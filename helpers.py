import random 

# chars from [a-zA-Z0-9]
CHARS = ['0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz']

def generate_url_code():
    random_chars = random.choices(CHARS, k = 5)
    url_code = "".join(random_chars)
    return url_code