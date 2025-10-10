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
  console.log('Attempting to render exports share pie chart...');
  
  const canvas = document.getElementById('exportsSharePie');
  if (!canvas) {
    console.error('Canvas element exportsSharePie not found!');
    return;
  }
  
  fetch('/exports_share_data')
    .then(res => {
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      return res.json();
    })
    .then(data => {
      console.log('Exports share data received:', data);
      
      if (!data || data.length === 0) {
        console.warn('No exports share data available');
        return;
      }
      
      const labels = data.map(row => row.country);
      const shares = data.map(row => row.share);
      const bgColors = getRandomColors(labels.length);

      const ctx = canvas.getContext('2d');
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
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            tooltip: {
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
              display: true,
              text: 'Exports Share by Country',
              color: '#C0C0C0'
            },
            legend: {
              labels: {
                color: '#C0C0C0'
              }
            }
          }
        }
      });
      console.log('Exports share pie chart rendered successfully');
    })
    .catch(error => {
      console.error('Error loading exports share data:', error);
    });
}

// Imports Share Pie Chart
function renderImportsSharePie() {
  console.log('Attempting to render imports share pie chart...');
  
  const canvas = document.getElementById('importsSharePie');
  if (!canvas) {
    console.error('Canvas element importsSharePie not found!');
    return;
  }
  
  fetch('/imports_share_data')
    .then(res => {
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      return res.json();
    })
    .then(data => {
      console.log('Imports share data received:', data);
      
      if (!data || data.length === 0) {
        console.warn('No imports share data available');
        return;
      }
      
      const labels = data.map(row => row.country);
      const shares = data.map(row => row.share);
      const bgColors = getRandomColors(labels.length);

      const ctx = canvas.getContext('2d');
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
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            tooltip: {
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
              display: true,
              text: 'Imports Share by Country',
              color: '#C0C0C0'
            },
            legend: {
              labels: {
                color: '#C0C0C0'
              }
            }
          }
        }
      });
      console.log('Imports share pie chart rendered successfully');
    })
    .catch(error => {
      console.error('Error loading imports share data:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM loaded, Chart.js available:', typeof Chart !== 'undefined');
  
  // Add a small delay to ensure everything is fully loaded
  setTimeout(() => {
    renderExportsSharePie();
    renderImportsSharePie();
  }, 500);
});