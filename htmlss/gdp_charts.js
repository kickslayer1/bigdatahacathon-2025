// GDP Visualization Charts for Rwanda Trade Intelligence Dashboard

// Color palette for consistency
const gdpColors = {
    agriculture: 'rgba(34, 139, 34, 0.8)',      // Forest green
    industry: 'rgba(255, 140, 0, 0.8)',        // Dark orange
    services: 'rgba(30, 144, 255, 0.8)',       // Dodger blue
    taxes: 'rgba(220, 20, 60, 0.8)',           // Crimson
    mining: 'rgba(255, 215, 0, 0.8)',          // Gold
    construction: 'rgba(139, 69, 19, 0.8)',    // Saddle brown
    wholesale: 'rgba(75, 0, 130, 0.8)',        // Indigo
    transport: 'rgba(0, 128, 128, 0.8)'        // Teal
};

// Fetch GDP main sector data and create sector comparison chart
async function createGDPSectorChart(canvasId) {
    try {
        const response = await fetch('/gdp_main_data');
        const data = await response.json();
        
        if (data.error) {
            console.error('Error fetching GDP data:', data.error);
            return;
        }
        
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        // Prepare data for chart
        const labels = [];
        const datasets = [];
        
        // Get all quarter columns (Q2020Q1 through Q2025Q1)
        const quarterColumns = Object.keys(data[0]).filter(key => key.startsWith('Q'));
        
        // Create labels from quarters
        quarterColumns.forEach(col => {
            labels.push(col.substring(1)); // Remove 'Q' prefix
        });
        
        // Create dataset for each sector
        data.forEach(sector => {
            const sectorData = quarterColumns.map(col => parseFloat(sector[col]) || 0);
            const sectorName = sector.items;
            
            // Assign color based on sector name
            let color;
            if (sectorName.includes('AGRICULTURE')) color = gdpColors.agriculture;
            else if (sectorName.includes('INDUSTRY')) color = gdpColors.industry;
            else if (sectorName.includes('SERVICES')) color = gdpColors.services;
            else if (sectorName.includes('Taxes')) color = gdpColors.taxes;
            else color = 'rgba(128, 128, 128, 0.8)';
            
            datasets.push({
                label: sectorName,
                data: sectorData,
                borderColor: color,
                backgroundColor: color.replace('0.8', '0.2'),
                borderWidth: 3,
                tension: 0.4,
                fill: false
            });
        });
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'GDP by Major Sectors (2020-2025)',
                        color: '#FFFFFF',
                        font: { size: 18, weight: 'bold' }
                    },
                    legend: {
                        display: true,
                        position: 'bottom',
                        labels: { color: '#FFFFFF', font: { size: 12 } }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': RWF ' + context.parsed.y.toFixed(0) + ' billion';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: 'Quarter', color: '#FFFFFF', font: { size: 14 } },
                        ticks: { 
                            color: '#FFFFFF',
                            maxRotation: 45,
                            minRotation: 45
                        },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    },
                    y: {
                        title: { display: true, text: 'GDP (Billion RWF)', color: '#FFFFFF', font: { size: 14 } },
                        ticks: { color: '#FFFFFF' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating GDP sector chart:', error);
    }
}

