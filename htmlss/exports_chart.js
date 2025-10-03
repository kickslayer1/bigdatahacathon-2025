document.addEventListener('DOMContentLoaded', function() {
  fetch('/exports_data')
    .then(response => response.json())
    .then(data => {
      const labels = data.map(row => row.period);
      const exportsData = data.map(row => row.exports);
      const importsData = data.map(row => row.imports);
      const reimportsData = data.map(row => row['re-imports']);

      const ctx = document.getElementById('exportsLineChart').getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Exports',
              data: exportsData,
              borderColor: '#003366',
              backgroundColor: 'rgba(0,51,102,0.1)',
              fill: false,
              tension: 0.1
            },
            {
              label: 'Imports',
              data: importsData,
              borderColor: '#d9534f',
              backgroundColor: 'rgba(217,83,79,0.1)',
              fill: false,
              tension: 0.1
            },
            {
              label: 'Re-imports',
              data: reimportsData,
              borderColor: '#5cb85c',
              backgroundColor: 'rgba(92,184,92,0.1)',
              fill: false,
              tension: 0.1
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            tooltip: {
              enabled: true,
              mode: 'index',
              intersect: false
            },
            title: {
              display: true,
              text: 'Exports, Imports, and Re-imports Over Time'
            }
          },
          interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false
          },
          scales: {
            x: { title: { display: true, text: 'Period' } },
            y: { title: { display: true, text: 'Amount (in million dollars)' } }
          }
        }
      });
    });
});