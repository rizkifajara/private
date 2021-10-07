function plotLog(WellName) {

  console.log("Plot Log run successfully!")

  var logChart = echarts.init(document.getElementById('log-chart'));

  logChart.showLoading()

  const heatmapConv = (data, col, idx) => {
    return [0.5, idx, data[col][idx]];
  }

  let callWellLog = (wellName) => {
    $.getJSON('/static/echart/database_volve.json', (response) => {
      dataLog = response[wellName];
      var newHC = [];
      var newFACIES = [];
      for (let i = 0; i < dataLog['DEPTH'].length; i++) {
        newHC.push(heatmapConv(dataLog, 'HC', i));
        newFACIES.push(heatmapConv(dataLog, 'FACIES_label', i));
      }
      logEchart(dataLog, newHC, newFACIES, logChart, wellName);
    });
  }

  callWellLog(WellName)

  const logEchart = (data, dataHC, dataFACIES, chart, wellname) => {
    chart.hideLoading();

    var option = {
      title: {
        text: 'Well Log Plot',
        subtext: `Data from well: ${wellname}`,
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          axis: 'auto',
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
          left: 100,
          width: 50,
          height: '70%'
        },
        {
          top: 80,
          left: 180,
          width: 50,
          height: '70%'
        },
        {
          top: 80,
          left: 260,
          width: 50,
          height: '70%'
        },
        {
          top: 80,
          left: 260,
          width: 50,
          height: '70%'
        },
        {
          top: 80,
          left: 340,
          width: 50,
          height: '70%'
        },
        {
          top: 80,
          left: 420,
          width: 50,
          height: '70%'
        },
        {
          top: 80,
          left: 500,
          width: 50,
          height: '70%'
        },
        {
          top: 80,
          left: 580,
          width: 50,
          height: '70%'
        },
        {
          top: 80,
          left: 660,
          width: 50,
          height: '70%'
        },
        {
          top: 80,
          left: 740,
          width: 50,
          height: '70%'
        }
      ],
      yAxis: [
        {
          axisLabel: {
            fontSize: 9,
            interval: 500,
            formatter: (value) => { return `${parseFloat(value).toFixed(0)} m` },
          },
          data: data.DEPTH,
          inverse: true,
        },
        {
          gridIndex: 1,
          axisLabel: {
            show: false,
            interval: 500
          },
          data: data.DEPTH,
          axisLine: { show: false },
          axisTick: { show: false },
          inverse: true
        },
        {
          gridIndex: 2,
          axisLabel: {
            show: false,
            interval: 500
          },
          data: data.DEPTH,
          axisLine: { show: false },
          axisTick: { show: false },
          inverse: true
        },
        {
          gridIndex: 3,
          axisLabel: {
            show: false,
            interval: 500
          },
          data: data.DEPTH,
          axisLine: { show: false },
          axisTick: { show: false },
          inverse: true
        },
        {
          gridIndex: 4,
          axisLabel: {
            show: false,
            interval: 500
          },
          axisLine: { show: false },
          axisTick: { show: false },
          data: data.DEPTH,
          inverse: true
        },
        {
          gridIndex: 5,
          axisLabel: {
            show: false,
            interval: 500
          },
          data: data.DEPTH,
          axisLine: { show: false },
          axisTick: { show: false },
          inverse: true
        },
        {
          gridIndex: 6,
          axisLabel: {
            show: false,
            interval: 500
          },
          data: data.DEPTH,
          axisLine: { show: false },
          axisTick: { show: false },
          inverse: true
        },
        {
          gridIndex: 7,
          axisLabel: {
            show: false,
            interval: 500
          },
          data: data.DEPTH,
          axisLine: { show: false },
          axisTick: { show: false },
          inverse: true
        },
        {
          gridIndex: 8,
          axisLabel: {
            show: false,
            interval: 500
          },
          data: data.DEPTH,
          axisLine: { show: false },
          axisTick: { show: false },
          inverse: true
        },
        {
          gridIndex: 9,
          axisLabel: {
            show: false,
            interval: 500
          },
          data: data.DEPTH,
          axisLine: { show: false },
          axisTick: { show: false },
          inverse: true
        }
      ],
      xAxis: [
        {
          position: 'top',
          type: 'value',
          axisLabel: { show: false },
          axisLine: { show: true },
          min: 0,
          max: 150,
          name: '0                150',
          nameLocation: 'middle',
          nameTextStyle: {
            fontSize: 9,
            color: 'green',
            padding: -10
          }
        },
        {
          gridIndex: 1,
          type: 'log',
          position: 'top',
          axisLabel: { show: false },
          axisLine: { show: true },
          minorSplitLine: { show: true },
          min: 0.2,
          max: 2000,
          name: '0.2            2000',
          nameLocation: 'middle',
          nameTextStyle: {
            fontSize: 9,
            color: 'black',
            padding: -10
          }
        },
        {
          gridIndex: 2,
          type: 'value',
          position: 'top',
          axisLabel: { show: false },
          axisLine: { show: true },
          min: 1.95,
          max: 2.95,
          name: '1.95            2.95',
          nameLocation: 'middle',
          axisLine: { show: false },
          axisTick: { show: false },
          nameTextStyle: {
            fontSize: 9,
            color: 'red',
            padding: -10
          }
        },
        {
          gridIndex: 3,
          type: 'value',
          position: 'top',
          axisLabel: { show: false },
          axisLine: { show: true },
          splitLine: { show: false },
          min: -0.15,
          max: 0.45,
          name: '0.45          -0.15',
          nameLocation: 'middle',
          nameTextStyle: {
            fontSize: 9,
            color: 'blue',
            padding: 5
          },
          inverse: true
        },
        {
          gridIndex: 4,
          type: 'value',
          position: 'top',
          axisLabel: { show: false },
          axisLine: { show: true },
          min: 0,
          max: 1,
          name: '0                 1',
          nameLocation: 'middle',
          nameTextStyle: {
            fontSize: 9,
            color: 'lime',
            padding: -10
          }
        },
        {
          gridIndex: 5,
          type: 'value',
          position: 'top',
          axisLabel: { show: false },
          axisLine: { show: true },
          min: 0,
          max: 0.5,
          name: '0.5                 0',
          nameLocation: 'middle',
          nameTextStyle: {
            fontSize: 9,
            color: 'darkblue',
            padding: -10
          },
          inverse: true
        },
        {
          gridIndex: 6,
          type: 'value',
          position: 'top',
          axisLabel: { show: false },
          axisLine: { show: true },
          min: 0,
          max: 1,
          name: '0                 1',
          nameLocation: 'middle',
          nameTextStyle: {
            fontSize: 9,
            color: 'purple',
            padding: -10
          }
        },
        {
          gridIndex: 7,
          type: 'value',
          position: 'top',
          axisLabel: { show: false },
          axisLine: { show: true },
          min: 0,
          max: 1,
          name: '0.1            10000',
          nameLocation: 'middle',
          nameTextStyle: {
            fontSize: 9,
            color: 'black',
            padding: -10
          }
        },
        {
          gridIndex: 8,
          type: 'value',
          position: 'top',
          axisLabel: { show: false },
          axisLine: { show: true },
          min: 0,
          max: 1,
          name: 'HC',
          nameLocation: 'middle',
          nameTextStyle: {
            fontSize: 9,
            color: 'black',
            padding: -10
          }
        },
        {
          gridIndex: 9,
          type: 'value',
          position: 'top',
          axisLabel: { show: false },
          axisLine: { show: true },
          min: 0,
          max: 1,
          name: 'Facies',
          nameLocation: 'middle',
          nameTextStyle: {
            fontSize: 9,
            color: 'black',
            padding: -10
          }
        }
      ],
      visualMap: [
        {
          seriesIndex: 8,
          min: 0,
          max: 1,
          type: 'piecewise',
          orient: 'vertical',
          top: 250,
          right: 40,
          textStyle: {fontSize: 8},
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
          seriesIndex: 9,
          min: 0,
          max: 8,
          type: 'piecewise',
          orient: 'vertical',
          top: 60,
          right: 40,
          splitNumber: 9, 
          textStyle: {fontSize: 8},
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
        }
      ],
      series: [
        {
          name: 'GR',
          type: 'line',
          showSymbol: false,
          lineStyle: { width: 1 },
          color: 'green',
          data: data.GR
        },
        {
          name: 'RT',
          type: 'line',
          showSymbol: false,
          lineStyle: { width: 1 },
          color: 'black',
          xAxisIndex: 1,
          yAxisIndex: 1,
          data: data.ILD
        },
        {
          name: 'RHOB',
          type: 'line',
          showSymbol: false,
          lineStyle: { width: 1 },
          color: 'red',
          xAxisIndex: 2,
          yAxisIndex: 2,
          data: data.RHOB
        },
        {
          name: 'NPHI',
          type: 'line',
          showSymbol: false,
          lineStyle: { width: 1 },
          color: 'blue',
          xAxisIndex: 3,
          yAxisIndex: 3,
          data: data.NPHI
        },
        {
          name: 'VSH',
          type: 'line',
          showSymbol: false,
          lineStyle: { width: 1 },
          color: 'lime',
          xAxisIndex: 4,
          yAxisIndex: 4,
          data: data.VSH
        },
        {
          name: 'PHIE',
          type: 'line',
          showSymbol: false,
          lineStyle: { width: 1 },
          color: 'darkblue',
          xAxisIndex: 5,
          yAxisIndex: 5,
          data: data.PHIE
        },
        {
          name: 'SW',
          type: 'line',
          showSymbol: false,
          lineStyle: { width: 1 },
          color: 'purple',
          xAxisIndex: 6,
          yAxisIndex: 6,
          data: data.SW
        },
        {
          name: 'PERM',
          type: 'line',
          showSymbol: false,
          lineStyle: { width: 1 },
          color: 'black',
          xAxisIndex: 7,
          yAxisIndex: 7,
          data: data.PERM
        },
        {
          name: 'HC',
          type: 'heatmap',
          xAxisIndex: 8,
          yAxisIndex: 8,
          data: dataHC,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'black'
            }
          }
        },
        {
          name: 'FACIES',
          type: 'heatmap',
          xAxisIndex: 9,
          yAxisIndex: 9,
          data: dataFACIES,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'black'
            }
          }
        }
      ],
      dataZoom: [
        {
          show: true,
          realtime: true,
          left: 10,
          start: 0,
          end: 30,
          yAxisIndex: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        }
      ],
      legend: {
        data: ['GR', 'RT', 'RHOB', 'NPHI', 'VSH', 'PHIE', 'SW', 'PERM'],
        left: 'center',
        bottom: 0,
        textStyle: {fontSize: 8}
      }
    };


    // option.xAxis[0].min = 0;
    // option.xAxis[0].max = 1;
    chart.setOption(option);

  }
}