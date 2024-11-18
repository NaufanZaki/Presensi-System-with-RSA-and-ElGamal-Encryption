
# Presensi System with RSA and ElGamal Encryption, Comparison between RSA and ElGamal Encryption

This project is a secure presensi (attendance) system utilizing both **RSA** and **ElGamal encryption** algorithms. It consists of two main components:
- **Teacher App**: Used by the teacher to generate and encrypt presensi codes.
- **Student App**: Used by students to verify their attendance using a presensi code.

The project allows users to select between RSA and ElGamal for encryption and decryption, enabling a practical comparison of these two cryptographic methods.

## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
  - [Teacher App](#teacher-app)
  - [Student App](#student-app)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
  - [RSA](#rsa-rivest-shamir-adleman)
  - [ElGamal](#elgamal)
- [Comparison](#Comparison-Result)
- [Technologies Used](#technologies-used)

## Features

- **Dual Encryption Methods**: Supports both RSA and ElGamal encryption.
- **Decryption Choice**: Students can choose the decryption type when verifying their attendance.
- **Performance Comparison**: Displays execution time and memory usage for each encryption method in the Teacher App.
- **Simple Web Interface**: Built with Flask and HTML for easy navigation and use.

## Setup

### Prerequisites

- **Python 3.x**
- **Flask** and **Requests** library

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/NaufanZaki/Presensi-System-with-RSA-and-ElGamal-Encryption.git
    cd presensi-encryption
    ```

2. **Install required packages**:
    ```bash
    pip install flask requests
    ```

3. **Start the Teacher App**:
    - Navigate to the `teacher_app` directory:
      ```bash
      cd teacher_app
      ```
    - Run the app:
      ```bash
      python app.py
      ```
    - The Teacher App should now be running on `http://localhost:5001`.

4. **Start the Student App**:
    - Open a new terminal window.
    - Navigate to the `student_app` directory:
      ```bash
      cd student_app
      ```
    - Run the app:
      ```bash
      python app.py
      ```
    - The Student App should now be running on `http://localhost:5002`.

## Usage

### Teacher App

1. Open the Teacher App in your browser at `http://localhost:5001`.
2. Enter the class name and click "Generate Presensi Code".
3. The app will generate a presensi code and display:
   - The original presensi code.
   - Encrypted codes using both RSA and ElGamal.
   - Performance metrics (execution time and memory usage) for each encryption method.

4. Students can now use the Student App to verify their attendance with the generated code.

### Student App

1. Open the Student App in your browser at `http://localhost:5002`.
2. Log in by entering your name.
3. Enter the presensi code provided by the teacher.
4. Select the **Decryption Type** (RSA or ElGamal) to use for verification.
5. Click "Verify".
6. The app will display a success or error message based on whether the entered code matches the decrypted code.

## Project Structure

```
presensi-encryption/
├── teacher_app/
│   ├── app.py                # Main Flask app for the Teacher
│   └── templates/
│       └── index.html        # Teacher interface for generating presensi codes
├── student_app/
│   ├── app.py                # Main Flask app for the Student
│   └── templates/
│       └── verify.html       # Student interface for verifying presensi codes
└── README.md                 # Project documentation
```

## How It Works

This project leverages two encryption methods, **RSA** and **ElGamal**, for securely verifying student attendance. Here’s a detailed breakdown of each encryption method:

### RSA (Rivest-Shamir-Adleman)

1. **Key Generation**:
   - RSA uses two large prime numbers, \( p \) and \( q \), to generate:
     - \( n = p \times q \)
     - \( \phi(n) = (p - 1) \times (q - 1) \)
   - An **encryption exponent** \( e \) is chosen, and the **decryption exponent** \( d \) is computed so that \( d \times e \equiv 1 \ (	ext{mod} \ \phi(n)) \).
   - The **public key** is \((e, n)\) and the **private key** is \((d, n)\).

2. **Encryption**:
   - The Teacher App encrypts each character in the presensi code by raising its ASCII value to the power of \( e \) modulo \( n \):
     \[
     	ext{encrypted\_char} = (	ext{ASCII\_value})^e \mod n
     \]

3. **Decryption**:
   - The Student App decrypts each encrypted character using the private key \( (d, n) \):
     \[
     	ext{decrypted\_char} = (	ext{encrypted\_char})^d \mod n
     \]
   - The decrypted ASCII values are converted back to the original presensi code for verification.

### ElGamal

1. **Key Generation**:
   - The Teacher App selects a large **prime number** \( p \), a **generator** \( g \), and a random **private key** \( x \).
   - The **public key** is calculated as \( h = g^x \mod p \), with \((g, h, p)\) as the public key and \( x \) as the private key.

2. **Encryption**:
   - For each character in the presensi code, a random integer \( k \) is selected as a session key.
   - Each character is encrypted into a pair \((c1, c2)\):
     - \( c1 = g^k \mod p \)
     - \( c2 = (	ext{ASCII\_value} \times h^k) \mod p \)

3. **Decryption**:
   - The Student App decrypts each character pair \((c1, c2)\) using the private key \( x \):
     \[
     	ext{ASCII\_value} = (c2 \times c1^{(p - 1 - x)}) \mod p
     \]
   - The decrypted values are converted back to characters to reconstruct the original presensi code.

This system allows for a practical comparison of both algorithms, showing differences in execution time and memory usage.

### Comparison Result
<img width="513" alt="Screenshot 2024-11-18 at 08 58 42" src="https://github.com/user-attachments/assets/86ae0e5b-74ae-43db-81e5-72d22cc0810b">

### 1. **Encryption Speed**
- **RSA** demonstrates significantly faster encryption performance compared to **ElGamal**.
  - RSA encryption time: **0.00040793 seconds**.
  - ElGamal encryption time: **6.008 seconds**.
- This highlights RSA's efficiency in encryption speed over ElGamal.

### 2. **Memory Usage**
- RSA uses less memory (**80 bytes**) compared to ElGamal, which requires **136 bytes**.
- This indicates that RSA is more resource-efficient than ElGamal.

### 3. **Encryption Output**
- RSA generates encrypted outputs as a one-dimensional array, e.g., `[1802, 1794, 538, 529]`.
- ElGamal produces encrypted outputs in the form of pairs `(k, [c1, c2, c3, ...])`, which are more complex than RSA.

### General Conclusion
- **RSA** is more suitable for applications requiring high performance and limited resources, such as this attendance website.
- While ElGamal provides enhanced security against certain types of attacks, it is less efficient in terms of speed and memory usage.
- The choice of algorithm depends on the application's requirements, but for an attendance website where fast encryption is essential, RSA is the more practical choice.

## Technologies Used

- **Python**: Programming language
- **Flask**: Web framework
- **Requests**: Library for HTTP requests
- **HTML/CSS**: Frontend structure and styling
