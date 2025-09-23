// Fetch and display export commodities data
function showExportCommodities() {
  fetch('/export_commodities_data')
    .then(response => response.json())
    .then(data => {
      let html = '<h3>Export Commodities</h3><table border="1"><tr>';
      if (data.length > 0) {
        Object.keys(data[0]).forEach(col => html += `<th>${col}</th>`);
        html += '</tr>';
        data.forEach(row => {
          html += '<tr>';
          Object.values(row).forEach(val => html += `<td>${val}</td>`);
          html += '</tr>';
        });
      }
      html += '</table>';
      document.getElementById('exportCommodities').innerHTML = html;
    });
}

// Fetch and display trade data
function showTradeData() {
  fetch('/trade20_25q2_data')
    .then(response => response.json())
    .then(data => {
      let html = '<h3>Trade 2020-2025 Q2</h3><table border="1"><tr>';
      if (data.length > 0) {
        Object.keys(data[0]).forEach(col => html += `<th>${col}</th>`);
        html += '</tr>';
        data.forEach(row => {
          html += '<tr>';
          Object.values(row).forEach(val => html += `<td>${val}</td>`);
          html += '</tr>';
        });
      }
      html += '</table>';
      document.getElementById('tradeData').innerHTML = html;
    });
}

// Call these functions on page load
document.addEventListener('DOMContentLoaded', function() {
  showExportCommodities();
  showTradeData();
});