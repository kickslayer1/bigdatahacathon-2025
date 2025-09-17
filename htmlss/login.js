document.getElementById('loginForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  fetch('/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username, password})
  })
  .then(response => response.json())
  .then(data => {
    const resultDiv = document.getElementById('loginResult');
    if (data.success) {
      resultDiv.textContent = 'Login successful! Redirecting...';
      setTimeout(() => { window.location.href = 'front_page.html'; }, 1500);
    } else {
      resultDiv.textContent = data.message;
    }
  });
});