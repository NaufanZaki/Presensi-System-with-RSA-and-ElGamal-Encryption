# teacher_app/app.py
import random
import tracemalloc
import time
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# RSA Key Generation and Encryption
def generate_rsa_keys():
    p, q = 61, 53  # Small primes for demonstration; use larger primes in production
    n = p * q
    e = 17  # Public exponent
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)  # Private exponent
    return {'public': (e, n), 'private': (d, n)}

def rsa_encrypt(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

# ElGamal Key Generation and Encryption
def generate_elgamal_keys(prime=1019, generator=2):
    private_key = random.randint(1, prime - 2)  # Secret key x
    public_key = (generator, pow(generator, private_key, prime), prime)  # (g, g^x mod p, p)
    return public_key, private_key

def elgamal_encrypt(message, public_key):
    g, h, p = public_key
    k = random.randint(1, p - 2)  # Random key k
    c1 = pow(g, k, p)
    c2 = [(ord(char) * pow(h, k, p)) % p for char in message]
    return (c1, c2)

# Store presensi data (including student name and class)
presensi_list = []

@app.route('/', methods=['GET', 'POST'])
def assign_class():
    presensi_code = None
    rsa_encrypted_code = None
    elgamal_encrypted_code = None
    rsa_time, elgamal_time, rsa_memory, elgamal_memory = None, None, None, None

    if request.method == 'POST':
        class_name = request.form.get('class_name')
        
        # Generate a random attendance code for demo
        presensi_code = str(random.randint(1000, 9999))
        
        # RSA Encryption
        rsa_start_time = time.time()
        tracemalloc.start()
        rsa_keys = generate_rsa_keys()
        rsa_encrypted_code = rsa_encrypt(presensi_code, rsa_keys['public'])
        rsa_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        rsa_time = time.time() - rsa_start_time

        # ElGamal Encryption
        elgamal_start_time = time.time()
        tracemalloc.start()
        elgamal_public_key, elgamal_private_key = generate_elgamal_keys()
        elgamal_encrypted_code = elgamal_encrypt(presensi_code, elgamal_public_key)
        elgamal_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        elgamal_time = time.time() - elgamal_start_time

        # Store the encrypted codes and keys in app config
        app.config['RSA_ENCRYPTED_CODE'] = rsa_encrypted_code
        app.config['ELGAMAL_ENCRYPTED_CODE'] = elgamal_encrypted_code
        app.config['PRESENSI_CODE'] = presensi_code
        app.config['RSA_KEYS'] = rsa_keys
        app.config['ELGAMAL_KEYS'] = (elgamal_public_key, elgamal_private_key)
        app.config['CLASS_NAME'] = class_name
        
        return render_template('index.html', 
                               class_name=class_name, 
                               presensi_code=presensi_code, 
                               rsa_time=rsa_time, 
                               rsa_memory=rsa_memory[1] - rsa_memory[0],
                               elgamal_time=elgamal_time, 
                               elgamal_memory=elgamal_memory[1] - elgamal_memory[0],
                               rsa_encrypted_code=rsa_encrypted_code, 
                               elgamal_encrypted_code=elgamal_encrypted_code)
    
    return render_template('index.html')

# API to provide both RSA and ElGamal encrypted presensi data to the student app
@app.route('/get_presensi_data', methods=['GET'])
def get_presensi_data():
    return jsonify({
        'rsa_code': app.config.get('RSA_ENCRYPTED_CODE'),
        'elgamal_code': app.config.get('ELGAMAL_ENCRYPTED_CODE'),
        'rsa_keys': app.config.get('RSA_KEYS')['private'],
        'elgamal_keys': app.config.get('ELGAMAL_KEYS')[1]  # Only private key for decryption
    })

# API to update presensi list with student name and class
@app.route('/update_presensi', methods=['POST'])
def update_presensi():
    student_name = request.json.get('student_name')
    presensi_class = app.config.get('CLASS_NAME')  # Get class name from current session
    if student_name and presensi_class:
        presensi_list.append({'name': student_name, 'class': presensi_class})
        return jsonify({'message': 'Presensi updated successfully'})
    return jsonify({'error': 'Invalid data'}), 400

# Route to display students who have marked their presensi
@app.route('/view_presensi', methods=['GET'])
def view_presensi():
    return render_template('presensi_list.html', presensi_list=presensi_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)