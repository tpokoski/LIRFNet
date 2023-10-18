// Set up the dimensions of the chart
var width = innerWidth;
var height = 400;
var margin = { top: 20, right: 20, bottom: 60, left: 60 };

// Set up the scales for the x and y axes
var xScale = d3.scaleTime().range([0, width - margin.left - margin.right]);

var yScale = d3.scaleLinear().range([height - margin.top - margin.bottom, 0]);

// Set up the x-axis
var xAxis = d3.axisBottom(xScale).tickSizeOuter(0);

// Set up the y-axis
var yAxis = d3.axisLeft(yScale).tickSizeOuter(0);

// Set up the line generator
var line = d3.line()
  .x(function(d) { return xScale(d.doy2); })
  .y(function(d) { return yScale(d.Tc); });

// Add the Chart element to the page
var chart = d3.select("body").append("svg")
  .attr("width", width)
  .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

chart.append("rect")
  .attr("width", "100%")
  .attr("height", "100%")
  .attr("fill", "#f5f5f1")

// Add the Context element to the page
var context = d3.select("body").append("svg")
  .attr("width", width)
  .attr("height", 100)
  .append("g")
    .attr("transform", "translate(" + margin.left + ",20)");

context.append("rect")
  .attr("width", "100%")
  .attr("height", "100%")
  .attr("fill", "#f5f5f1")

// Load the data and render the chart
d3.csv("data/irt_test.csv")
  .then(function(data) {

  // Parse the data
  data.forEach(function(d) {
    d.date = d.doy2;
    d.value = +d.Tc;
  });

  
  // Set the domain of the scales
  xScale.domain(d3.extent(data, function(d) { return d.date; }));
  yScale.domain([0, d3.max(data, function(d) { return d.Tc; })]);

    // Add the lines to the chart
    chart.append("path")
    .datum(data)
    .attr("class", "line")
    .attr("d", line);

  // Add the x-axis to the chart
  chart.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + (height - margin.top - margin.bottom) + ")")
    .call(xAxis);

  // Add the y-axis to the chart
  chart.append("g")
    .attr("class", "y axis")
    .call(yAxis);

  // Set up the brush and zoom behavior
  var brush = d3.brushX()
    .extent([[0, 0], [width - margin.left - margin.right, height - margin.top - margin.bottom]])
    .on("brush end", brushed);

  const zoom = d3.zoom()
    .scaleExtent([1, Infinity])
    .translateExtent([[0, 0], [width - margin.left - margin.right, height - margin.top - margin.bottom]])
    .extent([[0, 0], [width - margin.left - margin.right, height - margin.top - margin.bottom]])
    .on("zoom", zoomed);

  // Add the brush to the Context element
  context.append("g")
    .attr("class", "brush")
    .call(brush)
    .call(brush.move, xScale.range());

  // Add the lines to the Context element
  context.append("path")
    .datum(data)
    .attr("class", "line")
    .attr("d", line);
}).catch(function(error){
   console.error(error);
});


  // Add the zoom behavior to the Chart element
  chart.append("rect")
    .attr("class", "zoom")
    .attr("width", width - margin.left - margin.right)
    .attr("height", height - margin.top - margin.bottom)
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
    .call(zoom);

  // Add the mouseover with a tooltip
  chart.selectAll(".line")
    .on("mouseover", function(d) {
  // Show the tooltip
    d3.select("#tooltip")
      .style("left", d3.event.pageX + "px")
      .style("top", d3.event.pageY + "px")
      .style("display", "block")
      .html("Date: " + d.date + "<br>Value: " + d.value);
      })
      .on("mouseout", function(d) {
        // Hide the tooltip
        d3.select("#tooltip").style("display", "none");
        });


// Define the brushed function
function brushed() {
  if (!d3.event.sourceEvent) return;
  if (!d3.event.selection) return;
  var d0 = d3.event.selection.map(xScale.invert);
  var d1 = d0.map(d3.timeDay.round);
  var new_data = data.filter(function(d) { return d1[0] <= d.date && d.date <= d1[1] });
  xScale.domain(d1);
  chart.select(".line").datum(new_data);
  chart.select(".x.axis").call(xAxis);
  chart.select(".y.axis").call(yAxis);
}

function zoomed() {
  if (!d3.event.sourceEvent) return;
  if (!d3.event.selection) return;
  var d0 = d3.event.selection.map(xScale.invert);
  var d1 = d0.map(d3.timeDay.round);
  var new_data = data.filter(function(d) { return d1[0] <= d.date && d.date <= d1[1] });
  xScale.domain(d1);
  chart.select(".line").datum(new_data);
  chart.select(".x.axis").call(xAxis);
  chart.select(".y.axis").call(yAxis);
}


