document.getElementById('registerForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  
  // Show loading state
  const resultDiv = document.getElementById('registerResult');
  resultDiv.textContent = 'Creating account...';
  resultDiv.className = '';
  
  fetch('/register', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username, password})
  })
  .then(response => response.json())
  .then(data => {
    const toLoginBtn = document.getElementById('toLoginBtn');
    if (data.success) {
      resultDiv.textContent = 'Registration successful! You can now login.';
      resultDiv.className = 'success';
      toLoginBtn.style.display = 'block';
    } else {
      resultDiv.textContent = data.message || 'Registration failed. Please try again.';
      resultDiv.className = 'error';
      toLoginBtn.style.display = 'none';
    }
  })
  .catch(error => {
    console.error('Registration error:', error);
    resultDiv.textContent = 'Connection error. Please try again.';
    resultDiv.className = 'error';
    document.getElementById('toLoginBtn').style.display = 'none';
  });
});

document.getElementById('toLoginBtn').addEventListener('click', function() {
  window.location.href = 'login.html';
});