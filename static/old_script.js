
var data = [];
var eventOutputContainer = document.getElementById("message");
var eventSrc = new EventSource("/eventSource");
var tipswitch = 0;
eventSrc.onmessage = function(e) {
	console.log(e);
	eventOutputContainer.innerHTML = e.data;
};

var tooltip = d3.select("div.tooltip");
var tooltip_title = d3.select("#title");
var tooltip_price = d3.select("#price");

// uncheck radios:
var allRadios = document.getElementsByName('Return');
var booRadio;
var x = 0;
for(x = 0; x < allRadios.length; x++){

    allRadios[x].onclick = function() {
        if(booRadio == this){
            this.checked = false;
            booRadio = null;
        }else{
            booRadio = this;
        }
    };
}

var QStart =  start + " 00:00:00";
var QEnd = end + " 00:00:00";


$(".analysis").click(function(){
tipswitch = 1;
})

$(document).click(function(){
	   console.log(monthend);
	var overlay = $("input[name='overlay']:checked").val();
	var Return  = $("input[name='Return']:checked").val();
	var Analysis  = $("input[name='analysis']:checked").val();
	var Fake  = $("input[name='fake']:checked").val();
	var weekwidth = $("rect.w0").attr("weekwidth");
	console.log(weekwidth);


	if(Return == "regionalReturn")
	{
	$(".regional").removeClass("visible");
	ResetGraph();
	$("input[name='Return']:checked").attr('checked', false);
	groups.selectAll("circle").classed("active", false);
	}

	if (Analysis == "Total"){
		groups.selectAll("circle").classed("weeks",false);
		groups.selectAll("circle.w0").classed("weeks",true);
		groups.selectAll("circle").attr("r", function(d){ return d.R });
for(var i = 0; i < 4; i++){                     
    graph.selectAll("rect.w"+i).transition().delay((4-i)*100)                               
          .attr("width", 0)                             
          .style("opacity", 0);                       
             };   

        if(	tipswitch == 1){
		QStart =  start + " 00:00:00";
		QEnd = end + " 00:00:00";
		updateData();


        };
}

	if (Analysis == "Month"){
		groups.selectAll("circle").classed("weeks",false);
		groups.selectAll("circle.w0").classed("weeks",true);
		groups.selectAll("circle").attr("r", function(d){ return d.R });
for(var i = 1; i < 4; i++){                     
    graph.selectAll("rect.w"+i).transition().delay((4-i)*100)                               
          .attr("width", 0)                             
          .style("opacity", 0);                       
             };
    graph.selectAll("rect.w0").transition()                              
          .attr("width", eval(weekwidth)*4)                             
          .style("opacity", 1);
    
    if(	tipswitch == 1){
    			QStart =  monthstart + " 00:00:00";
		QEnd = monthend + " 00:00:00";
		updateData();
    };  

}

if (Analysis == "Weeks"){
		groups.selectAll("circle").classed("weeks",true);
            groups.selectAll("circle").attr("r", function(d){console.log(d.newRadius); return d.newRadius/2});
for(var i = 0; i < 4; i++){                     
    graph.selectAll("rect.w"+i).transition().delay(i*100)                               
          .attr("width", eval(weekwidth))                             
          .style("opacity", 1);                       
             };
if(	tipswitch == 1){
	    			QStart =  monthstart + " 00:00:00";
		QEnd = monthend + " 00:00:00";
		updateData();
};

}

if (Fake == "No"){
		groups.selectAll("circle").classed("weeks",false);
		hideAreas();
            }

else if(ActiveCategory == "" ){
	 ResetGraph();
}

else{
	updateArea();
}
            ;
 
tipswitch = 0;

});


var map = L.map('map').setView([22.769630, 113.707588], 10);

//this is the OpenStreetMap tile implementation

// L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
// 	attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
// }).addTo(map);

//uncomment for Mapbox implementation, and supply your own access token

		L.tileLayer('https://api.tiles.mapbox.com/v4/{mapid}/{z}/{x}/{y}.png?access_token={accessToken}', {
			attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
			mapid: 'mapbox.light',
			accessToken: 'pk.eyJ1Ijoic2t5bGFyYnIiLCJhIjoiY2lmaW84czRuYm5ybXJ5bHh5YnM5a3lzdiJ9.EFoA13UUx70WH41vhjRyuw'
		}).addTo(map);

//create variables to store a reference to svg and g elements



var svg_overlay = d3.select(map.getPanes().overlayPane).append("svg");
var g_overlay = svg_overlay.append("g").attr("class", "leaflet-zoom-hide");

var svg = d3.select(map.getPanes().overlayPane).append("svg");
var g = svg.append("g").attr("class", "leaflet-zoom-hide");
var groupsvg = d3.select( map.getPanes().overlayPane ).append("svg").attr("class", "areas");
var groups = groupsvg.append("g").attr("class", "leaflet-zoom-hide");

function projectPoint(lat, lng) {
	return map.latLngToLayerPoint(new L.LatLng(lat, lng));
}

function projectStream(lat, lng) {
	var point = projectPoint(lat,lng);
	this.stream.point(point.x, point.y);
}

var transform = d3.geo.transform({point: projectStream});
var path = d3.geo.path().projection(transform);

