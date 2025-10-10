document.getElementById('loginForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  
  // Show loading state
  const resultDiv = document.getElementById('loginResult');
  resultDiv.textContent = 'Logging in...';
  resultDiv.className = '';
  
  fetch('/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username, password})
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      resultDiv.textContent = 'Login successful! Redirecting to dashboard...';
      resultDiv.className = 'success';
      setTimeout(() => { window.location.href = 'front_page.html'; }, 1500);
    } else {
      resultDiv.textContent = data.message || 'Login failed. Please check your credentials.';
      resultDiv.className = 'error';
    }
  })
  .catch(error => {
    console.error('Login error:', error);
    resultDiv.textContent = 'Connection error. Please try again.';
    resultDiv.className = 'error';
  });
});