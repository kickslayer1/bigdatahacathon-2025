// demand_prediction.js
// Handles interactive price prediction form


document.addEventListener('DOMContentLoaded', function() {
  const showFormBtn = document.getElementById('showFormBtn');
  const formContainer = document.getElementById('predictionFormContainer');
  if (showFormBtn && formContainer) {
    showFormBtn.addEventListener('click', function() {
      formContainer.style.display = formContainer.style.display === 'none' ? 'block' : 'none';
    });
  }

  // Fetch options from backend and populate form
  fetch('http://127.0.0.1:5000/options')
    .then(response => response.json())
    .then(data => {
      // Populate item select
      const itemSelect = document.getElementById('item');
      itemSelect.innerHTML = '';
      data.items.forEach(item => {
        const option = document.createElement('option');
        option.value = item;
        option.textContent = item;
        itemSelect.appendChild(option);
      });
      // Populate time select
      const timeSelect = document.getElementById('time');
      timeSelect.innerHTML = '';
      data.times.forEach(time => {
        const option = document.createElement('option');
        option.value = time;
        option.textContent = time;
        timeSelect.appendChild(option);
      });
      // Populate amount select
      const amountSelect = document.getElementById('amount');
      amountSelect.innerHTML = '';
      data.amounts.forEach(amount => {
        const option = document.createElement('option');
        option.value = amount;
        option.textContent = amount;
        amountSelect.appendChild(option);
      });
    });
});

async function predictPrice() {
  const form = document.getElementById('predictForm');
  const data = {
    item: form.item.value,
    export: form.export.value,
    import: form.import.value,
    market_trend: form.market_trend.value,
    seasonality: form.seasonality.value
  };
  // Call backend API (Flask) for prediction
  const response = await fetch('http://127.0.0.1:5000/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (response.ok) {
    const result = await response.json();
    document.getElementById('predictionResult').innerText = 'Predicted Price: ' + result.price;
  } else {
    document.getElementById('predictionResult').innerText = 'Prediction failed.';
  }
}
