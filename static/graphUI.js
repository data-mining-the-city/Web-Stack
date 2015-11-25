	var w = $(".graph").width();
	var h = $(".graph").height();
	var padding = 38;


var graph = d3.select(".graph").append("svg").attr("width", w)
						.attr("height", h);

var lineSvg = graph.append("g");
var dataSvg = graph.append("g");

var focus = graph.append("g")
    .style("display", "none")
    ;

parseDate = d3.time.format("%Y-%m-%d").parse;
unparse = d3.time.format("%b %d, '%y");
reparse = d3.time.format("%b %d, '%y").parse;

bisectDate = d3.bisector(function(d) { return d.date; }).right;

var xScale = "";
var yScale = "";
var gData=[];

var index = $("input[name='index']:checked").val();

var start = "2012-01-06";
var end = "2015-10-01";
var request = "https://www.quandl.com/api/v3/datasets/YAHOO/" + index + ".json?auth_token=HP8mWGAmxhswaJQ_enkV&start_date=" + start + "&end_date=" + end;
var minDate = parseDate(start);
var maxDate = parseDate(end);

var dateRange = d3.time.days(minDate,maxDate);


//FAKE DATA
var allAreas = [];



for(var i = 0; i < 5; i++){
    var temp = [randomWalk(dateRange.length), randomWalk(dateRange.length), randomWalk(dateRange.length), randomWalk(dateRange.length), randomWalk(dateRange.length)];
    var tempArea = [];
  for(var j = 0; j < dateRange.length; j++){
              var partial1 = [temp[0][j], temp[1][j]];
              var stacked1 = partial1.reduce(function(pv, cv) { return pv + cv; }, 0);

              var partial2 = [temp[0][j], temp[1][j], temp[2][j]];
              var stacked2 = partial2.reduce(function(pv, cv) { return pv + cv; }, 0);

              var partial3 = [temp[0][j], temp[1][j], temp[2][j], temp[3][j]];
              var stacked3 = partial3.reduce(function(pv, cv) { return pv + cv; }, 0);

              var all = [temp[0][j], temp[1][j], temp[2][j], temp[3][j], temp[4][j]];
              var sum = all.reduce(function(pv, cv) { return pv + cv; }, 0);

              tempArea.push({
                date : dateRange[j],
                CategoryA : temp[0][j],
                CategoryB : temp[1][j],
                CategoryC : temp[2][j],
                CategoryD : temp[3][j],
                CategoryE : temp[4][j],
                StackedB : stacked1,
                StackedC : stacked2,
                StackedD : stacked3,
                Total: sum
                });
        };
allAreas[i] = tempArea;
};

var activeArea = allAreas [0];

console.log(allAreas);

// END FAKE DATA










var allDates = [];
    for(var i = 0; i < dateRange.length; i++){

        allDates.push({

        rawDate : dateRange[i],
        unparsedDate : unparse(dateRange[i])
                });
        };
var gData=[];
var dataDates = [];

