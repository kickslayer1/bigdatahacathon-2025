/**
 * Currency Analysis Visualization Script
 * Handles Chart.js visualizations for exchange rate analysis
 */

let historicalChart = null;
let spreadChart = null;
let forecastChart = null;

/**
 * Load all currency data and update visualizations
 */
function loadAllData() {
    const currency = document.getElementById('currencySelect').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    loadStatistics(currency, startDate, endDate);
    loadHistoricalChart(currency, startDate, endDate);
    loadSpreadChart(currency, startDate, endDate);
    loadForecast(currency);
}

/**
 * Load and display currency statistics
 */
function loadStatistics(currency, startDate, endDate) {
    const statsGrid = document.getElementById('statsGrid');
    statsGrid.innerHTML = '<div class="loading">Loading statistics...</div>';

    // Calculate period in days
    const start = new Date(startDate);
    const end = new Date(endDate);
    const periodDays = Math.floor((end - start) / (1000 * 60 * 60 * 24));

    fetch(`/api/currency/statistics?currency=${currency}&period_days=${periodDays}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                statsGrid.innerHTML = `<div class="error-message">${data.error}</div>`;
                return;
            }

            statsGrid.innerHTML = `
                <div class="stat-card">
                    <h3>Current Exchange Rate</h3>
                    <div class="stat-value">${data.current_average.toFixed(2)}</div>
                    <div class="stat-label">RWF per ${currency}</div>
                    <div class="stat-label" style="margin-top: 8px; font-size: 0.85em;">
                        As of ${data.end_date}
                    </div>
                </div>

                <div class="stat-card">
                    <h3>Period Change</h3>
                    <div class="stat-value">${data.period_change.toFixed(2)}</div>
                    <div class="stat-label">RWF Change</div>
                    <div class="stat-change ${data.period_change_percent > 0 ? 'positive' : 'negative'}">
                        ${data.period_change_percent > 0 ? '+' : ''}${data.period_change_percent.toFixed(2)}%
                    </div>
                </div>

                <div class="stat-card">
                    <h3>Volatility</h3>
                    <div class="stat-value">${data.volatility.toFixed(2)}%</div>
                    <div class="stat-label">Price Fluctuation</div>
                    <div class="stat-label" style="margin-top: 8px; font-size: 0.85em;">
                        ${data.volatility < 1 ? 'Low' : data.volatility < 2 ? 'Moderate' : 'High'} volatility
                    </div>
                </div>

                <div class="stat-card">
                    <h3>Exchange Trend</h3>
                    <div class="stat-value">${data.trend.toUpperCase()}</div>
                    <div class="stat-label">RWF ${data.trend === 'depreciating' ? 'Weakening' : 'Strengthening'}</div>
                    <div class="stat-label" style="margin-top: 8px; font-size: 0.85em;">
                        Trend strength: ${data.trend_strength.toFixed(2)}%
                    </div>
                </div>

                <div class="stat-card">
                    <h3>Min / Max Rate</h3>
                    <div class="stat-value" style="font-size: 1.3em;">
                        ${data.min_rate.toFixed(2)} / ${data.max_rate.toFixed(2)}
                    </div>
                    <div class="stat-label">Period Range (RWF)</div>
                    <div class="stat-label" style="margin-top: 8px; font-size: 0.85em;">
                        Range: ${(data.max_rate - data.min_rate).toFixed(2)} RWF
                    </div>
                </div>

                <div class="stat-card">
                    <h3>Average Rate</h3>
                    <div class="stat-value">${data.mean_rate.toFixed(2)}</div>
                    <div class="stat-label">Period Mean (RWF)</div>
                    <div class="stat-label" style="margin-top: 8px; font-size: 0.85em;">
                        Std Dev: ${data.std_rate.toFixed(2)}
                    </div>
                </div>
            `;
        })
        .catch(error => {
            console.error('Error loading statistics:', error);
            statsGrid.innerHTML = '<div class="error-message">Error loading statistics. Please try again.</div>';
        });
}

/**
 * Load and display historical exchange rate chart
 */
function loadHistoricalChart(currency, startDate, endDate) {
    fetch(`/api/currency/historical?currency=${currency}&start_date=${startDate}&end_date=${endDate}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                return;
            }

            const ctx = document.getElementById('historicalChart').getContext('2d');

            // Destroy existing chart
            if (historicalChart) {
                historicalChart.destroy();
            }

            historicalChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Buying Rate',
                            data: data.buying_rate,
                            borderColor: '#4caf50',
                            backgroundColor: 'rgba(76, 175, 80, 0.1)',
                            borderWidth: 2,
                            pointRadius: 0,
                            tension: 0.1
                        },
                        {
                            label: 'Average Rate',
                            data: data.average_rate,
                            borderColor: '#4da6ff',
                            backgroundColor: 'rgba(77, 166, 255, 0.1)',
                            borderWidth: 3,
                            pointRadius: 0,
                            tension: 0.1
                        },
                        {
                            label: 'Selling Rate',
                            data: data.selling_rate,
                            borderColor: '#ff5252',
                            backgroundColor: 'rgba(255, 82, 82, 0.1)',
                            borderWidth: 2,
                            pointRadius: 0,
                            tension: 0.1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                color: '#C0C0C0',
                                font: { size: 12 }
                            }
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                            callbacks: {
                                label: function(context) {
                                    return context.dataset.label + ': ' + context.parsed.y.toFixed(2) + ' RWF';
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Date',
                                color: '#C0C0C0'
                            },
                            ticks: {
                                color: '#C0C0C0',
                                maxTicksLimit: 12
                            },
                            grid: {
                                color: 'rgba(192, 192, 192, 0.1)'
                            }
                        },
                        y: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Exchange Rate (RWF)',
                                color: '#C0C0C0'
                            },
                            ticks: {
                                color: '#C0C0C0',
                                callback: function(value) {
                                    return value.toFixed(0);
                                }
                            },
                            grid: {
                                color: 'rgba(192, 192, 192, 0.1)'
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error loading historical chart:', error);
        });
}

