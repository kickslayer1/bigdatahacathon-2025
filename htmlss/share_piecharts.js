// Helper to generate random colors for the pie slices
function getRandomColors(n) {
  const colors = [];
  for (let i = 0; i < n; i++) {
    colors.push(`hsl(${Math.floor(360 * Math.random())},70%,60%)`);
  }
  return colors;
}

// Exports Share Pie Chart
function renderExportsSharePie() {
  fetch('/exports_share_data')
    .then(res => res.json())
    .then(data => {
      const labels = data.map(row => row.country);
      const shares = data.map(row => row.share);
      const bgColors = getRandomColors(labels.length);

      const ctx = document.getElementById('exportsSharePie').getContext('2d');
      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: shares,
            backgroundColor: bgColors
          }]
        },
        options: {
          plugins: {
            tooltip: {
              callbacks: {
                label: function(context) {
                  const idx = context.dataIndex;
                  const row = data[idx];
                  return [
                    `Country: ${row.country}`,
                    `Share: ${row.share}%`,
                    `Value: $${row.value}M`,
                    `Change1: ${row.change1}`,
                    `Change2: ${row.change2}`
                  ];
                }
              }
            },
            title: {
              display: true,
              text: 'Exports Share by Country'
            }
          }
        }
      });
    });
}

// Imports Share Pie Chart
function renderImportsSharePie() {
  fetch('/imports_share_data')
    .then(res => res.json())
    .then(data => {
      const labels = data.map(row => row.country);
      const shares = data.map(row => row.share);
      const bgColors = getRandomColors(labels.length);

      const ctx = document.getElementById('importsSharePie').getContext('2d');
      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: shares,
            backgroundColor: bgColors
          }]
        },
        options: {
          plugins: {
            tooltip: {
              callbacks: {
                label: function(context) {
                  const idx = context.dataIndex;
                  const row = data[idx];
                  return [
                    `Country: ${row.country}`,
                    `Share: ${row.share}%`,
                    `Value: $${row.value}M`,
                    `Change1: ${row.change1}`,
                    `Change2: ${row.change2}`
                  ];
                }
              }
            },
            title: {
              display: true,
              text: 'Imports Share by Country'
            }
          }
        }
      });
    });
}

document.addEventListener('DOMContentLoaded', function() {
  renderExportsSharePie();
  renderImportsSharePie();
});