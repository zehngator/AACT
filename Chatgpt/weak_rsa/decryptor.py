from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Random import get_random_bytes

# Function to load the RSA private key components
def load_private_key(n, e, d):
    return RSA.construct((n, e, d))

# Function to decrypt the ciphertext using RSA
def rsa_decrypt(ciphertext, private_key):
    # Convert ciphertext from bytes to integer
    ciphertext_int = bytes_to_long(ciphertext)
    
    # Perform RSA decryption (c^d mod n)
    decrypted_int = pow(ciphertext_int, private_key.d, private_key.n)
    
    # Convert the decrypted integer back to bytes
    decrypted_bytes = long_to_bytes(decrypted_int)
    
    return decrypted_bytes

# Main function to decrypt a file
def decrypt_file(input_file, output_file, n, e, d):
    # Load private key
    private_key = load_private_key(n, e, d)
    
    # Read the encrypted ciphertext from the file
    with open(input_file, 'rb') as f:
        ciphertext = f.read()
    
    # Decrypt the ciphertext
    decrypted_data = rsa_decrypt(ciphertext, private_key)
    
    # Write the decrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

# Example RSA parameters
n = 573177824579630911668469272712547865443556654086190104722795509756891670023259031275433509121481030331598569379383505928315495462888788593695945321417676298471525243254143375622365552296949413920679290535717172319562064308937342567483690486592868352763021360051776130919666984258847567032959931761686072492923
e = 68180928631284147212820507192605734632035524131139938618069575375591806315288775310503696874509130847529572462608728019290710149661300246138036579342079580434777344111245495187927881132138357958744974243365962204835089753987667395511682829391276714359582055290140617797814443530797154040685978229936907206605
d = 4242617958003109100082864406072167427785560147150840767890248587370173330663486845929242723

# Example of how to use the function
input_file = 'flag.enc'  # Path to the encrypted file
output_file = 'decrypted_file.txt'  # Path to save the decrypted file

# Decrypt the file
decrypt_file(input_file, output_file, n, e, d)

print(f"File decrypted successfully and saved as {output_file}")