/**
 * Load and display spread analysis chart
 */
function loadSpreadChart(currency, startDate, endDate) {
    fetch(`/api/currency/historical?currency=${currency}&start_date=${startDate}&end_date=${endDate}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                return;
            }

            // Calculate spread
            const spread = data.selling_rate.map((selling, index) => 
                selling - data.buying_rate[index]
            );

            const ctx = document.getElementById('spreadChart').getContext('2d');

            // Destroy existing chart
            if (spreadChart) {
                spreadChart.destroy();
            }

            spreadChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Spread (Selling - Buying)',
                            data: spread,
                            borderColor: '#ff9800',
                            backgroundColor: 'rgba(255, 152, 0, 0.2)',
                            borderWidth: 2,
                            pointRadius: 0,
                            tension: 0.1,
                            fill: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                color: '#C0C0C0',
                                font: { size: 12 }
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return 'Spread: ' + context.parsed.y.toFixed(2) + ' RWF';
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Date',
                                color: '#C0C0C0'
                            },
                            ticks: {
                                color: '#C0C0C0',
                                maxTicksLimit: 12
                            },
                            grid: {
                                color: 'rgba(192, 192, 192, 0.1)'
                            }
                        },
                        y: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Spread (RWF)',
                                color: '#C0C0C0'
                            },
                            ticks: {
                                color: '#C0C0C0'
                            },
                            grid: {
                                color: 'rgba(192, 192, 192, 0.1)'
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error loading spread chart:', error);
        });
}

/**
 * Load and display 2026 forecast
 */
function loadForecast(currency) {
    const forecastSection = document.getElementById('forecastSection');
    forecastSection.innerHTML = `
        <div class="forecast-header">🔮 2026 Exchange Rate Forecast</div>
        <div class="loading">Loading forecast data...</div>
    `;

    fetch(`/api/currency/forecast?currency=${currency}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                forecastSection.innerHTML = `
                    <div class="forecast-header">🔮 2026 Exchange Rate Forecast</div>
                    <div class="error-message">${data.error}</div>
                `;
                return;
            }

            // Display forecast summary
            let summaryHTML = `
                <div class="forecast-header">🔮 2026 Exchange Rate Forecast for ${data.currency_name}</div>
                <div style="text-align: center; color: #C0C0C0; margin-bottom: 20px;">
                    <p style="font-size: 1.1em;">Forecasting Method: <strong style="color: #4da6ff;">${data.method}</strong></p>
                    <p>Current Rate: <strong>${data.current_rate.toFixed(2)} RWF</strong> (${data.current_date})</p>
            `;

            if (data['2026_statistics']) {
                const stats = data['2026_statistics'];
                const change = data.projected_change_percent || 0;
                summaryHTML += `
                    <p>Projected 2026 Average: <strong style="color: #4da6ff;">${stats.mean_rate.toFixed(2)} RWF</strong></p>
                    <p>Projected Change: <strong style="color: ${change > 0 ? '#ff5252' : '#4caf50'};">
                        ${change > 0 ? '+' : ''}${change.toFixed(2)}%
                    </strong></p>
                `;
            }

            summaryHTML += '</div>';

            // Monthly predictions
            if (data.predictions && data.predictions.length > 0) {
                summaryHTML += '<div class="forecast-grid">';
                
                data.predictions.forEach(pred => {
                    summaryHTML += `
                        <div class="forecast-card">
                            <div class="forecast-month">${pred.month_name}</div>
                            <div class="forecast-rate">${pred.predicted_rate.toFixed(2)}</div>
                            <div style="color: #B0B0B0; font-size: 0.9em;">RWF per ${currency}</div>
                        </div>
                    `;
                });

                summaryHTML += '</div>';
            }

            forecastSection.innerHTML = summaryHTML;

            // Update forecast chart
            loadForecastChart(currency, data);
        })
        .catch(error => {
            console.error('Error loading forecast:', error);
            forecastSection.innerHTML = `
                <div class="forecast-header">🔮 2026 Exchange Rate Forecast</div>
                <div class="error-message">Error loading forecast. Please try again.</div>
            `;
        });
}

