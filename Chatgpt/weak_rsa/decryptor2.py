from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from sympy import factorint
import math

# Function to factor the modulus n
def factor_n(n):
    factors = factorint(n)  # Factor the modulus n
    if len(factors) == 2:  # RSA key should have exactly two prime factors
        return factors.keys()
    else:
        raise ValueError("Cannot factor n. It's either not a product of two primes or is too large.")

# Function to calculate private exponent d
def compute_private_exponent(n, e, p, q):
    # Calculate Euler's totient function φ(n) = (p - 1) * (q - 1)
    phi_n = (p - 1) * (q - 1)
    # Compute the modular inverse of e modulo φ(n)
    d = pow(e, -1, phi_n)
    return d

# Function to decrypt the ciphertext using RSA formula m = c^d mod n
def rsa_decrypt(ciphertext, d, n):
    ciphertext_int = bytes_to_long(ciphertext)
    decrypted_int = pow(ciphertext_int, d, n)
    decrypted_bytes = long_to_bytes(decrypted_int)
    return decrypted_bytes

# Main function to decrypt an encrypted flag
def decrypt_flag(n, e, encrypted_flag):
    # Step 1: Factor the modulus n to get p and q
    p, q = factor_n(n)
    
    # Step 2: Compute the private exponent d
    d = compute_private_exponent(n, e, p, q)
    
    # Step 3: Decrypt the ciphertext (encrypted_flag)
    decrypted_flag = rsa_decrypt(encrypted_flag, d, n)
    
    return decrypted_flag

# Example usage
if __name__ == "__main__":
    # Replace these with the weak RSA public key and encrypted flag
    n = 573177824579630911668469272712547865443556654086190104722795509756891670023259031275433509121481030331598569379383505928315495462888788593695945321417676298471525243254143375622365552296949413920679290535717172319562064308937342567483690486592868352763021360051776130919666984258847567032959931761686072492923
    e = 68180928631284147212820507192605734632035524131139938618069575375591806315288775310503696874509130847529572462608728019290710149661300246138036579342079580434777344111245495187927881132138357958744974243365962204835089753987667395511682829391276714359582055290140617797814443530797154040685978229936907206605

    encrypted_flag = bytes.fromhex("01a25fe...ee")  # Use the full encrypted flag hex here

    # Decrypt the flag
    decrypted_flag = decrypt_flag(n, e, encrypted_flag)

    # Print the decrypted flag (or save to a file)
    print("Decrypted Flag:", decrypted_flag.decode('utf-8', errors='ignore'))