var dataset = d3.json(request,function(data) {
	names = data.dataset.column_names;
	data = data.dataset.data;

	for(var i = 0; i < data.length; i++){
        data[i][0]=parseDate(data[i][0]);
        dataDates.push(unparse(data[i][0]));
        };

    for(var i = 0; i < allDates.length; i++){
    var matchIndex = $.inArray(allDates[i].unparsedDate,dataDates)
    var tempVal = "";
    if(matchIndex != -1){
        tempVal = data[matchIndex][1];
    }
    else{tempVal = gData[i-1].val ;};

    gData.push({
        date : dateRange[i],
        val : tempVal
        });
        };
 // console.log(gData);
 // console.log(data);
	// console.log(data);

// var diff = $(allDates).not(dataDates).get();


xScale = d3.time.scale()
								 .domain([minDate,maxDate])
								 .range([padding, w - padding]);

yScale = d3.scale.linear()
								 .domain([0,d3.max(gData, function(d) { return d.val; })])
								 .range([h - padding/1.5, padding]);

yScale2 = d3.scale.linear()
                                 .domain([0,d3.max(activeArea, function(d) { return d.Total; })])
                                 .range([h - padding/1.5, padding]);


var xAxis = d3.svg.axis()
							  .scale(xScale)
							  .orient("bottom")
							  .ticks(10);

			//Define Y axis
var yAxis = d3.svg.axis()
							  .scale(yScale)
							  .orient("left")
							  .ticks(5);

var yAxis2 = d3.svg.axis()
                              .scale(yScale2)
                              .orient("right")
                              .ticks(5);

var valueline = d3.svg.line()
    .x(function(d) { return xScale(d.date); })
    .y(function(d) { return yScale(d.val); });


var CategoryA = d3.svg.area()
    .x(function(d) { return xScale(d.date); })
    .y0(yScale2(0))
    .y1(function(d) { return yScale2(d.CategoryA); });

var CategoryB = d3.svg.area()
    .x(function(d) { return xScale(d.date); })
    .y0(function(d) { return yScale2(d.CategoryA); })
    .y1(function(d) { return yScale2(d.StackedB); });

var CategoryC = d3.svg.area()
    .x(function(d) { return xScale(d.date); })
    .y0(function(d) { return yScale2(d.StackedB); })
    .y1(function(d) { return yScale2(d.StackedC); });

var CategoryD = d3.svg.area()
    .x(function(d) { return xScale(d.date); })
    .y0(function(d) { return yScale2(d.StackedC); })
    .y1(function(d) { return yScale2(d.StackedD); });

var CategoryE = d3.svg.area()
    .x(function(d) { return xScale(d.date); })
    .y0(function(d) { return yScale2(d.StackedD); })
    .y1(function(d) { return yScale2(d.Total); });

dataSvg.append("path")
        .datum(activeArea)                                // **********
        .attr("class", "datalineA area")
        .style({fill: "#ee4035"})
        .attr("d", CategoryA);

dataSvg.append("path")
        .datum(activeArea)                                // **********
        .attr("class", "datalineB area")
        .style({fill: "#f37736"})
        .attr("d", CategoryB);

dataSvg.append("path")
        .datum(activeArea)                                // **********
        .attr("class", "datalineC area")
        .style({fill: "#fdf498"})
        .attr("d", CategoryC);

dataSvg.append("path")
        .datum(activeArea)                                // **********
        .attr("class", "datalineD area")
        .style({fill: "#7bc043"})
        .attr("d", CategoryD);

dataSvg.append("path")
        .datum(activeArea)                                // **********
        .attr("class", "datalineE area")
        .style({fill: "#0392cf"})
        .attr("d", CategoryE);

lineSvg.append("path")                                 // **********
        .attr("class", "line")
        .attr("d", valueline(gData));

graph.append("g")
    .attr("class", "x_axis axis") 
    .attr("transform", "translate(0," + (h - padding/1.5) + ")")//Assign "axis" class
    .call(xAxis);

graph.append("g")
    .attr("class", "y_axis axis")
    .attr("transform", "translate(" + padding + ",0)")//Assign "axis" class
    .call(yAxis);

graph.append("g")
    .attr("class", "y2_axis axis")
    .attr("transform", "translate(" + (w - padding) + ",0)")//Assign "axis" class
    .call(yAxis2);



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
        .attr("x2", w - padding);

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


});

function updateIndex() {

var index = $("input[name='index']:checked").val();
var request = "https://www.quandl.com/api/v3/datasets/YAHOO/" + index + ".json?auth_token=HP8mWGAmxhswaJQ_enkV&start_date=" + start + "&end_date=" + end;

 gData=[];
 dataDates = [];

var dataset = d3.json(request,function(data) {
    names = data.dataset.column_names;
    data = data.dataset.data;

    for(var i = 0; i < data.length; i++){
        data[i][0]=parseDate(data[i][0]);
        dataDates.push(unparse(data[i][0]));
        };

    for(var i = 0; i < allDates.length; i++){
    var matchIndex = $.inArray(allDates[i].unparsedDate,dataDates)
    var tempVal = "";
    if(matchIndex != -1){
        tempVal = data[matchIndex][1];
    }
    else{tempVal = gData[i-1].val ;};

    gData.push({
        date : dateRange[i],
        val : tempVal
        });
        };
 // console.log(gData);
 // console.log(data);
    // console.log(data);

// var diff = $(allDates).not(dataDates).get();




xScale = d3.time.scale()
                                 .domain([minDate,maxDate])
                                 .range([padding, w - padding]);

yScale = d3.scale.linear()
                                 .domain([0,d3.max(gData, function(d) { return d.val; })])
                                 .range([h - padding/1.5, padding]);


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
    .x(function(d) { return xScale(d.date); })
    .y(function(d) { return yScale(d.val); });

var newgraph = d3.select(".graph").transition();

newgraph.select(".line")   // change the line
            .duration(750)
            .attr("d", valueline(gData));

newgraph.select(".x_axis.axis") // change the x axis
            .duration(750)
            .call(xAxis);

newgraph.select(".y_axis.axis") // change the x axis
            .duration(750)
            .call(yAxis);
 
    });};



$("input[name='index']").change(function() {
  console.log("change");
  updateIndex();

});


