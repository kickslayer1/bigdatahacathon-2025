document.addEventListener('DOMContentLoaded', function() {
  // Fetch available items for the dropdown
  fetch('http://127.0.0.1:5000/options')
    .then(response => response.json())
    .then(data => {
      const itemSelect = document.getElementById('itemSelect');
      itemSelect.innerHTML = '';
      data.items.forEach(item => {
        const option = document.createElement('option');
        option.value = item;
        option.textContent = item;
        itemSelect.appendChild(option);
      });
    });

  // Handle form submission
  document.getElementById('datamapForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const selectedItem = document.getElementById('itemSelect').value;
    fetch('http://127.0.0.1:5000/datamap_item', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({item: selectedItem})
    })
    .then(response => response.json())
    .then(data => {
      const itemDataDiv = document.getElementById('itemData');
      if (data.length > 0) {
        let html = '<table><tr><th>Item</th><th>Time</th><th>Amount</th></tr>';
        data.forEach(row => {
          html += `<tr><td>${row.item}</td><td>${row.time}</td><td>${row.amount}</td></tr>`;
        });
        html += '</table>';
        itemDataDiv.innerHTML = html;
      } else {
        itemDataDiv.textContent = 'No data found for this item.';
      }
    });
  });
});