for (var i = 0; i < 4; i++) {
  for (var j = 0; j < 8; j++) {
      var rect = {
          type: 'rect',
          xref: 'x',
          yref: 'y',
          x0: i,
          y0: j,
          x1: i + 1,
          y1: j + 1,
          fillcolor: 'white',
          line: {
              color: 'black'
          },
          hoverlabel: {
            bgcolor: 'blue',
            font: {
              size: 14
            }
          },
          text: `Rectangle ${i * 8 + j + 1}`
      };


      var annotation = {
          x: i + 0.5,
          y: j + 0.5,
          text: `E${i + 1}${j + 1}`,
          font: {
              size: 14
          },
          showarrow: false
      };

  }
};

var layout = {
xaxis: {
    range: [-1, 4],
    showgrid: false,
    zeroline: false,
    visible: false
},
yaxis: {
    range: [-1, 8],
    showgrid: false,
    zeroline: false,
    visible: false
},
hovermode: 'closest',
shapes: [rect],
annotations:[annotation]
};

var data = [];

Plotly.newPlot('myDiv', data, layout);
