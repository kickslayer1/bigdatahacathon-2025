document.getElementById('registerForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  fetch('/register', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username, password})
  })
  .then(response => response.json())
  .then(data => {
    const resultDiv = document.getElementById('registerResult');
    const toLoginBtn = document.getElementById('toLoginBtn');
    if (data.success) {
      resultDiv.textContent = 'Registration successful! You can now login.';
      toLoginBtn.style.display = 'inline-block';
    } else {
      resultDiv.textContent = data.message;
      toLoginBtn.style.display = 'none';
    }
  });
});

document.getElementById('toLoginBtn').addEventListener('click', function() {
  window.location.href = 'login.html';
});