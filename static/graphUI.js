	var w = $(".graph").width();
	var h = $(".graph").height();
	var padding = 38;

var graph = d3.select(".graph").append("svg").attr("width", w)
						.attr("height", h);

var lineSvg = graph.append("g");

var focus = graph.append("g")
    .style("display", "none")
    ;

parseDate = d3.time.format("%Y-%m-%d").parse;
unparse = d3.time.format("%b %d, '%y");

bisectDate = d3.bisector(function(d) { return -d[0]; }).right;



var start = "2009-01-01";
var end = "2016-01-01"
var request = "https://www.quandl.com/api/v3/datasets/YAHOO/SZ_399106.json?auth_token=HP8mWGAmxhswaJQ_enkV&start_date=" + start + "&end_date=" + end;


var dataset = d3.json(request,function(data) {
	names = data.dataset.column_names;
	data = data.dataset.data;

	for(var i = 0; i < data.length; i++)
		{data[i][0]=parseDate(data[i][0])};

	console.log(names);
	console.log(data);

minDate = parseDate(start);
maxDate = parseDate(end);
console.log(maxDate);
console.log(data[0][0]);



var xScale = d3.time.scale()
								 .domain([minDate,maxDate])
								 .range([padding, w - padding/2]);

var yScale = d3.scale.linear()
								 .domain([0,d3.max(data, function(d) { return d[1]; })])
								 .range([h - padding/1.5, padding/4]);


var xAxis = d3.svg.axis()
							  .scale(xScale)
							  .orient("bottom")
							  .ticks(10);

			//Define Y axis
var yAxis = d3.svg.axis()
							  .scale(yScale)
							  .orient("left")
							  .ticks(5);

var valueline = d3.svg.line()
    .x(function(d) { return xScale(d[0]); })
    .y(function(d) { return yScale(d[1]); });

lineSvg.append("path")                                 // **********
        .attr("class", "line")
        .attr("d", valueline(data));

graph.append("g")
    .attr("class", "axis") 
    .attr("transform", "translate(0," + (h - padding/1.5) + ")")//Assign "axis" class
    .call(xAxis);

graph.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(" + padding + ",0)")//Assign "axis" class
    .call(yAxis);


  // append the circle at the intersection              
    focus.append("circle")                                
        .attr("class", "point")                                                       
        .attr("r", 4);
       // append the x line
    focus.append("line")
        .attr("class", "x")
        .attr("y1", 0)
        .attr("y2", h);

    // append the y line
    focus.append("line")
        .attr("class", "y")
        .attr("x1", 0 + padding)
        .attr("x2", w - padding/1.5);

    // place the value at the intersection
    focus.append("text")
        .attr("class", "y1")
        .style("stroke", "white")
        .style("stroke-width", "3.5px")
        .style("opacity", 0.8)
        .attr("dx", 8)
        .attr("dy", "-.3em");
    focus.append("text")
        .attr("class", "y2")
        .attr("dx", 8)
        .attr("dy", "-.3em");

    // place the date at the intersection
    focus.append("text")
        .attr("class", "y3")
        .style("stroke", "white")
        .style("stroke-width", "3.5px")
        .style("opacity", 0.8)
        .attr("dx", 8)
        .attr("dy", "1em");
    focus.append("text")
        .attr("class", "y4")
        .attr("dx", 8)
        .attr("dy", "1em");
                                    
    
    // append the rectangle to capture mouse              
    graph.append("rect")                                    
        .attr("width", w)                             
        .attr("height", h)                           
        .style("fill", "none")                            
        .style("pointer-events", "all")                   
        .on("mouseover", function() { focus.style("display", null); })
        .on("mouseout", function() { focus.style("display", "none"); })
        .on("mousemove", mousemove);                      

    function mousemove() {                                
        var x0 = xScale.invert(d3.mouse(this)[0]),             
            i = bisectDate(data, (x0 * -1), 1),                   
            d0 = data[i - 1],                              
            d1 = data[i],                                 
            d = x0 - d0[0] > d1[0] - x0 ? d1 : d0;     
           console.log(x0);
           console.log(i);


        focus.select("circle.point")                           
            .attr("transform",                             
                  "translate(" + xScale(d[0]) + "," +         
                                 yScale(d[1]) + ")");

		 focus.select("text.y1")
		      .attr("transform",
		            "translate(" + xScale(d[0]) + "," +
		                           yScale(d[1]) + ")")
		      .text(Math.round(d[1]));

		  focus.select("text.y2")
		      .attr("transform",
		            "translate(" + xScale(d[0]) + "," +
		                           yScale(d[1]) + ")")
		      .text(Math.round(d[1]));

		  focus.select("text.y3")
		      .attr("transform",
		            "translate(" + xScale(d[0]) + "," +
		                           yScale(d[1]) + ")")
		      .text(unparse(d[0]));

		  focus.select("text.y4")
		      .attr("transform",
		            "translate(" + xScale(d[0]) + "," +
		                           yScale(d[1]) + ")")
		      .text(unparse(d[0]));

		  focus.select(".x")
		      .attr("transform",
		            "translate(" + xScale(d[0]) + "," +
		                           yScale(d[1]) + ")")
		                 .attr("y2", h - yScale(d[1])-padding/1.5);

		  focus.select(".y")
		      .attr("transform",
		            "translate(0," + yScale(d[1]) + ")");





    }  




});







// function addGraph(elementID, jsonUrl){

// 	d3.select(graph).append("div").attr("class",elementID);
//     var svg = d3.select(elementID).append("svg");
//     //...   
//     d3.json(jsonUrl,function(error,graph) {

//     var group = svg.append("g")
//         .attr("transform", "translate(100,10)")

//    	var line = d3.svg.line()
//         .x(function(d, i) {
//             return d.x;
//         })
//         .y(function(d, i) {
//             return d.y;
//         }); 
//     };
// }