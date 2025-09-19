// Study Tracker Dashboard Charts

// Function to create a bar chart for study hours by subject
function createSubjectHoursChart(elementId, data) {
    const ctx = document.getElementById(elementId).getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.subjects,
            datasets: [{
                label: 'Study Hours',
                data: data.hours,
                backgroundColor: [
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)',
                    'rgba(255, 159, 64, 0.7)',
                    'rgba(199, 199, 199, 0.7)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(199, 199, 199, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Hours'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Subject'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Study Hours by Subject',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: false
                }
            }
        }
    });
}

// Function to create a line chart for productivity over time
function createProductivityChart(elementId, data) {
    const ctx = document.getElementById(elementId).getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Productivity Rating',
                data: data.ratings,
                fill: false,
                borderColor: 'rgba(75, 192, 192, 1)',
                tension: 0.1,
                pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 5,
                    title: {
                        display: true,
                        text: 'Rating (1-5)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Productivity Trend',
                    font: {
                        size: 16
                    }
                }
            }
        }
    });
}

// Function to create a pie chart for study time distribution
function createTimeDistributionChart(elementId, data) {
    const ctx = document.getElementById(elementId).getContext('2d');
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.subjects,
            datasets: [{
                data: data.percentages,
                backgroundColor: [
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)',
                    'rgba(255, 159, 64, 0.7)',
                    'rgba(199, 199, 199, 0.7)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(199, 199, 199, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Study Time Distribution',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    position: 'right'
                }
            }
        }
    });
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if chart data is available in the page
    if (typeof chartData !== 'undefined') {
        // Create charts with the data
        createSubjectHoursChart('subjectHoursChart', chartData.subjectHours);
        createProductivityChart('productivityChart', chartData.productivity);
        createTimeDistributionChart('timeDistributionChart', chartData.timeDistribution);
    }
});