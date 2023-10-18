// set the dimensions and margins of the graph
const margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = 900 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

// append the svg object to the body of the page
const svg = d3.select("#my_dataviz")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          `translate(${margin.left}, ${margin.top})`);


//Read the data
d3.csv("data/pivottest2.csv").then(

  // Now I can use this dataset:
  function(data) {
    let value = 'E11'

    // Create an array of columns available in your data
    const allGroup = ["E11", "E12", "E13"]

    // add the options to the button
    const columnSelect = d3.select("#selectButton")
        .selectAll('option')
        .data(allGroup)
        .enter().append('option')
        .text(function (d) { return d; }) // text showed in the menu
        .attr("value", function (d) { return d; }) // corresponding value returned by the button
    

    // A color scale: one color for each group
    const myColor = d3.scaleOrdinal()
      .domain(allGroup)
      .range(d3.schemeSet2);
      
    // Add X axis --> it is a date format
    const x = d3.scaleTime()
      .domain(d3.extent(data, function(d) { return d3.timeParse("%_m/%e/%Y %I:%M")(d.timestamp); }))
      .range([ 0, width ]);
    xAxis = svg.append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(d3.axisBottom(x));

    // Add Y axis
    const y = d3.scaleLinear()
      .domain([0, d3.max(data, function(d) { return +d.E11; })])
      .range([ height, 0 ]);
    yAxis = svg.append("g")
      .call(d3.axisLeft(y));



    
    // Add a clipPath: everything out of this area won't be drawn.
    const clip = svg.append("defs").append("svg:clipPath")
        .attr("id", "clip")
        .append("svg:rect")
        .attr("width", width )
        .attr("height", height )
        .attr("x", 0)
        .attr("y", 0);

    // Add brushing
    const brush = d3.brushX()                   // Add the brush feature using the d3.brush function
        .extent( [ [0,0], [width,height] ] )  // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
        .on("end", updateChart)               // Each time the brush selection changes, trigger the 'updateChart' function

    // Create the line variable: where both the line and the brush take place
    const line = svg.append('g')
      .attr("clip-path", "url(#clip)")

    // Add the line
    line.append("path")
      .datum(data)
      .attr("class", "line")  // I add the class line to be able to modify this line later on.
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("d", d3.line()
        .x(function(d) { return x(d3.timeParse("%_m/%e/%Y %I:%M")(d.timestamp)) })
        .y(function(d) { return y(d.E11) })
        )
      .attr("stroke", function(d){ return myColor("E11") })
      .style("stroke-width", 4)
      .style("fill", "none");

  
    // Add the brushing
    line.append("g")
        .attr("class", "brush")
        .call(brush);


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
            .x(function(d) { return x(d3.timeParse("%_m/%e/%Y %I:%M")(d.timestamp)) })
            .y(function(d) { return y(d.E11) })
          )
    }

    // If user double click, reinitialize the chart
    svg.on("dblclick",function(){
      x.domain(d3.extent(data, function(d) { return d3.timeParse("%_m/%e/%Y %I:%M")(d.timestamp); }))
      xAxis.transition().call(d3.axisBottom(x))
      line
        .select('.line')
        .transition()
        .attr("d", d3.line()
          .x(function(d) { return x(d3.timeParse("%_m/%e/%Y %I:%M")(d.timestamp)) })
          .y(function(d) { return y(d.E11) })
      )
    });

    
    // A function that update the chart
    function update(selectedGroup) {

        // Create new data with the selection?
        const dataFilter = data.map(function(d){return {time: d3.timeParse("%_m/%e/%Y %I:%M")(d.timestamp), value:d[selectedGroup]} })
  
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

