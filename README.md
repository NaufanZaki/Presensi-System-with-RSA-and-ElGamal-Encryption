# Presensi System with RSA and ElGamal Encryption

This project is a secure **Presensi (Attendance)** system utilizing both **RSA** and **ElGamal encryption** algorithms. It allows for a practical comparison of these cryptographic methods while providing a user-friendly interface for both teachers and students.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Teacher App](#teacher-app)
  - [Student App](#student-app)
- [How It Works](#how-it-works)
  - [RSA Algorithm](#rsa-algorithm)
  - [ElGamal Algorithm](#elgamal-algorithm)
- [Comparison Results](#comparison-results)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)

---

## Overview

This system consists of two main components:
- **Teacher App**: Allows teachers to generate and encrypt presensi codes.
- **Student App**: Enables students to verify attendance using the encrypted presensi code.

Users can select between **RSA** and **ElGamal** for encryption and decryption. The system also displays performance metrics, making it suitable for comparing both algorithms.

---

## Features

- **Dual Encryption Options**: Choose between RSA and ElGamal encryption for attendance codes.
- **Decryption Flexibility**: Students can choose their preferred decryption method.
- **Performance Metrics**: Displays encryption time and memory usage for each algorithm.
- **Simple Web Interface**: User-friendly design built with Flask and HTML.

---

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
    - Access the Teacher App at `http://localhost:5001`.

4. **Start the Student App**:
    - Open a new terminal.
    - Navigate to the `student_app` directory:
      ```bash
      cd student_app
      ```
    - Run the app:
      ```bash
      python app.py
      ```
    - Access the Student App at `http://localhost:5002`.

---

## Usage

### Teacher App

1. Open the Teacher App in your browser at `http://localhost:5001`.
2. Enter the **class name** and click **"Generate Presensi Code"**.
3. The app will generate:
   - Original presensi code.
   - Encrypted codes (RSA and ElGamal).
   - Performance metrics (execution time and memory usage).

4. Share the presensi code with students for verification.

### Student App

1. Open the Student App in your browser at `http://localhost:5002`.
2. Log in with your name.
3. Enter the **presensi code** provided by the teacher.
4. Select the **Decryption Type** (RSA or ElGamal) and click **"Verify"**.
5. The app will display a success or error message based on the verification.

---

## How It Works

### RSA Algorithm

1. **Key Generation**:
   - Uses two large prime numbers to compute:
     - \( n = p \times q \)
     - \( \phi(n) = (p - 1) \times (q - 1) \)
   - Public key: \((e, n)\), Private key: \((d, n)\).

2. **Encryption**:
   - Converts each character in the presensi code to an encrypted value:
     \[
     \text{encrypted\_char} = (\text{ASCII\_value})^e \mod n
     \]

3. **Decryption**:
   - Restores the original code:
     \[
     \text{decrypted\_char} = (\text{encrypted\_char})^d \mod n
     \]

### ElGamal Algorithm

1. **Key Generation**:
   - Uses a prime \( p \), generator \( g \), and private key \( x \).
   - Public key: \((g, h, p)\), where \( h = g^x \mod p \).

2. **Encryption**:
   - Each character is encrypted as a pair:
     \[
     c1 = g^k \mod p,\ c2 = (\text{ASCII\_value} \times h^k) \mod p
     \]

3. **Decryption**:
   - Recovers the original value:
     \[
     \text{ASCII\_value} = (c2 \times c1^{(p - 1 - x)}) \mod p
     \]

---

## Comparison Results

### Encryption Speed
- **RSA**: **0.00011897 seconds**
- **ElGamal**: **0.00013113 seconds**

### Memory Usage
- **RSA**: **80 bytes**
- **ElGamal**: **112 bytes**

### Encrypted Outputs
- **RSA**: `[368, 624, 1794, 624]`
- **ElGamal**: `(221, [479, 271, 486, 271])`

### Conclusion
- **RSA** is faster and more memory-efficient than ElGamal, making it more practical for real-time applications like attendance systems.
- **ElGamal** offers more complex encryption but is less efficient in performance.

---

## Technologies Used

- **Python**: Programming language
- **Flask**: Web framework
- **Requests**: Library for HTTP requests
- **HTML/CSS**: Frontend structure and styling

---

## Project Structure
