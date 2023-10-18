// Set the dimensions of the canvas / graph
const margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = innerWidth - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

// Set the ranges
const x = d3.scaleTime().range([0, width]);  
const y = d3.scaleLinear().range([height, 0]);

const parseTime = d3.timeParse("%m/%e/%Y %I:%M")


// Define the line
let plotline = d3.line()	
    .x(function(d) { return x(d.doy2); })
    .y(function(d) { return y(d.Tc); });
    
// Adds the svg canvas
let svg = d3.select("body")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", 
              "translate(" + margin.left + "," + margin.top + ")");

svg.append("rect")
    .attr("width", "100%")
    .attr("height", "100%")
    .attr("fill", "#f5f5f1")
            
  // Add the X Axis
var xAxis = svg.append("g")
  .attr("class", "axis")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x));

// Add the Y Axis
var yAxis = svg.append("g")
  .attr("class", "axis")
  .call(d3.axisLeft(y));



// Get the data
const data = d3.csv("data/irt_test.csv").then(function(data) {

    data.forEach(function(d) {
		d.date = d.doy2;
		d.value = +d.Tc;
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([0, d3.max(data, function(d) { return d.value; })]);

    // Group the entries by plot
    const dataNest = Array.from(
	    d3.group(data, d => d.plot), ([key, value]) => ({key, value})
	);
  
    // set the colour scale
    var color = d3.scaleOrdinal(d3.schemeCategory10);

    legendSpace = width/dataNest.length; // spacing for the legend

     // Add a clipPath: everything out of this area won't be drawn.
     const clip = svg.append("defs").append("svg:clipPath")
     .attr("id", "clip")
     .append("svg:rect")
     .attr("width", width )
     .attr("height", height )
     .attr("x", 0)
     .attr("y", 0);

    const line = svg.append('g')
        .attr("clip-path", "url(#clip)");

    // Add brushing
    const brush = d3.brushX()                   // Add the brush feature using the d3.brush function
        .extent( [ [0,0], [width,height] ] )  // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
        .on("end", updateChart)               // Each time the brush selection changes, trigger the 'updateChart' function

    // Add the brushing
    line.append("g")
        .attr("class", "brush")
        .call(brush);

    // Loop through each symbol / key
    dataNest.forEach(function(d,i) { 

              
        line.append("path")
            .attr("class", "line")
            .style("stroke", function() { // Add the colours dynamically
                return d.color = color(d.key); })
            .attr("d", plotline(d.value));

    });


/* // A function that set idleTimeOut to null
let idleTimeout
function idled() { idleTimeout = null; }

// A function that update the chart for given boundaries
function updateChart(event,d) {

  // What are the selected boundaries?
  extent = event.selection

  // If no selection, back to initial coordinate. Otherwise, update X axis domain
  if(!extent){
    if (!idleTimeout) return idleTimeout = setTimeout(idled, 350); // This allows to wait a little bit
    x.domain([ 4,8])
  }else{
    x.domain([ x.invert(extent[0]), x.invert(extent[1]) ])
    line.select(".brush").call(brush.move, null) // This remove the grey brush area as soon as the selection has been done
  }

  // Update axis and line position
  xAxis.transition().duration(1000).call(d3.axisBottom(x))
  line
      .select('.line')
      .transition()
      .duration(1000)
      .attr("d", d3.line()
        .x(function(d) { return x(d.doy2) })
        .y(function(d) { return y(d.Tc) })
      )
}; */

function updateChart() {
  if (!d3.event.sourceEvent) return; // Only transition after input.
  if (!d3.event.selection) return; // Ignore empty selections.
  var d0 = d3.event.selection.map(x.invert);
  var d1 = d0.map(d3.timeDay.round);
  var new_data = data.filter(function(d) { return d1[0] <= d.date && d.date <= d1[1] });
  x.domain(d1);
  y.domain([0, d3.max(new_data, function(d) { return d.value; })]);
  svg.select(".line").datum(new_data);
  svg.select(".x.axis").call(xAxis);
  svg.select(".y.axis").call(yAxis);
};



// If user double click, reinitialize the chart
svg.on("dblclick",function(){
    x.domain(d3.extent(data, function(d) { return d.doy2; }))
    xAxis.transition().call(d3.axisBottom(x))
    line
      .select('.line')
      .transition()
      .attr("d", d3.line()
        .x(function(d) { return x(d.doy2) })
        .y(function(d) { return y(d.Tc) })
    )
  });

});
