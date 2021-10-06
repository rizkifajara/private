window.onload = function () { 
  var lateralChart = echarts.init(document.getElementById('lateral'));
  var profileChart = echarts.init(document.getElementById('profile'));

  
lateralChart.showLoading()
profileChart.showLoading()

const callTrajectoryWell = (wellName) => {
  $.getJSON('/static/echart/trajectory.json', (response) => {
    dataLateral = response[wellName]['lateral'];
    dataProfile = response[wellName]['profile'];

    lateralEchart(dataLateral, lateralChart, wellName);
    profileEchart(dataProfile, profileChart, wellName);

    bottomDepth = dataLateral[dataLateral.length - 1].map((x) => {return x * 0.3048/111});
    // console.log(bottomDepth)
    return bottomDepth
  });
}

callTrajectoryWell('15/9-F-14')
//console.log(bottomDepth)

const lateralEchart = (data, chart, wellname) => {
  chart.hideLoading()

  var option = {
    title: {
      text: 'Lateral',
      left: 'center',
      subtext: `Data from well: ${wellname}`
    },
    grid: {
      left: 100,
      top: 80,
    },
    xAxis: [
      {
        name: 'West - East',
        nameLocation: 'middle',
        nameGap: 35,
        type: 'value',
        scale: true,
        axisLabel: {
          formatter: '{value} ft',
          rotate: 30,
          fontSize: 9
        },
        splitLine: {
          show: false
        }
      }
    ],
    yAxis: [
      {
        name: 'North - South',
        nameLocation: 'middle',
        nameGap: 50,
        type: 'value',
        scale: true,
        axisLabel: {
          formatter: '{value} ft',
          fontSize: 9
        },
        splitLine: {
          show: false
        }
      }
    ],
    legend: {
      left: 'center',
      bottom: 0
    },
    tooltip: {
      position: 'top',
      formatter: (params) => {
        return (
          `x: ${parseFloat(params.value[0]).toFixed(2)} <br/> y:  ${parseFloat(params.value[1]).toFixed(2)}`
        )
      },
      axisPointer: {
        show: true,
        type: 'cross',
        lineStyle: {
          type: 'dashed',
          width: 1
        }
      }
    },
    series: [
      {
        type: 'scatter',
        color: 'green',
        symbolSize: 3,
        data: data
      }, 
      {
        name: 'Top Depth',
        type: 'effectScatter',
        color: 'blue',
        emphasis: { focus: 'series' },
        symbolSize: 10,
        data: [
          data[0]
        ]
      },
      {
        name: 'Bottom Depth',
        type: 'effectScatter',
        color: 'gold',
        emphasis: { focus: 'series' },
        symbolSize: 10,
        data: [
          data[data.length - 1]
        ]
      },
      {
        name: 'Trajectory Line',
        type: 'line',
        color: 'red',
        emphasis: { focus: 'series' },
        data: [
          data[0],
          data[data.length - 1]
        ]
      }
    ]
  };
  
  chart.setOption(option);
}

profileEchart = (data, chart, wellname) => {
  chart.hideLoading()

  var option = {
    title: {
      text: 'Profile',
      left: 'center',
      subtext: `Data from well: ${wellname}`
    },
    grid: {
      left: 80,
      right: 110,
      top: 80,
    },
    xAxis: [
      {
        name: 'Distance',
        nameLocation: 'middle',
        nameGap: 50,
        type: 'value',
        scale: true,
        axisLabel: {
          formatter: '{value} ft',
          rotate: 90,
          fontSize: 9
        },
        splitLine: {
          show: false
        }
      }
    ],
    yAxis: [
      {
        name: 'TVD',
        nameLocation: 'middle',
        nameGap: 60,
        type: 'value',
        scale: true,
        inverse: true,
        axisLabel: {
          formatter: '{value} ft',
          fontSize: 9
        }
      }
    ],
    legend: {
      orient: 'vertical',
      right: 0,
      bottom: 'center',
      show: false
    },
    tooltip: {
      position: 'top',
      formatter: (params) => {
        return (
          `x: ${parseFloat(params.value[0]).toFixed(2)} <br/> y:  ${parseFloat(params.value[1]).toFixed(2)}`
        )
      },
      axisPointer: {
        show: true,
        type: 'cross',
        lineStyle: {
          type: 'dashed',
          width: 1
        }
      }
    },
    series: [
      {
        type: 'scatter',
        color: 'green',
        symbolSize: 3,
        data: data
      },
      {
        name: 'Top Depth',
        type: 'effectScatter',
        color: 'blue',
        emphasis: { focus: 'series' },
        symbolSize: 10,
        data: [
          data[0]
        ]
      },
      {
        name: 'Bottom Depth',
        type: 'effectScatter',
        color: 'gold',
        emphasis: { focus: 'series' },
        symbolSize: 10,
        data: [
          data[data.length - 1]
        ]
      }
    ]
  };
  
  chart.setOption(option);
}
}