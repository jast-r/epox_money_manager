let salesChart;
let customersChart;

function getDateRange(period, startDate = new Date()) {
    let firstDay, lastDay;
    const date = new Date(startDate);

    switch (period) {
        case 'week':
            firstDay = new Date(date);
            firstDay.setDate(date.getDate() - date.getDay() + (date.getDay() === 0 ? -6 : 1));
            lastDay = new Date(firstDay);
            lastDay.setDate(lastDay.getDate() + 6);
            break;
        case 'month':
            firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
            lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
            break;
        case 'year':
            firstDay = new Date(date.getFullYear(), 0, 1);
            lastDay = new Date(date.getFullYear(), 11, 31);
            break;
    }

    return {
        firstDay: formatDateForDjango(firstDay),
        lastDay: formatDateForDjango(lastDay)
    };
}

function formatDateForDjango(date) {
    const offset = date.getTimezoneOffset();
    const localDate = new Date(date.getTime() - (offset * 60 * 1000));
    return localDate.toISOString().split('T')[0];
}

function drawCharts(data, labels) {
    createChart('salesChart', data, labels,
        ['revenue', 'profit'],
        ['Выручка', 'Прибыль'],
        ['rgb(0, 18, 176)', 'rgb(0, 176, 18)'],
        'line'
    );
    createChart('customersChart', data, labels,
        ['customers_count'],
        ['Клиенты'],
        ['rgb(75, 192, 192)'],
        'bar'
    );
}

function createChart(chartName, chartData, labels, dataKeys, dataLabels, colors, type) {
    const ctx = document.getElementById(chartName).getContext('2d');
    const datasets = dataKeys.map((key, index) => ({
        label: dataLabels[index],
        data: chartData.map(item => item[key]),
        borderColor: colors[index],
        backgroundColor: type === 'bar' ? colors[index] : undefined,
        tension: 0.2,
        borderRadius: type === 'bar' ? 10 : undefined
    }));

    const chart = new Chart(ctx, {
        type: type,
        data: { labels, datasets },
        options: {
            plugins: { legend: { display: false } },
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: chartName === 'salesChart' ? 200 : 1 }
                },
                x: { grid: { display: chartName === 'salesChart' } }
            }
        },
        tooltips: {
            callbacks: {
                label: function (item, data) {
                    const label = data.datasets[item.datasetIndex].label || '';
                    const yLabel = item.yLabel;
                    return data.datasets.length > 1 ? `${label}: ${yLabel}` : yLabel;
                }
            }
        }
    });

    if (chartName === 'salesChart') salesChart = chart;
    if (chartName === 'customersChart') customersChart = chart;
}
