// Helper to generate consistent colors for the pie slices
function getChartColors(n) {
  const colors = [
    '#003366', '#0066CC', '#3399FF', '#66B2FF', '#99CCFF',
    '#C0C0C0', '#808080', '#404040', '#1a4d7a', '#2d5f8d',
    '#4682B4', '#5F9EA0', '#6495ED', '#7B68EE', '#8B7D6B'
  ];
  const result = [];
  for (let i = 0; i < n; i++) {
    result.push(colors[i % colors.length]);
  }
  return result;
}

// Exports Share Pie Chart
function renderExportsSharePie() {
  fetch('/exports_share_data')
    .then(res => res.json())
    .then(data => {
      if (!data || data.length === 0) {
        console.warn('No exports share data available');
        return;
      }
      
      const labels = data.map(row => row.country);
      const shares = data.map(row => row.share);
      const bgColors = getChartColors(labels.length);

      const ctx = document.getElementById('exportsSharePie').getContext('2d');
      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: shares,
            backgroundColor: bgColors,
            borderColor: '#FFFFFF',
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            tooltip: {
              backgroundColor: 'rgba(0, 31, 63, 0.95)',
              titleColor: '#FFFFFF',
              bodyColor: '#FFFFFF',
              titleFont: {
                size: 14,
                weight: 'bold'
              },
              bodyFont: {
                size: 13
              },
              padding: 12,
              callbacks: {
                label: function(context) {
                  const idx = context.dataIndex;
                  const row = data[idx];
                  return [
                    `Country: ${row.country}`,
                    `Share: ${row.share}%`,
                    `Value: $${row.value}M`
                  ];
                }
              }
            },
            title: {
              display: false
            },
            legend: {
              position: 'bottom',
              labels: {
                color: '#FFFFFF',
                font: {
                  size: 13
                },
                padding: 15,
                boxWidth: 15
              }
            }
          }
        }
      });
    })
    .catch(error => {
      console.error('Error loading exports share data:', error);
    });
}

// Imports Share Pie Chart
function renderImportsSharePie() {
  fetch('/imports_share_data')
    .then(res => res.json())
    .then(data => {
      if (!data || data.length === 0) {
        console.warn('No imports share data available');
        return;
      }
      
      const labels = data.map(row => row.country);
      const shares = data.map(row => row.share);
      const bgColors = getChartColors(labels.length);

      const ctx = document.getElementById('importsSharePie').getContext('2d');
      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: shares,
            backgroundColor: bgColors,
            borderColor: '#FFFFFF',
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            tooltip: {
              backgroundColor: 'rgba(0, 31, 63, 0.95)',
              titleColor: '#FFFFFF',
              bodyColor: '#FFFFFF',
              titleFont: {
                size: 14,
                weight: 'bold'
              },
              bodyFont: {
                size: 13
              },
              padding: 12,
              callbacks: {
                label: function(context) {
                  const idx = context.dataIndex;
                  const row = data[idx];
                  return [
                    `Country: ${row.country}`,
                    `Share: ${row.share}%`,
                    `Value: $${row.value}M`,
                    `Change 1: ${row.change1}`,
                    `Change 2: ${row.change2}`
                  ];
                }
              }
            },
            title: {
              display: false
            },
            legend: {
              position: 'bottom',
              labels: {
                color: '#FFFFFF',
                font: {
                  size: 13
                },
                padding: 15,
                boxWidth: 15
              }
            }
          }
        }
      });
    })
    .catch(error => {
      console.error('Error loading imports share data:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
  renderExportsSharePie();
  renderImportsSharePie();
});