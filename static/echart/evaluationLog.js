function evaluationLog(logName) {

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
    VSH: { range: [0, 1], color: 'green', type: 'value', model: 'reg', tooltip: 'cross' },
    PHIE: { range: [0, 0.5], color: 'blue', type: 'value', model: 'reg', tooltip: 'cross' },
    PERM: { range: [0.2, 2000], color: 'black', type: 'log', model: 'reg', tooltip: 'cross' },
    SW: { range: [0, 1], color: 'purple', type: 'value', model: 'reg', tooltip: 'cross' },
    FACIES: { range: [0, 7], color: 'black', type: 'category', model: 'classFACIES', tooltip: 'auto' },
    HC: { range: [0, 1], color: 'black', type: 'category', model: 'classHC', tooltip: 'auto' }
  }

  const callBlindLog = (col) => {
    $.getJSON('/static/echart/evaluation.json', (response) => {
      dataLog = response[col];
      // maxData = largestInColumn(dataLog)
      range = param[col]['range']
      color = param[col]['color']
      type = param[col]['type']
      model = param[col]['model']
      tooltip = param[col]['tooltip']
      blindEchart(dataLog, evalChart, col);
    });
  }

  // Compare string sama key object param
  // let myString = logName
  // let item
  // if(param.hasOwnProperty(myString)) {
  //   item = param[myString]
  // }
  callBlindLog(logName)

  const blindEchart = (data, chart, col) => {
    chart.hideLoading();
    const dataActual = data.map(x => x[3])
    const dataPredict = data.map(x => x[4])
    const cm = ConfusionMatrix.fromLabels(dataActual, dataPredict)
    
    var matrix = cm.matrix.splice(2, 8).map(x => [x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]])
    var labels = cm.labels.splice(2, 8)
    var dataMatrix = [];
    for(var i=0; i<labels.length; i++){
      for(var j=0; j<labels.length; j++){
        dataMatrix.push([i,j,matrix[i][j]])
      }
    }
    console.table(dataMatrix)

    const params = {
      reg: {
        series: [
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
        ]
      },
      classHC: {
        series: [
          {
            name: 'Actual',
            type: 'heatmap',
            data: data.map(x => [0.5, x[0], x[3]]),
            encode: { tooltip: [2] }
          },
          {
            name: 'Prediction',
            type: 'heatmap',
            data: data.map(x => [0.5, x[0], x[4]]),
            encode: { tooltip: [2] },
            xAxisIndex: 1,
            yAxisIndex: 1,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'black'
              }
            }
          },
          {
            type: 'heatmap',
            data: data.map(x => [0.5, x[0], String(x[5]) == "false"]),
            encode: { tooltip: [2] },
            xAxisIndex: 2,
            yAxisIndex: 2,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'black'
              }
            }
          },
          {
            type: 'heatmap',
            data: dataMatrix,
            xAxisIndex: 3,
            yAxisIndex: 3,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ],
        visualMap: [
          {
            seriesIndex: [0, 1],
            min: 0,
            max: 1,
            type: 'piecewise',
            orient: 'horizontal',
            bottom: 10,
            left: 'center',
            splitNumber: 2,
            pieces: [
              {
                min: 0.5,
                max: 1,
                color: "gold",
                label: "Hydrocarbon Prospect Zone",
              }
            ],
            outOfRange: {
              color: "rgba(0,0,0,0)",
            }
          },
          {
            seriesIndex: [2],
            min: 0,
            max: 1,
            type: 'piecewise',
            orient: 'vertical',
            bottom: 'center',
            left: '45%',
            splitNumber: 2,
            pieces: [
              {
                min: 0,
                max: 0.5,
                color: "green",
                label: "True",
              },
              {
                min: 0.5,
                max: 1,
                color: "red",
                label: "False",
              }
            ],
            outOfRange: {
              color: "rgba(0,0,0,0)",
            }
          },
          {
            seriesIndex: 3,
            orient: 'vertical',
            top: 'center',
            right: '5%',
            text: ['Max Count', 'Min Count'],
            max: matrix[0][0],
            dimension: 2,
            inRange: {
              color: ['#ffffff', '#4586F3']
            }
          }
        ],
        grid: [
          {
            top: 80,
            left: '21%',
            width: 100,
            height: '80%'
          },
          {
            top: 80,
            left: '25%',
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
        ]
      },
      classFACIES: {
        series: [
          {
            name: 'Actual',
            type: 'heatmap',
            data: data.map(x => [0.5, x[0], x[6]]),
            encode: { tooltip: [2] }
          },
          {
            name: 'Prediction',
            type: 'heatmap',
            data: data.map(x => [0.5, x[0], x[7]]),
            encode: { tooltip: [2] },
            xAxisIndex: 1,
            yAxisIndex: 1,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'black'
              }
            }
          },
          {
            type: 'heatmap',
            data: data.map(x => [0.5, x[0], String(x[5]) == "false"]),
            encode: { tooltip: [2] },
            xAxisIndex: 2,
            yAxisIndex: 2,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'black'
              }
            }
          },
          {
            type: 'heatmap',
            data: dataMatrix,
            xAxisIndex: 3,
            yAxisIndex: 3,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ],
        visualMap: [
          {
            seriesIndex: [0,1],
            min: 0,
            max: 8,
            orient: 'horizontal',
            bottom: 10,
            left: 'center',
            splitNumber: 9,
            pieces: [
              {
                min: 0.888889,
                max: 1.77778,
                color: "#5e4fa2",
                label: "F-TIDAL BAR",
              },
              {
                min: 1.77778,
                max: 2.66667,
                color: "#3288bd",
                label: "F-LOWER SHOREFACE",
              },
              {
                min: 2.66667,
                max: 3.55556,
                color: "#abdda4",
                label: "F-TIDAL FLAT MUDDY",
              },
              {
                min: 3.55556,
                max: 4.44445,
                color: "#e6f598",
                label: "F-OFFSHORE",
              },
              {
                min: 4.44445,
                max: 5.33334,
                color: "#ffffbf",
                label: "F-TIDAL CHANNEL",
              },
              {
                min: 5.33334,
                max: 6.22223,
                color: "#fee08b",
                label: "F-MOUTHBAR",
              },
              {
                min: 6.22223,
                max: 7.11112,
                color: "#f46d43",
                label: "F-UPPER SHOREFACE",
              },
              {
                min: 7.11112,
                max: 8,
                color: "#9a0140",
                label: "F-MARSH",
              }
            ],
            outOfRange: {
              color: "rgba(0,0,0,0)",
            }
          },
          {
            seriesIndex: [2],
            min: 0,
            max: 1,
            type: 'piecewise',
            orient: 'vertical',
            bottom: 'center',
            left: '40%',
            splitNumber: 2,
            pieces: [
              {
                min: 0,
                max: 0.5,
                color: "green",
                label: "True",
              },
              {
                min: 0.5,
                max: 1,
                color: "red",
                label: "False",
              }
            ],
            outOfRange: {
              color: "rgba(0,0,0,0)",
            }
          },
          {
            seriesIndex: 3,
            orient: 'vertical',
            top: 'center',
            right: '5%',
            text: ['Max Count', 'Min Count'],
            max: matrix[0][0],
            dimension: 2,
            inRange: {
              color: ['#ffffff', '#4586F3']
            }
          }
        ],
        grid: [
          {
            top: 80,
            left: '17%',
            width: 100,
            height: '80%'
          },
          {
            top: 80,
            left: '21%',
            width: 100,
            height: '80%'
          },
          {
            top: 80,
            left: '30%',
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
        ]
      }
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
          type: tooltip
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
      grid: params[model]['grid'],
      yAxis: [
        {
          type: 'value',
          axisLabel: {
            fontSize: 9,
            interval: 499,
          },
          name: 'num_data',
          nameLocation: 'middle',
          nameTextStyle: {
            padding: 20
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
          axisLine: { show: true },
          axisTick: { show: true },
          inverse: true
        },
        {
          gridIndex: 2,
          type: 'category',
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
          },
          min: range[0],
          max: range[1],
          name: 'Prediction',
          nameLocation: 'middle',
          minorSplitLine: { show: true },
          nameTextStyle: {
            padding: 20
          },
          data: labels
        }
      ],
      xAxis: [
        {
          position: 'top',
          type: type,
          axisLabel: { show: false },
          axisLine: { show: true },
          minorSplitLine: { show: true },
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
          axisLine: { show: false },
          axisTick: { show: false },
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
          name: `Status\n\n0                                    ${range[1]}`,
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
          axisLabel: { show: true, fontSize: 9, rotate: 30 },
          minorSplitLine: { show: true },
          name: '',
          min: range[0],
          max: range[1],
          name: 'Actual',
          nameLocation: 'middle',
          nameTextStyle: {
            padding: 45
          },
          data: labels
        }
      ],
      visualMap: params[model]['visualMap'],
      series: params[model]['series'],
      dataZoom: [
        {
          show: true,
          realtime: true,
          right: 10,
          start: 0,
          end: 100,
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

}