/**
 * Load and display forecast chart with historical data
 */
function loadForecastChart(currency, forecastData) {
    // Get recent historical data (last 2 years)
    const endDate = new Date().toISOString().split('T')[0];
    const startDate = new Date();
    startDate.setFullYear(startDate.getFullYear() - 2);
    const startDateStr = startDate.toISOString().split('T')[0];

    fetch(`/api/currency/historical?currency=${currency}&start_date=${startDateStr}&end_date=${endDate}`)
        .then(response => response.json())
        .then(historicalData => {
            if (historicalData.error) {
                console.error('Error:', historicalData.error);
                return;
            }

            // Combine historical and forecast data
            const allLabels = [...historicalData.labels, ...forecastData.daily_forecast.dates];
            const historicalRates = [...historicalData.average_rate, ...Array(forecastData.daily_forecast.dates.length).fill(null)];
            const forecastRates = [...Array(historicalData.labels.length).fill(null), ...forecastData.daily_forecast.rates];

            const ctx = document.getElementById('forecastChart').getContext('2d');

            // Destroy existing chart
            if (forecastChart) {
                forecastChart.destroy();
            }

            const datasets = [
                {
                    label: 'Historical Data',
                    data: historicalRates,
                    borderColor: '#4da6ff',
                    backgroundColor: 'rgba(77, 166, 255, 0.1)',
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.1
                },
                {
                    label: '2026 Forecast',
                    data: forecastRates,
                    borderColor: '#ff9800',
                    backgroundColor: 'rgba(255, 152, 0, 0.1)',
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.1,
                    borderDash: [5, 5]
                }
            ];

            // Add confidence intervals if available
            if (forecastData.daily_forecast.lower_bound && forecastData.daily_forecast.upper_bound) {
                const lowerBound = [...Array(historicalData.labels.length).fill(null), ...forecastData.daily_forecast.lower_bound];
                const upperBound = [...Array(historicalData.labels.length).fill(null), ...forecastData.daily_forecast.upper_bound];

                datasets.push({
                    label: 'Confidence Interval (Lower)',
                    data: lowerBound,
                    borderColor: 'rgba(255, 152, 0, 0.3)',
                    backgroundColor: 'rgba(255, 152, 0, 0.05)',
                    borderWidth: 1,
                    pointRadius: 0,
                    tension: 0.1,
                    borderDash: [2, 2],
                    fill: '+1'
                });

                datasets.push({
                    label: 'Confidence Interval (Upper)',
                    data: upperBound,
                    borderColor: 'rgba(255, 152, 0, 0.3)',
                    backgroundColor: 'rgba(255, 152, 0, 0.05)',
                    borderWidth: 1,
                    pointRadius: 0,
                    tension: 0.1,
                    borderDash: [2, 2]
                });
            }

            forecastChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: allLabels,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                color: '#C0C0C0',
                                font: { size: 12 },
                                filter: function(item) {
                                    // Hide confidence interval from legend
                                    return !item.text.includes('Confidence Interval');
                                }
                            }
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                            callbacks: {
                                label: function(context) {
                                    if (context.parsed.y === null) return null;
                                    return context.dataset.label + ': ' + context.parsed.y.toFixed(2) + ' RWF';
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Date',
                                color: '#C0C0C0'
                            },
                            ticks: {
                                color: '#C0C0C0',
                                maxTicksLimit: 15
                            },
                            grid: {
                                color: 'rgba(192, 192, 192, 0.1)'
                            }
                        },
                        y: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Exchange Rate (RWF)',
                                color: '#C0C0C0'
                            },
                            ticks: {
                                color: '#C0C0C0'
                            },
                            grid: {
                                color: 'rgba(192, 192, 192, 0.1)'
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error loading forecast chart:', error);
        });
}
