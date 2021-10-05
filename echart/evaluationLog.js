var evalChart = echarts.init(document.getElementById('eval-chart'));

evalChart.showLoading()

// function largestInColumn(arr) {
//   var res = []
//   for (let i = 0; i < arr[0].length; i++) {
//     let maxm = arr[1][i];
//     for (let j = 1; j < arr.length; j++)
//       if (arr[j][i] > maxm)
//         maxm = arr[j][i];
//         res.push(maxm)
//   }
//   return res
// }

const param = {
  VSH: {range: [0,1], color: 'green', type:'value', model:'reg'},
  PHIE: {range: [0,0.5], color: 'blue', type:'value', model:'reg'},
  PERM: {range: [0.2,2000], color: 'black', type:'log', model:'reg'},
  SW: {range: [0,1], color: 'purple', type:'value', model:'reg'},
  FACIES: {range: [0,1], color: 'black', type:'value', model:'class'},
  HC: {range: [0,1], color: 'black', type:'value', model:'class'}
}

const callBlindLog = (col) => {
  $.getJSON('./evaluation.json', (response) => {
    dataLog = response[col];
    // maxData = largestInColumn(dataLog)
    range = param[col]['range']
    color = param[col]['color']
    type = param[col]['type']
    model = param[col]['model']
    blindEchart(dataLog, evalChart, col, range, color, type, model);
  });
}

callBlindLog('HC')

const blindEchart = (data, chart, col, range, color, type, model) => {
  chart.hideLoading();

  const Series = {
    reg: [
      {
        name: col,
        type: 'line',
        showSymbol: false,
        lineStyle: { width: 0.5 },
        color: color,
        encode: {
          x: col,
          y: 'index',
          tooltip: ['index', col, 'DEPTH', 'WELL']
        }
      },
      {
        name: 'prediction',
        type: 'line',
        showSymbol: false,
        lineStyle: {
          width: 0.5,
          type: 'dashed'
        },
        color: 'red',
        encode: {
          x: 'prediction',
          y: 'index',
          tooltip: ['prediction']
        },
        xAxisIndex: 1,
        yAxisIndex: 1,
      },
      {
        type: 'bar',
        xAxisIndex: 2,
        yAxisIndex: 2,
        dimensions: ['error'],
        data: data.map(x => x[5])
      },
      {
        type: 'scatter',
        xAxisIndex: 3,
        yAxisIndex: 3,
        symbolSize: 3,
        encode: {
          x: col,
          y: 'prediction',
          tooltip: [col, 'prediction', 'error', 'DEPTH', 'WELL']
        }
      }
    ],
    class: [
      {
        name: col,
        type: 'line',
        showSymbol: false,
        lineStyle: { width: 0.5 },
        color: color,
        encode: {
          x: col,
          y: 'index',
          tooltip: ['index', col, 'DEPTH', 'WELL']
        }
      },
      {
        name: 'prediction',
        type: 'line',
        showSymbol: false,
        lineStyle: {
          width: 0.5,
          type: 'dashed'
        },
        color: 'red',
        encode: {
          x: 'prediction',
          y: 'index',
          tooltip: ['prediction']
        },
        xAxisIndex: 1,
        yAxisIndex: 1,
      },
      {
        type: 'bar',
        xAxisIndex: 2,
        yAxisIndex: 2,
        dimensions: ['error'],
        data: data.map(x => x[5])
      },
      {
        type: 'scatter',
        xAxisIndex: 3,
        yAxisIndex: 3,
        symbolSize: 3,
        encode: {
          x: col,
          y: 'prediction',
          tooltip: [col, 'prediction', 'error', 'DEPTH', 'WELL']
        }
      }
    ]
  }

  var option = {
    title: {
      text: 'Blind Well Test',
      subtext: `to evaluation: ${col}`,
      left: 'center'
    },
    dataset: {
      source: data
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        axis: 'y',
        type: 'cross'
      }
    },
    toolbox: {
      feature: {
        dataZoom: {
          xAxisIndex: 'none'
        },
        restore: {},
        saveAsImage: {}
      }
    },
    grid: [
      {
        top: 80,
        left: '20%',
        width: 100,
        height: '80%'
      },
      {
        top: 80,
        left: '20%',
        width: 100,
        height: '80%'
      },
      {
        top: 80,
        left: '35%',
        width: 100,
        height: '80%'
      },
      {
        top: 'center',
        left: '55%',
        width: '30%',
        height: '50%'
      },
      {
        top: 'center',
        left: '55%',
        width: '30%',
        height: '50%'
      }
    ],
    yAxis: [
      {
        type: 'value',
        axisLabel: {
          fontSize: 9,
          interval: 499,
          // formatter: (value) => { return `${parseFloat(value).toFixed(0)}` },
        },
        inverse: true,
      },
      {
        gridIndex: 1,
        type: 'value',
        axisLabel: {
          show: false,
          interval: 499
        },
        axisLine: { show: false },
        axisTick: { show: false },
        name: 'num_data',
        nameLocation: 'middle',
        nameTextStyle: {
          padding: 20
        },
        inverse: true
      },
      {
        gridIndex: 2,
        axisLabel: {
          show: false,
          interval: 499
        },
        data: data.map(x => x[0]),
        inverse: true
      },
      {
        gridIndex: 3,
        type: type,
        axisLabel: {
          show: true,
          fontSize: 9,
          // interval: 10
        },
        min: range[0],
        max: range[1],
        name: 'Prediction',
        nameLocation: 'middle',
        minorSplitLine: { show: true },
        nameTextStyle: {
          padding: 20
        }
      }
    ],
    xAxis: [
      {
        position: 'top',
        type: type,
        axisLabel: { show: false },
        axisLine: { show: true },
        min: range[0],
        max: range[1],
        name: `${range[0]}                                    ${range[1]}`,
        nameLocation: 'middle',
        nameTextStyle: {
          fontSize: 9,
          color: color,
          padding: -10
        }
      },
      {
        gridIndex: 1,
        type: type,
        position: 'top',
        axisLabel: { show: false },
        axisLine: { show: true },
        minorSplitLine: { show: true },
        min: range[0],
        max: range[1],
        nameTextStyle: {
          fontSize: 9,
          padding: 5
        }
      },
      {
        gridIndex: 2,
        type: 'value',
        position: 'top',
        min: 0,
        max: range[1],
        name: `Abs Error\n\n0                                    ${range[1]}`,
        nameLocation: 'middle',
        axisLine: { show: true },
        axisTick: { show: false },
        axisLabel: { show: false },
        minorSplitLine: { show: true },
        nameTextStyle: {
          padding: -10,
          fontSize: 9
        }
      },
      {
        gridIndex: 3,
        type: type,
        axisLabel: { show: true, fontSize: 9 },
        minorSplitLine: { show: true },
        name: '',
        min: range[0],
        max: range[1],
        name: 'Actual',
        nameLocation: 'middle',
        nameTextStyle: {
          padding: 15
        }
      }
    ],
    visualMap: [
      {
        seriesIndex: [2, 3],
        orient: 'vertical',
        top: 'center',
        left: '45%',
        min: 0,
        max: range[1],
        text: ['High Error', 'Low Error'],
        dimension: 'error',
        inRange: {
          color: ['#65B581', '#FFCE34', '#FD665F']
        }
      }
    ],
    series: Series[model],
    dataZoom: [
      {
        show: true,
        realtime: true,
        right: 10,
        start: 0,
        end: 30,
        yAxisIndex: [0, 1, 2]
      }
    ],
    legend: {
      data: [col, 'prediction'],
      left: 'center',
      bottom: 10
    }
  };

  chart.setOption(option);

}

