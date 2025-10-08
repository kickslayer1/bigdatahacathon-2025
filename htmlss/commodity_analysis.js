// Commodity Analysis JavaScript
let commodityChart = null;
let importCommodityChart = null;

// Initialize commodity analysis when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadCommodityOptions();
    loadImportCommodityOptions();
    setupCommoditySelector();
    setupImportCommoditySelector();
});

// Load available commodities for dropdown
async function loadCommodityOptions() {
    try {
        const response = await fetch('/commodity_options');
        const data = await response.json();
        
        const commoditySelect = document.getElementById('commoditySelect');
        commoditySelect.innerHTML = '<option value="">Select a commodity...</option>';
        
        data.commodities.forEach(commodity => {
            const option = document.createElement('option');
            option.value = commodity;
            option.textContent = commodity;
            commoditySelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading commodity options:', error);
    }
}

// Load available import commodities for dropdown
async function loadImportCommodityOptions() {
    try {
        const response = await fetch('/import_commodity_options');
        const data = await response.json();
        
        const importCommoditySelect = document.getElementById('importCommoditySelect');
        importCommoditySelect.innerHTML = '<option value="">Select a commodity...</option>';
        
        data.commodities.forEach(commodity => {
            const option = document.createElement('option');
            option.value = commodity;
            option.textContent = commodity;
            importCommoditySelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading import commodity options:', error);
    }
}

// Setup commodity selector event listener
function setupCommoditySelector() {
    const commoditySelect = document.getElementById('commoditySelect');
    commoditySelect.addEventListener('change', function() {
        const selectedCommodity = this.value;
        if (selectedCommodity) {
            loadCommodityTimeline(selectedCommodity);
        } else {
            clearCommodityChart();
        }
    });
}

// Setup import commodity selector event listener
function setupImportCommoditySelector() {
    const importCommoditySelect = document.getElementById('importCommoditySelect');
    importCommoditySelect.addEventListener('change', function() {
        const selectedCommodity = this.value;
        if (selectedCommodity) {
            loadImportCommodityTimeline(selectedCommodity);
        } else {
            clearImportCommodityChart();
        }
    });
}

// Load and display commodity timeline data
async function loadCommodityTimeline(commodity) {
    try {
        const response = await fetch(`/commodity_timeline/${encodeURIComponent(commodity)}`);
        const data = await response.json();
        
        displayCommodityChart(data);
        displayCommodityTable(data);
    } catch (error) {
        console.error('Error loading commodity timeline:', error);
        document.getElementById('commodityError').innerHTML = 
            '<p style="color: red;">Error loading commodity data. Please try again.</p>';
    }
}

// Load and display import commodity timeline data
async function loadImportCommodityTimeline(commodity) {
    try {
        const response = await fetch(`/import_commodity_timeline/${encodeURIComponent(commodity)}`);
        const data = await response.json();
        
        displayImportCommodityChart(data);
        displayImportCommodityTable(data);
    } catch (error) {
        console.error('Error loading import commodity timeline:', error);
        document.getElementById('importCommodityError').innerHTML = 
            '<p style="color: red;">Error loading import commodity data. Please try again.</p>';
    }
}

// Display commodity timeline chart
function displayCommodityChart(data) {
    const ctx = document.getElementById('commodityChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (commodityChart) {
        commodityChart.destroy();
    }
    
    const labels = data.timeline.map(item => item.quarter);
    const actualValues = data.timeline.filter(item => item.is_actual).map(item => item.value);
    const predictionValues = data.timeline.map(item => item.is_prediction ? item.value : null);
    const upperBounds = data.timeline.map(item => item.upper_bound || null);
    const lowerBounds = data.timeline.map(item => item.lower_bound || null);
    
    commodityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Actual Exports (USD)',
                    data: data.timeline.map(item => item.is_actual ? item.value : null),
                    borderColor: '#001f3f',
                    backgroundColor: 'rgba(0, 31, 63, 0.1)',
                    borderWidth: 3,
                    fill: false,
                    tension: 0.4
                },
                {
                    label: 'ML Predictions (USD)',
                    data: predictionValues,
                    borderColor: '#ff6b9d',
                    backgroundColor: 'rgba(255, 107, 157, 0.1)',
                    borderWidth: 3,
                    borderDash: [10, 5],
                    fill: false,
                    tension: 0.4
                },
                {
                    label: 'Confidence Upper Bound',
                    data: upperBounds,
                    borderColor: '#ffccdd',
                    backgroundColor: 'rgba(255, 204, 221, 0.1)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                },
                {
                    label: 'Confidence Lower Bound',
                    data: lowerBounds,
                    borderColor: '#ffccdd',
                    backgroundColor: 'rgba(255, 204, 221, 0.1)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: `${data.commodity} - ML-Enhanced Export Timeline Trends`,
                    font: {
                        size: 16,
                        weight: 'bold'
                    },
                    color: '#001f3f'
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Quarter',
                        font: {
                            weight: 'bold'
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Export Value (USD)',
                        font: {
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + (value / 1000000).toFixed(1) + 'M';
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            },
            elements: {
                point: {
                    radius: function(context) {
                        const item = data.timeline[context.dataIndex];
                        return item && item.is_prediction ? 8 : 4;
                    },
                    backgroundColor: function(context) {
                        const item = data.timeline[context.dataIndex];
                        return item && item.is_prediction ? '#ff6b9d' : '#001f3f';
                    }
                }
            }
        }
    });
}

// Display commodity data table
function displayCommodityTable(data) {
    const tableContainer = document.getElementById('commodityTable');
    
    let tableHTML = `
        <h4>ML-Enhanced Timeline Analysis for ${data.commodity}</h4>
    `;
    
    // Display ML model information if available
    if (data.prediction_info && data.prediction_info.ml_enabled) {
        const perf = data.prediction_info.model_performance;
        const models = data.prediction_info.models_used;
        
        tableHTML += `
            <div style="background: #f0f8ff; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #001f3f;">
                <h5 style="color: #001f3f; margin-top: 0;">🤖 Machine Learning Model Performance</h5>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div>
                        <strong>Model Accuracy:</strong> ${perf ? perf.model_accuracy + '%' : 'N/A'}<br>
                        <strong>R² Score:</strong> ${perf ? perf.r2_score : 'N/A'}<br>
                        <strong>Mean Abs Error:</strong> ${perf ? '$' + (perf.mean_absolute_error/1000).toFixed(0) + 'K' : 'N/A'}
                    </div>
                    <div>
                        <strong>Prophet Model:</strong> ${models.prophet ? '✅ Active' : '❌ Failed'}<br>
                        <strong>Linear Regression:</strong> ${models.linear_regression ? '✅ Active' : '❌ Failed'}<br>
                        <strong>Ensemble Method:</strong> ${models.ensemble_method || 'Weighted Average'}
                    </div>
                </div>
            </div>
        `;
    }
    
    tableHTML += `
        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
            <thead>
                <tr style="background: #001f3f; color: #C0C0C0;">
                    <th style="padding: 12px; border: 1px solid #ddd;">Quarter</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Export Value (USD)</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Growth Rate</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Type</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Confidence</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    data.timeline.forEach((item, index) => {
        const growthRate = index > 0 ? 
            (((item.value - data.timeline[index - 1].value) / data.timeline[index - 1].value) * 100).toFixed(1) : 
            '---';
        
        let rowStyle, typeLabel, confidenceInfo;
        
        if (item.is_prediction) {
            rowStyle = 'background-color: rgba(255, 107, 157, 0.1);';
            
            if (item.fallback) {
                typeLabel = '<span style="color: #ff6b9d; font-weight: bold;">Simple Prediction</span>';
            } else {
                typeLabel = '<span style="color: #ff6b9d; font-weight: bold;">🤖 ML Prediction</span>';
            }
            
            confidenceInfo = item.confidence_level ? 
                `<span style="color: ${item.confidence_level === 'High' ? 'green' : item.confidence_level === 'Medium' ? 'orange' : 'red'};">
                    ${item.confidence_level}
                </span>` : 'N/A';
            
            // Add confidence bounds if available
            if (item.upper_bound && item.lower_bound) {
                confidenceInfo += `<br><small>±$${((item.upper_bound - item.lower_bound)/2/1000).toFixed(0)}K</small>`;
            }
        } else {
            rowStyle = index % 2 === 0 ? 'background-color: #f9f9f9;' : '';
            typeLabel = '<span style="color: #001f3f;">Historical Data</span>';
            confidenceInfo = '<span style="color: green;">Actual</span>';
        }
        
        tableHTML += `
            <tr style="${rowStyle}">
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">${item.quarter}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">$${item.value.toLocaleString()}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">${growthRate}%</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">${typeLabel}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">${confidenceInfo}</td>
            </tr>
        `;
    });
    
    tableHTML += `
            </tbody>
        </table>
    `;
    
    // Add prediction summary
    const predictions = data.timeline.filter(item => item.is_prediction);
    if (predictions.length > 0) {
        tableHTML += `
            <div style="margin-top: 15px; padding: 15px; background: rgba(255, 107, 157, 0.1); border-radius: 8px;">
                <strong>🎯 ML Prediction Summary:</strong>
                <ul style="margin: 10px 0;">
        `;
        
        predictions.forEach((pred, index) => {
            const prevQuarter = data.timeline[data.timeline.length - predictions.length + index - 1];
            if (prevQuarter) {
                const growth = ((pred.value - prevQuarter.value) / prevQuarter.value * 100).toFixed(1);
                tableHTML += `<li><strong>${pred.quarter}:</strong> $${pred.value.toLocaleString()} (${growth}% growth, ${pred.confidence_level || 'Medium'} confidence)</li>`;
            }
        });
        
        tableHTML += `
                </ul>
                <small style="color: #666;">
                    💡 Predictions generated using ensemble of Prophet time series forecasting and polynomial linear regression models.
                </small>
            </div>
        `;
    }
    
    tableContainer.innerHTML = tableHTML;
}

// Clear commodity chart
function clearCommodityChart() {
    if (commodityChart) {
        commodityChart.destroy();
        commodityChart = null;
    }
    document.getElementById('commodityTable').innerHTML = '';
    document.getElementById('commodityError').innerHTML = '';
}

// Clear import commodity chart
function clearImportCommodityChart() {
    if (importCommodityChart) {
        importCommodityChart.destroy();
        importCommodityChart = null;
    }
    document.getElementById('importCommodityTable').innerHTML = '';
    document.getElementById('importCommodityError').innerHTML = '';
}

// Display import commodity timeline chart
function displayImportCommodityChart(data) {
    const ctx = document.getElementById('importCommodityChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (importCommodityChart) {
        importCommodityChart.destroy();
    }
    
    const labels = data.timeline.map(item => item.quarter);
    const actualValues = data.timeline.filter(item => item.is_actual).map(item => item.value);
    const predictionValues = data.timeline.map(item => item.is_prediction ? item.value : null);
    const upperBounds = data.timeline.map(item => item.upper_bound || null);
    const lowerBounds = data.timeline.map(item => item.lower_bound || null);
    
    importCommodityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Actual Imports (USD)',
                    data: data.timeline.map(item => item.is_actual ? item.value : null),
                    borderColor: '#d2691e',
                    backgroundColor: 'rgba(210, 105, 30, 0.1)',
                    borderWidth: 3,
                    fill: false,
                    tension: 0.4
                },
                {
                    label: 'ML Predictions (USD)',
                    data: predictionValues,
                    borderColor: '#ff6b9d',
                    backgroundColor: 'rgba(255, 107, 157, 0.1)',
                    borderWidth: 3,
                    borderDash: [10, 5],
                    fill: false,
                    tension: 0.4
                },
                {
                    label: 'Confidence Upper Bound',
                    data: upperBounds,
                    borderColor: '#ffccdd',
                    backgroundColor: 'rgba(255, 204, 221, 0.1)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                },
                {
                    label: 'Confidence Lower Bound',
                    data: lowerBounds,
                    borderColor: '#ffccdd',
                    backgroundColor: 'rgba(255, 204, 221, 0.1)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: `${data.commodity} - ML-Enhanced Import Timeline Trends`,
                    font: {
                        size: 16,
                        weight: 'bold'
                    },
                    color: '#d2691e'
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Quarter',
                        font: {
                            weight: 'bold'
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Import Value (USD)',
                        font: {
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + (value / 1000000).toFixed(1) + 'M';
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            },
            elements: {
                point: {
                    radius: function(context) {
                        const item = data.timeline[context.dataIndex];
                        return item && item.is_prediction ? 8 : 4;
                    },
                    backgroundColor: function(context) {
                        const item = data.timeline[context.dataIndex];
                        return item && item.is_prediction ? '#ff6b9d' : '#d2691e';
                    }
                }
            }
        }
    });
}

// Display import commodity data table
function displayImportCommodityTable(data) {
    const tableContainer = document.getElementById('importCommodityTable');
    
    let tableHTML = `
        <h4>ML-Enhanced Import Timeline Analysis for ${data.commodity}</h4>
    `;
    
    // Display ML model information if available
    if (data.prediction_info && data.prediction_info.ml_enabled) {
        const perf = data.prediction_info.model_performance;
        const models = data.prediction_info.models_used;
        
        tableHTML += `
            <div style="background: #fff8dc; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #d2691e;">
                <h5 style="color: #d2691e; margin-top: 0;">🤖 Machine Learning Model Performance</h5>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div>
                        <strong>Model Accuracy:</strong> ${perf ? perf.model_accuracy + '%' : 'N/A'}<br>
                        <strong>R² Score:</strong> ${perf ? perf.r2_score : 'N/A'}<br>
                        <strong>Mean Abs Error:</strong> ${perf ? '$' + (perf.mean_absolute_error/1000).toFixed(0) + 'K' : 'N/A'}
                    </div>
                    <div>
                        <strong>Prophet Model:</strong> ${models.prophet ? '✅ Active' : '❌ Failed'}<br>
                        <strong>Linear Regression:</strong> ${models.linear_regression ? '✅ Active' : '❌ Failed'}<br>
                        <strong>Ensemble Method:</strong> ${models.ensemble_method || 'Weighted Average'}
                    </div>
                </div>
            </div>
        `;
    }
    
    tableHTML += `
        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
            <thead>
                <tr style="background: #d2691e; color: white;">
                    <th style="padding: 12px; border: 1px solid #ddd;">Quarter</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Import Value (USD)</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Growth Rate</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Type</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Confidence</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    data.timeline.forEach((item, index) => {
        const growthRate = index > 0 ? 
            (((item.value - data.timeline[index - 1].value) / data.timeline[index - 1].value) * 100).toFixed(1) : 
            '---';
        
        let rowStyle, typeLabel, confidenceInfo;
        
        if (item.is_prediction) {
            rowStyle = 'background-color: rgba(255, 107, 157, 0.1);';
            
            if (item.fallback) {
                typeLabel = '<span style="color: #ff6b9d; font-weight: bold;">Simple Prediction</span>';
            } else {
                typeLabel = '<span style="color: #ff6b9d; font-weight: bold;">🤖 ML Prediction</span>';
            }
            
            confidenceInfo = item.confidence_level ? 
                `<span style="color: ${item.confidence_level === 'High' ? 'green' : item.confidence_level === 'Medium' ? 'orange' : 'red'};">
                    ${item.confidence_level}
                </span>` : 'N/A';
            
            // Add confidence bounds if available
            if (item.upper_bound && item.lower_bound) {
                confidenceInfo += `<br><small>±$${((item.upper_bound - item.lower_bound)/2/1000).toFixed(0)}K</small>`;
            }
        } else {
            rowStyle = index % 2 === 0 ? 'background-color: #f9f9f9;' : '';
            typeLabel = '<span style="color: #d2691e;">Historical Data</span>';
            confidenceInfo = '<span style="color: green;">Actual</span>';
        }
        
        tableHTML += `
            <tr style="${rowStyle}">
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">${item.quarter}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">$${item.value.toLocaleString()}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">${growthRate}%</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">${typeLabel}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">${confidenceInfo}</td>
            </tr>
        `;
    });
    
    tableHTML += `
            </tbody>
        </table>
    `;
    
    // Add prediction summary
    const predictions = data.timeline.filter(item => item.is_prediction);
    if (predictions.length > 0) {
        tableHTML += `
            <div style="margin-top: 15px; padding: 15px; background: rgba(210, 105, 30, 0.1); border-radius: 8px;">
                <strong>🎯 ML Import Prediction Summary:</strong>
                <ul style="margin: 10px 0;">
        `;
        
        predictions.forEach((pred, index) => {
            const prevQuarter = data.timeline[data.timeline.length - predictions.length + index - 1];
            if (prevQuarter) {
                const growth = ((pred.value - prevQuarter.value) / prevQuarter.value * 100).toFixed(1);
                tableHTML += `<li><strong>${pred.quarter}:</strong> $${pred.value.toLocaleString()} (${growth}% growth, ${pred.confidence_level || 'Medium'} confidence)</li>`;
            }
        });
        
        tableHTML += `
                </ul>
                <small style="color: #666;">
                    💡 Import predictions generated using ensemble of Prophet time series forecasting and polynomial linear regression models.
                </small>
            </div>
        `;
    }
    
    tableContainer.innerHTML = tableHTML;
}