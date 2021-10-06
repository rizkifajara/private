const data = {
  'DEPTH': [1,2,3],
  'FACIES': ['aaa','bbb','ccc']
}

const heatmapConv = (data, col, idx) => {
  return [0.5, data.DEPTH[idx], data[col][idx]];
}

var newArray = [];
for(let i = 0; i<data['DEPTH'].length; i++) {
  newArray.push(heatmapConv(data, 'FACIES', i))
}

// console.log(newArray)