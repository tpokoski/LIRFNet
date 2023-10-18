d3.csv('data/pivottest2.csv').then( function(rows) {
    console.log(rows);
    function unpack(rows, key) {
          return rows.map(function(row) { return row[key]; });
      }

    var E11 = {
        x: unpack(rows, 'timestamp'),
        y: unpack(rows, 'E11'),
        type: 'scatter',
        name: 'E11'
    };

    var E12= {
        x: unpack(rows, 'timestamp'),
        y: unpack(rows, 'E12'),
        type: 'scatter',
        name: 'E12'
    };


    var data = [E11, E12];

    var daysOfYear = Array.from(new Set(unpack(rows, 'DOY'))).sort((a,b) => a-b);
    var steps = daysOfYear.map(function(day) {
      var range = [
        d3.min(unpack(rows, 'timestamp').filter(function(d,i) { return unpack(rows, 'DOY')[i] === day;})),
        d3.max(unpack(rows, 'timestamp').filter(function(d,i) { return unpack(rows, 'DOY')[i] === day;})),
    ]
        return {
            label: day,
            method: "update",
            args: ["x", unpack(rows, 'timestamp').filter(function(d,i) { return unpack(rows, 'DOY')[i] === day;})]
        }
    });


    var layout = {
        title: 'IRT Temps',
        xaxis: {
          showgrid: false,
          zeroline: false
        },
        yaxis: {
          title: 'Deg C',
          showline: false
        },
        sliders: [{
          active: 0,
          currentvalue: {
              prefix: "Day of Year: "
          },
          pad: {t: 50},
          steps: steps
      }],
      
      };

    Plotly.newPlot('myPlot', data, layout);

});
