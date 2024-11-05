document.addEventListener('DOMContentLoaded', function() {
    fetchData().then(data => {
        drawChart(data);
    });
});

function drawChart(data) {
    const ctx = document.getElementById('stockChart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates, // X轴标签
            datasets: [{
                label: 'Stock Price',
                data: data.prices, // Y轴数据
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Price'
                    }
                }
            }
        }
    });
}