// Create GDP growth analysis chart
async function createGDPGrowthChart(canvasId) {
    try {
        const response = await fetch('/gdp_growth_analysis');
        const data = await response.json();
        
        if (data.error) {
            console.error('Error fetching growth analysis:', data.error);
            return;
        }
        
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        // Prepare data for bar chart
        const labels = data.map(item => item.sector.replace('AGRICULTURE, FORESTRY & FISHING', 'Agriculture')
                                                      .replace('INDUSTRY', 'Industry')
                                                      .replace('SERVICES', 'Services')
                                                      .replace('Taxes less subsidies on products', 'Taxes'));
        const growthPercentages = data.map(item => item.growth_percent);
        
        // Color bars based on growth rate
        const barColors = growthPercentages.map(growth => {
            if (growth >= 150) return 'rgba(34, 139, 34, 0.8)';      // Dark green for high growth
            if (growth >= 100) return 'rgba(50, 205, 50, 0.8)';      // Lime green
            if (growth >= 50) return 'rgba(255, 215, 0, 0.8)';       // Gold
            return 'rgba(255, 140, 0, 0.8)';                         // Orange
        });
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Growth Rate (%)',
                    data: growthPercentages,
                    backgroundColor: barColors,
                    borderColor: barColors.map(c => c.replace('0.8', '1')),
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'GDP Growth by Sector (2020Q1 - 2025Q1)',
                        color: '#FFFFFF',
                        font: { size: 18, weight: 'bold' }
                    },
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Growth: ' + context.parsed.y.toFixed(2) + '%';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: '#FFFFFF', font: { size: 12 } },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    },
                    y: {
                        title: { display: true, text: 'Growth Rate (%)', color: '#FFFFFF', font: { size: 14 } },
                        ticks: { color: '#FFFFFF' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating GDP growth chart:', error);
    }
}

// Create top subsectors growth chart
async function createTopSubsectorsChart(canvasId, topN = 10) {
    try {
        const response = await fetch('/gdp_subsector_growth');
        const data = await response.json();
        
        if (data.error) {
            console.error('Error fetching subsector data:', data.error);
            return;
        }
        
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        // Get top N growing subsectors
        const topSubsectors = data.slice(0, topN);
        
        const labels = topSubsectors.map(item => {
            // Shorten long names
            let name = item.subsector;
            if (name.length > 30) {
                name = name.substring(0, 27) + '...';
            }
            return name;
        });
        const growthPercentages = topSubsectors.map(item => item.growth_percent);
        
        // Color gradient from green to yellow
        const barColors = topSubsectors.map((item, index) => {
            const intensity = 1 - (index / topN);
            return `rgba(${Math.floor(255 * (1 - intensity))}, ${Math.floor(200 * intensity + 55)}, 34, 0.8)`;
        });
        
        new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Growth Rate (%)',
                    data: growthPercentages,
                    backgroundColor: barColors,
                    borderColor: barColors.map(c => c.replace('0.8', '1')),
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                plugins: {
                    title: {
                        display: true,
                        text: 'Top 10 High-Growth Subsectors (2020-2025)',
                        color: '#FFFFFF',
                        font: { size: 18, weight: 'bold' }
                    },
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.parsed.x.toFixed(2) + '%';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: 'Growth Rate (%)', color: '#FFFFFF', font: { size: 14 } },
                        ticks: { color: '#FFFFFF' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        beginAtZero: true
                    },
                    y: {
                        ticks: { 
                            color: '#FFFFFF',
                            font: { size: 11 }
                        },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating top subsectors chart:', error);
    }
}

// Create GDP-Export correlation chart
async function createGDPExportCorrelationChart(canvasId) {
    try {
        const response = await fetch('/gdp_export_correlation');
        const data = await response.json();
        
        if (data.error) {
            console.error('Error fetching correlation data:', data.error);
            return;
        }
        
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        // Prepare GDP quarterly data
        const gdpLabels = data.gdp_industry.quarterly_values.map(item => item.quarter);
        const gdpValues = data.gdp_industry.quarterly_values.map(item => item.value);
        
        // Prepare export yearly data (we'll need to map to quarters for visualization)
        const exportYears = data.exports.yearly_values.map(item => item.year);
        const exportValues = data.exports.yearly_values.map(item => item.value);
        
        // Create dual-axis chart
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: gdpLabels,
                datasets: [
                    {
                        label: 'Industry GDP (Billion RWF)',
                        data: gdpValues,
                        borderColor: gdpColors.industry,
                        backgroundColor: gdpColors.industry.replace('0.8', '0.2'),
                        borderWidth: 3,
                        tension: 0.4,
                        yAxisID: 'y',
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'GDP vs Export Growth Correlation',
                        color: '#FFFFFF',
                        font: { size: 18, weight: 'bold' }
                    },
                    legend: {
                        display: true,
                        position: 'bottom',
                        labels: { color: '#FFFFFF', font: { size: 12 } }
                    },
                    subtitle: {
                        display: data.analysis ? true : false,
                        text: data.analysis ? `GDP Growth: ${data.analysis.gdp_growth_trend}% | Export Growth: ${data.analysis.export_growth_trend}% | Correlation: ${data.analysis.correlation_strength}` : '',
                        color: '#FFD700',
                        font: { size: 14 }
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: 'Quarter', color: '#FFFFFF', font: { size: 14 } },
                        ticks: { 
                            color: '#FFFFFF',
                            maxRotation: 45,
                            minRotation: 45
                        },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: { display: true, text: 'Industry GDP (Billion RWF)', color: '#FFFFFF', font: { size: 14 } },
                        ticks: { color: '#FFFFFF' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating correlation chart:', error);
    }
}

// Initialize all GDP charts when called
function initializeGDPCharts(config) {
    if (config.sectorChart) {
        createGDPSectorChart(config.sectorChart);
    }
    if (config.growthChart) {
        createGDPGrowthChart(config.growthChart);
    }
    if (config.subsectorsChart) {
        createTopSubsectorsChart(config.subsectorsChart, config.topN || 10);
    }
    if (config.correlationChart) {
        createGDPExportCorrelationChart(config.correlationChart);
    }
}
