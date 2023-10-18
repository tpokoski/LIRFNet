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

    // Add a clipPath: everything out of this area won't be drawn.
    const clip = svg2.append("defs").append("svg:clipPath")
        .attr("id", "clip")
        .append("svg:rect")
        .attr("width", width2 )
        .attr("height", height2 )
        .attr("x", 0)
        .attr("y", 0);

    // Add brushing
    const brush = d3.brushX()                   // Add the brush feature using the d3.brush function
        .extent( [ [0,0], [width2,height2] ] )  // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
        .on("end", updateChart);              // Each time the brush selection changes, trigger the 'updateChart' function

    // Create the line variable: where both the line and the brush take place
    const line = svg2.append('g')
      .attr("clip-path", "url(#clip)")
	
	// Initialize line with group a
    line.append('g')
      .append("path")
        .datum(data)
        .attr("d", d3.line()
          .x(function(d) { return x2(+d.doynumber) })
          .y(function(d) { return y2(+d.E11) })
        )
        .attr("stroke", function(d){ return myColor("E11") })
        .style("stroke-width", 4)
        .style("fill", "none");

   // Add the brushing
   line.append("g")
     .attr("class", "brush")
     .call(brush);

//Appending x and Y axes
	const xAxis = svg2.append("g")
		.attr("class", "x axis")
		.attr("transform", `translate(0, ${height2})`)
		.call(d3.axisBottom(x2));
  
  
	const yAxis = svg2.append("g")
		.attr("class", "y axis")
		.call(d3.axisLeft(y2));
    
	// A function that update the chart
    function updatedropdown(selectedGroup) {

      // Create new data with the selection?
      const dataFilter = data.map(function(d){return {time: d.doynumber, value:d[selectedGroup]} })

      // Give these new data to update line
      line.datum(dataFilter)
          .transition()
          .duration(1000)
          .attr("d", d3.line()
            .x(function(d) { return x2(+d.time) })
            .y(function(d) { return y2(+d.value) })
          )
          .attr("stroke", function(d){ return myColor(selectedGroup) })
    };

	
    // When the button is changed, run the updateChart function
    d3.select("#selectButton").on("change", function(event,d) {
        // recover the option that has been chosen
        const selectedOption = d3.select(this).property("value")
        // run the updateChart function with this selected option
        updatedropdown(selectedOption)
    })
    
    // A function that set idleTimeOut to null
    let idleTimeout
    function idled() { idleTimeout = null; }

    // A function that update the chart for given boundaries
    function updateChart(event,d) {

      // What are the selected boundaries?
      extent = event.selection

      // If no selection, back to initial coordinate. Otherwise, update X axis domain
      if(!extent){
        if (!idleTimeout) return idleTimeout = setTimeout(idled, 350); // This allows to wait a little bit
        x2.domain([ 4,8])
      }else{
        x2.domain([ x2.invert(extent[0]), x2.invert(extent[1]) ])
        line.select(".brush").call(brush.move, null) // This remove the grey brush area as soon as the selection has been done
      }

      // Update axis and line position
      xAxis.transition().duration(1000).call(d3.axisBottom(x2))
      line.select('.line')
          .transition()
          .duration(1000)
          .attr("d", d3.line()
            .x(function(d) { return x2(d.doynumber) })
            .y(function(d) { return y2(d.E13) })
          )
    }

    // If user double click, reinitialize the chart
    svg2.on("dblclick",function(){
      x2.domain(d3.extent(data, function(d) { return d.doynumber; }))
      xAxis.transition().call(d3.axisBottom(x2))
      line
        .select('.line')
        .transition()
        .attr("d", d3.line()
          .x(function(d) { return x2(d.doynumber) })
          .y(function(d) { return y2(d.E13) })
      )
    });



});
