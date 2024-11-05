document.addEventListener('DOMContentLoaded', function() {
    loadComponent('navbar', 'components/navbar.html');
    loadComponent('footer', 'components/footer.html');
    loadComponent('chart', 'components/chart.html');
});

function loadComponent(id, url) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById(id).innerHTML = data;
            if (id === 'chart') {
                fetchData().then(data => {
                    drawChart(data);
                });
            }
        })
        .catch(error => console.error('Error loading component:', error));
}