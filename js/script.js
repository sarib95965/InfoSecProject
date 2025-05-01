// script.js

// Helper to send POST requests with JSON
async function postJson(url, data) {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await response.json();
  }
  
  // Handle Key Generation
  document.getElementById('btn-keygen').onclick = async () => {
    const output = await postJson('/keygen', {});
    document.getElementById('output-keygen').textContent = JSON.stringify(output, null, 2);
    document.getElementById('enc-pk').value = output.public_key;
    document.getElementById('dec-sk').value = output.private_key;
  };
  
  // Handle Encryption
  document.getElementById('btn-encrypt').onclick = async () => {
    const publicKey = document.getElementById('enc-pk').value.trim();
    const message = document.getElementById('enc-msg').value;
    const output = await postJson('/encrypt', { public_key: publicKey, message: message });
    document.getElementById('output-encrypt').textContent = JSON.stringify(output, null, 2);
    document.getElementById('dec-ct').value = output.ciphertext || '';
  };
  
  // Handle Decryption
  document.getElementById('btn-decrypt').onclick = async () => {
    const privateKey = document.getElementById('dec-sk').value.trim();
    const ciphertext = document.getElementById('dec-ct').value.trim();
    const output = await postJson('/decrypt', { private_key: privateKey, ciphertext: ciphertext });
    document.getElementById('output-decrypt').textContent = JSON.stringify(output, null, 2);
  };
  