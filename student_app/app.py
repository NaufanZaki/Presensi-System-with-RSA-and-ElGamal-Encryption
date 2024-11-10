# student_app/app.py
from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# RSA and ElGamal decryption functions
def rsa_decrypt(encrypted_message, private_key):
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in encrypted_message])

def elgamal_decrypt(c1, c2, private_key, prime):
    return ''.join([chr((char * pow(c1, prime - 1 - private_key, prime)) % prime) for char in c2])

# Route for student login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Store the student name in the session after login
        session['student_name'] = request.form.get('student_name')
        return redirect(url_for('verify_code'))
    return render_template('login.html')

# Route for student to enter presensi code
@app.route('/verify', methods=['GET', 'POST'])
def verify_code():
    if 'student_name' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        entered_code = request.form.get('presensi_code')
        decryption_type = request.form.get('decryption_type')
        student_name = session['student_name']
        
        # Fetch encrypted data and keys from teacher app
        response = requests.get('http://localhost:5001/get_presensi_data')
        data = response.json()

        # Choose decryption method based on user selection
        if decryption_type == 'RSA':
            decrypted_code = rsa_decrypt(data['rsa_code'], data['rsa_keys'])
        elif decryption_type == 'ElGamal':
            c1, c2 = data['elgamal_code']
            decrypted_code = elgamal_decrypt(c1, c2, data['elgamal_keys'], 1019)

        # Check if the entered code matches the decrypted code
        if entered_code == decrypted_code:
            presensi_data = {'student_name': student_name}
            # Send presensi data after successful verification
            requests.post('http://localhost:5001/update_presensi', json=presensi_data)
            return render_template('verify.html', result=f"Success! {student_name} has been marked present.")
        else:
            return render_template('verify.html', result="Error! Incorrect presensi code.")

    return render_template('verify.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)