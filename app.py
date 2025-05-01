import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from flask_talisman import Talisman  # 🛡️ Import Talisman

# Load environment variables
load_dotenv()


# Custom CSP to allow Bootstrap + inline scripts/styles
csp = {
    'default-src': [
        '\'self\''
    ],
    'style-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
        '\'unsafe-inline\''
    ],
    'script-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
        '\'unsafe-inline\''
    ]
}


# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecret')

# 🛡️ Enable Flask-Talisman with default settings (adds security headers)
Talisman(app, content_security_policy=csp)

# Import cryptographic functions
from crypto import generate_keys, encrypt_message, decrypt_message

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/keygen', methods=['POST'])
def keygen():
    public_key, private_key = generate_keys()
    return jsonify({
        'public_key': public_key.hex(),
        'private_key': private_key.hex()
    })

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json() or {}
    public_key_hex = data.get('public_key')
    message = data.get('message')
    try:
        ciphertext, shared_secret = encrypt_message(public_key_hex, message)
        return jsonify({
            'ciphertext': ciphertext.hex(),
            'shared_secret': shared_secret.hex()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json() or {}
    private_key_hex = data.get('private_key')
    ciphertext_hex = data.get('ciphertext')
    try:
        shared_secret = decrypt_message(private_key_hex, ciphertext_hex)
        return jsonify({
            'shared_secret': shared_secret.hex()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
