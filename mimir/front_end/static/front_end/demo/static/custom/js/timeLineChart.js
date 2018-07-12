new Chart(document.getElementById("myChart"), {
    type: 'line',
    data: data,
    options: {
      title: {
        display: true,
        text: 'BTC Price Chart'
      },
      legend: { 
        display: true 
      },
    },
    scales: {
      xAxes: [{
        type: 'time',
        position: 'bottom',
        time: {
          tooltipFormat: "YYYY-MM-DD",
        },
      }],
    }
  });