function updateData(){

	var mapBounds = map.getBounds();
	var lat1 = mapBounds["_southWest"]["lat"];
	var lat2 = mapBounds["_northEast"]["lat"];
	var lng1 = mapBounds["_southWest"]["lng"];
	var lng2 = mapBounds["_northEast"]["lng"];

	// CAPTURE USER INPUT FOR CELL SIZE FROM HTML ELEMENTS
	// var cell_size = $("input[name='grid']:checked").val();
	var w = window.innerWidth;
	var h = window.innerHeight;

	// CAPTURE USER INPUT FOR ANALYSIS TYPE SELECTION
	var overlay = $("input[name='overlay']:checked").val();

	// CAPTURE USER INPUT FOR HEAT MAP 'SPREAD' OR OTHER PARAMETERS
	var spread = $("input[name='spread']:checked").val();
	var results = $("input[name='results']:checked").val();



	// SEND USER CHOICES FOR ANALYSIS TYPE, CELL SIZE, HEAT MAP SPREAD, ETC. TO SERVER
	request = "/getData?lat1=" + lat1 + "&lat2=" + lat2 + "&lng1=" + lng1 + "&lng2=" + lng2 + "&w=" + w + "&h=" + h + "&starttime=" + QStart + "&endtime=" + QEnd

	console.log(request);

  	d3.json(request, function(data) {

		//create placeholder circle geometry and bind it to data

		// call function to update geometry
		update();
		map.on("viewreset", update);

		if ((overlay == "interpolation") || (overlay == "heatmap")){


			var topleft = projectPoint(lat2, lng1);

			svg_overlay.attr("width", w)
				.attr("height", h)
				.style("left", topleft.x + "px")
				.style("top", topleft.y + "px");

			var rectangles = g_overlay.selectAll("rect").data(data.analysis);
			rectangles.enter().append("rect");

			rectangles
				.attr("x", function(d) { return d.x; })
				.attr("y", function(d) { return d.y; })
				.attr("width", function(d) { return d.width; })
				.attr("height", function(d) { return d.height; })
		    	.attr("fill-opacity", ".2")
		    	.attr("fill", function(d) { return "hsl(" + Math.floor((1-d.value)*250) + ", 100%, 50%)"; });
		
		};

		// function to update the data
		function update() {

			// g.selectAll("circle").remove();

			g_overlay.selectAll("rect").remove()

			// get bounding box of data
		    var bounds = path.bounds(data),
		        topLeft = bounds[0],
		        bottomRight = bounds[1];

		    var buffer = 50;

		    // reposition the SVG to cover the features.
		    svg .attr("width", bottomRight[0] - topLeft[0] + (buffer * 2))
		        .attr("height", bottomRight[1] - topLeft[1] + (buffer * 2))
		        .style("left", (topLeft[0] - buffer) + "px")
		        .style("top", (topLeft[1] - buffer) + "px");

		    g   .attr("transform", "translate(" + (-topLeft[0] + buffer) + "," + (-topLeft[1] + buffer) + ")");

		    // update circle position and size


			var circles = g.selectAll("circle").data(data.features);

			circles.exit().remove();
			console.log(data);

			circles.enter()
				.append("circle")
				.on("mouseover", function(d){
					tooltip.style("visibility", "visible");
					// tooltip_title.text(d.properties.name);
					// tooltip_price.text("Price: " + d.properties.price);
				})
				.on("mousemove", function(){
					tooltip.style("top", (d3.event.pageY-10)+"px")
					tooltip.style("left",(d3.event.pageX+10)+"px");
				})
				.on("mouseout", function(){
					tooltip.style("visibility", "hidden");
				})

				// .attr("fill", function(d) { return "hsl(" + Math.floor((1-d.properties.priceNorm)*250) + ", 100%, 50%)"; })
			;


		    circles
		    	.attr("cx", function(d) { return projectPoint(d.geometry.coordinates[0], d.geometry.coordinates[1]).x; })
		    	.attr("cy", function(d) { return projectPoint(d.geometry.coordinates[0], d.geometry.coordinates[1]).y; })
    			.attr("r", 5)
    			.attr("class", "dataPoint")
				.exit();
		};
	});

};


function drawCircles(i){
   data = [];

  for(var i = 0; i < 4; i++)
  	data.push(
    { "coords" : [ 22.987269, 113.743628 ], "R" : (allTotals[0]/50),"ID" : "A", "ID2" : 0, "week" : (i), "Color" : "#556270" },
    { "coords" : [ 23.094686, 113.304175 ], "R" : (allTotals[1]/50),"ID" : "B", "ID2" : 1, "week" : (i), "Color" : "#4eccc3" },
    { "coords" : [ 22.503470, 114.111670 ], "R" : (allTotals[2]/50),"ID" : "C", "ID2" : 2, "week" : (i), "Color" : "#c7f464" },
    { "coords" : [ 22.483169, 113.453863 ], "R" : (allTotals[3]/50),"ID" : "D", "ID2" : 3, "week" : (i), "Color" : "#ff6b64" },
    { "coords" : [ 22.941748, 113.177832 ], "R" : (allTotals[4]/50),"ID" : "E", "ID2" : 4, "week" : (i), "Color" : "#ffb04d" });
  

  data.map( function(d){ var newPoint = map.latLngToLayerPoint( d.coords ); d.coords = { 'x' : newPoint.x, 'y' : newPoint.y }; return d; } );



 groups.selectAll("circle").data( data ).enter().append("circle")
    .attr("cx", function(d){return d.coords.x } )
    .attr("cy", function(d){ return d.coords.y } )
    .attr("r", function(d){ return d.R } )
    .attr("ID",function(d){ return d.ID } )
    .attr("ID2",function(d){ return d.ID2 } )
    .attr("week",function(d){ return d.week } )
    .attr("class",(function(d){ return "w" + d.week } ))
    .style("fill", function(d){ return d.Color })
    .on("click", function(d){
    				ActiveCategory = d3.select(this).attr("ID");
    				updateArea();
    				groups.selectAll("circle").classed("active", false);
    				d3.select(this).classed("active", true);
    })
    ;};
    drawCircles(4);
updateData();