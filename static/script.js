

var eventOutputContainer = document.getElementById("message");
var eventSrc = new EventSource("/eventSource");

eventSrc.onmessage = function(e) {
	eventOutputContainer.innerHTML = e.data;
};

var tooltip = d3.select("div.tooltip");
var tooltip_title = d3.select("#title");
var tooltip_category = d3.select("#cat");


var map = L.map('map').setView([22.929935, 113.639837], 16);

var markerClicked = false;
	

//this is the OpenStreetMap tile implementation
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

//uncomment for Mapbox implementation, and supply your own access token

L.tileLayer('https://api.tiles.mapbox.com/v4/{mapid}/{z}/{x}/{y}.png?access_token={accessToken}', {
 	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
 	mapid: 'mapbox.dark',
 	accessToken: 'pk.eyJ1IjoiaXZyaWVsNTAxIiwiYSI6ImNpZm9wNnY4OWhwYjhzeWx4bDJucWFkeGgifQ.Hl_QF7F6JApTIPOeHBXlGQ'
 }).addTo(map);

//create variables to store a reference to svg and g elements

d3.select(map.getPanes().overlayPane).on("click", showLines);

var svg = d3.select(map.getPanes().overlayPane).append("svg");
var g_line = svg.append("g").attr("class", "leaflet-zoom-hide");
var g = svg.append("g").attr("class", "leaflet-zoom-hide");

function projectPoint(lat, lng) {
	return map.latLngToLayerPoint(new L.LatLng(lat, lng));
}

function projectStream(lat, lng) {
	var point = projectPoint(lat,lng);
	this.stream.point(point.x, point.y);
}

var transform = d3.geo.transform({point: projectStream});
var path = d3.geo.path().projection(transform);


function remap(value, min1, max1, min2, max2){
	return (min2) + ((value) - (min1)) * ((max2) - (min2)) / ((max1) - (min1));
}

function updateData(){

	var mapBounds = map.getBounds();
	var lat1 = mapBounds["_southWest"]["lat"];
	var lat2 = mapBounds["_northEast"]["lat"];
	var lng1 = mapBounds["_southWest"]["lng"];
	var lng2 = mapBounds["_northEast"]["lng"];

	request = "/getData?lat1=" + lat1 + "&lat2=" + lat2 + "&lng1=" + lng1 + "&lng2=" + lng2

	console.log(request);

	g.selectAll("circle").remove()
	g_line.selectAll("line").remove()

  	d3.json(request, function(data) {

		//create placeholder circle geometry and bind it to data
		var circles = g.selectAll("circle").data(data.features);

		circles.enter()
			.append("circle")
			.on("mouseover", function(d){
				tooltip.style("visibility", "visible");
				tooltip_title.text(d.properties.name);
				tooltip_category.text("Category: " + d.properties.cat);
			})
			.on("mousemove", function(){
				tooltip.style("top", (d3.event.pageY-10)+"px")
				tooltip.style("left",(d3.event.pageX+10)+"px");
			})
			.on("mouseout", function(){
				tooltip.style("visibility", "hidden");
			})
			.on("click", function(d){
				hideLines(d.id);
			})
			.attr("r", 7)
		;

		var lines = g_line.selectAll("line").data(data.lines);
		lines.enter().append("line")

		// call function to update geometry
		update();
		map.on("viewreset", update);

		// function to update the data
		function update() {

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
		    g_line.attr("transform", "translate(" + (-topLeft[0] + buffer) + "," + (-topLeft[1] + buffer) + ")");

		    // update circle position and size
		    circles
		    	.attr("cx", function(d) { return projectPoint(d.geometry.coordinates[0], d.geometry.coordinates[1]).x; })
		    	.attr("cy", function(d) { return projectPoint(d.geometry.coordinates[0], d.geometry.coordinates[1]).y; })
    		;

			lines
				.attr("x1", function(d) { return projectPoint(d.coordinates[0], d.coordinates[1]).x; })
				.attr("y1", function(d) { return projectPoint(d.coordinates[0], d.coordinates[1]).y; })
				.attr("x2", function(d) { return projectPoint(d.coordinates[2], d.coordinates[3]).x; })
				.attr("y2", function(d) { return projectPoint(d.coordinates[2], d.coordinates[3]).y; })
			;
		};

		function hideLines(id) {

			markerClicked = true;

			var others = [id];

			lines.transition()
				.style("stroke-opacity", .5)
				.style("stroke-width", function(d) { 
					if (d.from == id ){
						others.push(d.to);
						return 3;
					};
					if(d.to == id ){
						others.push(d.from);
						return 3;
					}; 
				})
				.style("visibility", function(d) { 
					if (d.from == id || d.to == id){
						return "visible";
					}else{
						return "hidden";
					}; 
				})
			;

			var minVal = 1000000000;
			var maxVal = 0;

			circles
				.style("visibility", function(d) { 

					var val = d.properties.score;

					for (var i = 0; i < others.length; i++){
						if (d.id == others[i]){
							if (val > maxVal){
								maxVal = val;
							}								
							if (val < minVal){
								minVal = val;
							}

							return "visible";
						}
					}
					return "hidden";
				})
			;

			circles.transition()
				.attr("r", function(d) { 
					for (var i = 0; i < others.length; i++){
						if (d.id == others[i]){
							return remap(d.properties.score, minVal, maxVal, 10, 30);
						}
					}
					return 7;
				})
			;
		};
	});

};




function showLines() {

	if (markerClicked == true){
		markerClicked = false
		return
	}

	g_line.selectAll("line")
		.transition()
		.style("stroke-opacity", .2)
		.style("stroke-width", 1)
		.style("visibility", "visible")
	;

	g.selectAll("circle")
		.transition()
		.attr("r", 7)
		.style("visibility", "visible")
	;
};

updateData();