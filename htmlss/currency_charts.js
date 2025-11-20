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
    const includeTrade = document.getElementById('includeTradeToggle')?.checked || false;
    
    forecastSection.innerHTML = `
        <div class="forecast-header">
            🔮 2026 Exchange Rate Forecast
            <div style="float: right; font-size: 0.9em;">
                <label style="cursor: pointer; display: inline-flex; align-items: center; gap: 8px;">
                    <input type="checkbox" id="includeTradeToggle" ${includeTrade ? 'checked' : ''} style="cursor: pointer; width: 18px; height: 18px;">
                    <span>Include Trade Balance Impact</span>
                </label>
            </div>
        </div>
        <div class="loading">Loading forecast data...</div>
        <div id="tradeImpactMetrics" style="display: none; margin-top: 15px; padding: 15px; background: rgba(77, 166, 255, 0.1); border-radius: 8px; border-left: 4px solid #4da6ff;">
            <h4 style="margin-top: 0; color: #4da6ff;">📊 Trade Balance Impact Analysis</h4>
            <div id="tradeImpactContent" style="color: #C0C0C0; font-size: 0.95em;"></div>
        </div>
    `;

    // Re-attach toggle event listener
    document.getElementById('includeTradeToggle').addEventListener('change', function() {
        loadForecast(currency);
    });

    fetch(`/api/currency/forecast?currency=${currency}&include_trade=${includeTrade}`)
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
                <div class="forecast-header">
                    🔮 2026 Exchange Rate Forecast for ${data.currency_name}
                    <div style="float: right; font-size: 0.9em;">
                        <label style="cursor: pointer; display: inline-flex; align-items: center; gap: 8px;">
                            <input type="checkbox" id="includeTradeToggle" ${includeTrade ? 'checked' : ''} style="cursor: pointer; width: 18px; height: 18px;">
                            <span>Include Trade Balance Impact</span>
                        </label>
                    </div>
                </div>
                <div style="text-align: center; color: #C0C0C0; margin-bottom: 20px;">
                    <p style="font-size: 1.1em;">Forecasting Method: <strong style="color: #4da6ff;">${data.method}${includeTrade ? ' + Trade Balance Adjustment' : ''}</strong></p>
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

            // Re-attach toggle event listener
            setTimeout(() => {
                document.getElementById('includeTradeToggle')?.addEventListener('change', function() {
                    loadForecast(currency);
                });
            }, 0);
            
            // Load trade impact data if toggle is enabled
            if (includeTrade) {
                loadTradeImpact(currency);
            }

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

/**
 * Load and display trade balance impact analysis
 */
function loadTradeImpact(currency) {
    const metricsSection = document.getElementById('tradeImpactMetrics');
    const contentDiv = document.getElementById('tradeImpactContent');
    
    if (!metricsSection || !contentDiv) return;
    
    metricsSection.style.display = 'block';
    contentDiv.innerHTML = '<div class="loading">Analyzing trade balance impact...</div>';
    
    fetch(`/api/currency/trade_impact?currency=${currency}&period_quarters=8`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                contentDiv.innerHTML = `<div class="error-message">${data.error}</div>`;
                return;
            }
            
            const correlation = data.correlation || 0;
            const impactLevel = data.impact_level || 'Unknown';
            const tradeTrend = data.trade_balance_trend || 'Unknown';
            const interpretation = data.interpretation || 'No analysis available';
            
            // Determine correlation strength color
            let corrColor = '#4da6ff';
            if (Math.abs(correlation) > 0.7) corrColor = '#ff5252';
            else if (Math.abs(correlation) > 0.4) corrColor = '#ffa500';
            else corrColor = '#4caf50';
            
            contentDiv.innerHTML = `
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 15px;">
                    <div style="text-align: center; padding: 10px; background: rgba(0, 0, 0, 0.2); border-radius: 6px;">
                        <div style="font-size: 0.85em; color: #B0B0B0;">Correlation</div>
                        <div style="font-size: 1.5em; font-weight: bold; color: ${corrColor};">${correlation.toFixed(3)}</div>
                    </div>
                    <div style="text-align: center; padding: 10px; background: rgba(0, 0, 0, 0.2); border-radius: 6px;">
                        <div style="font-size: 0.85em; color: #B0B0B0;">Impact Level</div>
                        <div style="font-size: 1.2em; font-weight: bold; color: ${corrColor};">${impactLevel}</div>
                    </div>
                    <div style="text-align: center; padding: 10px; background: rgba(0, 0, 0, 0.2); border-radius: 6px;">
                        <div style="font-size: 0.85em; color: #B0B0B0;">Trade Balance Trend</div>
                        <div style="font-size: 1.2em; font-weight: bold; color: #4da6ff;">${tradeTrend}</div>
                    </div>
                </div>
                <div style="padding: 10px; background: rgba(0, 0, 0, 0.2); border-radius: 6px;">
                    <div style="font-size: 0.9em; color: #B0B0B0; margin-bottom: 5px;">📝 Analysis:</div>
                    <div style="line-height: 1.6;">${interpretation}</div>
                </div>
            `;
        })
        .catch(error => {
            console.error('Error loading trade impact:', error);
            contentDiv.innerHTML = `<div class="error-message">Failed to load trade impact data</div>`;
        });
}
