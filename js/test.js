// set the dimensions and margins of the graph
const margin2 = {top: 10, right: 50, bottom: 50, left: 50},
    width2 = innerWidth - margin2.left - margin2.right,
    height2 = 600 - margin2.top - margin2.bottom;


// append the svg object to the body of the page
const svg2 = d3.select("#my_dataviz")
  .append("svg")
    .attr("width", width2 + margin2.left + margin2.right)
    .attr("height", height2 + margin2.top + margin2.bottom)
  .append("g")
    .attr("transform", `translate(${margin2.left},${margin2.top})`);

// Add X axis --> it is a date format
const x2 = d3.scaleTime().range([ 0, width2 ]);
// Add Y axis
const y2 = d3.scaleLinear().range([ height2, 0 ]);
  	
//Read the data
d3.csv("data/pivottest.csv").then( function(data) {


    // List of groups (here I have one group per column from pivoted IRT data)
    const allGroup = ["E11", "E12", "E13"]

    // add the options to the button
    d3.select("#selectButton")
    	.selectAll('myOptions')
    	.data(allGroup)
    	.enter().append('option')
    	.text(function (d) { return d; }) // text showed in the menu
    	.attr("value", function (d) { return d; }) // corresponding value returned by the button

    // A color scale: one color for each group
    const myColor = d3.scaleOrdinal()
      .domain(allGroup)
      .range(d3.schemeSet2);


    // Scale the range of the data
    x2.domain(d3.extent(data, function(d) { return d.doynumber; }));
    y2.domain(d3.extent(data, function(d) { return d.E11; }));

	
	// Initialize line with group a
    const line = svg2.append('g')
      .append("path")
        .datum(data)
        .attr("d", d3.line()
          .x(function(d) { return x(+d.doynumber) })
          .y(function(d) { return y(+d.E11) })
        )
        .attr("stroke", function(d){ return myColor("E11") })
        .style("stroke-width", 4)
        .style("fill", "none")

	
//Appending x and Y axes
	svg2.append("g")
		.attr("class", "x axis")
		.attr("transform", `translate(0, ${height2})`)
		.call(d3.axisBottom(x2));
  
  
	svg2.append("g")
		.attr("class", "y axis")
		.call(d3.axisLeft(y2));
    
	// A function that update the chart
    function update(selectedGroup) {

      // Create new data with the selection?
      const dataFilter = data.map(function(d){return {time: d.doynumber, value:d[selectedGroup]} })

      // Give these new data to update line
      line
          .datum(dataFilter)
          .transition()
          .duration(1000)
          .attr("d", d3.line()
            .x(function(d) { return x(+d.time) })
            .y(function(d) { return y(+d.value) })
          )
          .attr("stroke", function(d){ return myColor(selectedGroup) })
    };

	
    // When the button is changed, run the updateChart function
    d3.select("#selectButton").on("change", function(event,d) {
        // recover the option that has been chosen
        const selectedOption = d3.select(this).property("value")
        // run the updateChart function with this selected option
        update(selectedOption)
    })

});