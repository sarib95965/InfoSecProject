from crypto import generate_keys, encrypt_message, decrypt_message
from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Security headers
Talisman(app)

# CSRF protection
app.secret_key = os.getenv('SECRET_KEY', 'defaultsecretkey')
csrf = CSRFProtect(app)

# For CSRF token in templates
@app.context_processor
def inject_csrf():
    from flask_wtf.csrf import generate_csrf
    return dict(csrf_token=generate_csrf)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form.get('message')
        flash(f"Message received: {message}", "info")
        return redirect('/')
    return render_template('index.html')

@app.route('/keygen', methods=['POST'])
def keygen():
    """Generate PQC key pair and return them"""
    public_key, private_key = generate_keys()
    return jsonify({
        'public_key': public_key.hex(),
        'private_key': private_key.hex()
    })

@app.route('/encrypt', methods=['POST'])
def encrypt():
    """Encrypt a message using provided public key"""
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
    """Decrypt ciphertext using provided private key"""
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