function mousemove() {                              
        var x0 = xScale.invert(d3.mouse(this)[0]),             
            i = bisectDate(gData, (x0), 1),                   
            d0 = gData[i - 1],                              
            d1 = gData[i],                                 
            d = x0 - d0.date > d1.date - x0 ? d1 : d0;     
           // console.log(x0);
           // console.log(i);


        focus.select("circle.point")                           
            .attr("transform",                             
                  "translate(" + xScale(d.date) + "," +         
                                 yScale(d.val) + ")");

         focus.select("text.y1")
              .attr("transform",
                    "translate(" + xScale(d.date) + "," +
                                   yScale(d.val) + ")")
              .text(Math.round(d.val));

          focus.select("text.y2")
              .attr("transform",
                    "translate(" + xScale(d.date) + "," +
                                   yScale(d.val) + ")")
              .text(Math.round(d.val));

          focus.select("text.y3")
              .attr("transform",
                    "translate(" + xScale(d.date) + "," +
                                   yScale(d.val) + ")")
              .text(unparse(d.date));

          focus.select("text.y4")
              .attr("transform",
                    "translate(" + xScale(d.date) + "," +
                                   yScale(d.val) + ")")
              .text(unparse(d.date));

          focus.select(".x")
              .attr("transform",
                    "translate(" + xScale(d.date) + "," +
                                   yScale(d.val) + ")")
                         .attr("y2", h - yScale(d.val)-padding/1.5);

          focus.select(".y")
              .attr("transform",
                    "translate(0," + yScale(d.val) + ")");

    } 


window.onresize = function() {
     w = $("#map").width()-$(".indexSelection").width()-50;
     h = $(".graph").height();


xScale = d3.time.scale()
                 .domain([minDate,maxDate])
                 .range([padding, w - padding]);

yScale = d3.scale.linear()
                 .domain([0,d3.max(gData, function(d) { return d.val; })])
                 .range([h - padding/1.5, padding]);

yScale2 = d3.scale.linear()
                                 .domain([0,d3.max(activeArea, function(d) { return d.Total; })])
                                 .range([h - padding/1.5, padding]);


 xAxis = d3.svg.axis()
                .scale(xScale)
                .orient("bottom")
                .ticks(10);

      //Define Y axis
 yAxis = d3.svg.axis()
                .scale(yScale)
                .orient("left")
                .ticks(5);

 yAxis2 = d3.svg.axis()
                              .scale(yScale2)
                              .orient("right")
                              .ticks(5);

 valueline = d3.svg.line()
    .x(function(d) { return xScale(d.date); })
    .y(function(d) { return yScale(d.val); });


 CategoryA = d3.svg.area()
    .x(function(d) { return xScale(d.date); })
    .y0(yScale2(0))
    .y1(function(d) { return yScale2(d.CategoryA); });

 CategoryB = d3.svg.area()
    .x(function(d) { return xScale(d.date); })
    .y0(function(d) { return yScale2(d.CategoryA); })
    .y1(function(d) { return yScale2(d.StackedB); });

 CategoryC = d3.svg.area()
    .x(function(d) { return xScale(d.date); })
    .y0(function(d) { return yScale2(d.StackedB); })
    .y1(function(d) { return yScale2(d.StackedC); });

 CategoryD = d3.svg.area()
    .x(function(d) { return xScale(d.date); })
    .y0(function(d) { return yScale2(d.StackedC); })
    .y1(function(d) { return yScale2(d.StackedD); });

 CategoryE = d3.svg.area()
    .x(function(d) { return xScale(d.date); })
    .y0(function(d) { return yScale2(d.StackedD); })
    .y1(function(d) { return yScale2(d.Total); });




    var resize = d3.select(".graph").transition();

    resize.select("svg").attr("width", w)
                        .attr("height", h);

    resize.select(".line")   // change the line
            .duration(750)
            .attr("d", valueline(gData));


    resize.select(".datalineA")   // change the line
            .duration(750)
             .attr("d", CategoryA);

    resize.select(".datalineB")   // change the line
            .duration(750)
             .attr("d", CategoryB);

    resize.select(".datalineC")   // change the line
            .duration(750)
             .attr("d", CategoryC);

    resize.select(".datalineD")   // change the line
            .duration(750)
             .attr("d", CategoryD);

    resize.select(".datalineE")   // change the line
            .duration(750)
             .attr("d", CategoryE);

    resize.select(".x_axis.axis") // change the x axis
            .duration(750)
            .call(xAxis);

    resize.select(".y_axis.axis") // change the x axis
            .duration(750)
            .call(yAxis);

       resize.select(".y2_axis.axis") // change the x axis
            .duration(750)
            .attr("transform", "translate(" + (w - padding) + ",0)")
            .call(yAxis2);

    resize.select("rect") // change the x axis
            .duration(750)
            .attr("width", w)                             
            .attr("height", h)
    resize.select(".y")
        .duration(750)
        .attr("x2", w - padding);



};


