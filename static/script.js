
var eventOutputContainer = document.getElementById("message");
var eventSrc = new EventSource("/eventSource");

eventSrc.onmessage = function(e) {
	eventOutputContainer.innerHTML = e.data;
};

//Setting up global variables to show time and day on the tooltip
var tooltip = d3.select("div.tooltip");
var tooltip_time = d3.select("#time");
var tooltip_day = d3.select("#day");

//Setting the map central point location and zoom level so that the scope of downtown Shenzhen show up upon opening the web page
var map = L.map('map').setView([22.539029, 114.062076], 13);

var markerClicked = false;
	
var svg_overlay = d3.select(map.getPanes().overlayPane).append("svg");
var g_overlay = svg_overlay.append("g").attr("class", "leaflet-zoom-hide");

var svg = d3.select(map.getPanes().overlayPane).append("svg");
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

	var cell_size = 20;
	var w = window.innerWidth;
	var h = window.innerHeight;

	var checked = document.getElementById("heatmap").checked

	//Setting up variables containing "day of week" and "time of day" by getting values from the html file
	var dropdownDay_object = document.getElementById("dropdownDay");
	var dropdownDay = dropdownDay_object.options[dropdownDay_object.selectedIndex].value;

	var dropdownTime_object = document.getElementById("dropdownTime");
	var dropdownTime = dropdownTime_object.options[dropdownTime_object.selectedIndex].value;

	//Get client information and send to the server
  	request = "/getData?lat1=" + lat1 + "&lat2=" + lat2 + "&lng1=" + lng1 + "&lng2=" + lng2 + "&w=" + w + "&h=" + h + "&cell_size=" + cell_size + "&analysis=" + checked + "&dayOfWeek=" + dropdownDay +"&timeOfDay=" + dropdownTime

	console.log(request);

	//Set up the basemap to show dark basemap when "time of day" is set to "Evening" or "Night", and light basemap for "Morning" and "Day"
	if (dropdownTime==0|dropdownTime==3){
		L.tileLayer('https://api.tiles.mapbox.com/v4/{mapid}/{z}/{x}/{y}.png?access_token={accessToken}', {
 		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
 		mapid: 'mapbox.dark',
 		accessToken: ['pk.eyJ1IjoiZWttaW5vdWdvdSIsImEiOiJjaWk0djNhcWowMWdtdG9rZnE3b3RybWEzIn0.LZVMU9yjc00114OdlzAzxg']
		 }).addTo(map);
	}
	else {
		L.tileLayer('https://api.tiles.mapbox.com/v4/{mapid}/{z}/{x}/{y}.png?access_token={accessToken}', {
 		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
 		mapid: 'mapbox.light',
 		accessToken: ['pk.eyJ1IjoiZWttaW5vdWdvdSIsImEiOiJjaWk0djNhcWowMWdtdG9rZnE3b3RybWEzIn0.LZVMU9yjc00114OdlzAzxg']
		 }).addTo(map);
	}

	g.selectAll("circle").remove()

  	d3.json(request, function(data) {

		//create placeholder circle geometry and bind it to data
		var circles = g.selectAll("circle").data(data.features);

			circles.enter()
				.append("circle")
				.on("mouseover", function(d){
					tooltip.style("visibility", "visible");
					tooltip_time.text(d.properties.time);
					tooltip_day.text(d.properties.day);
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

		update();
		map.on("viewreset", update);

		//setting up the heatmap
		if (checked == true){

			var topleft = projectPoint(lat2, lng1);

			console.log(lat2);

			svg_overlay.attr("width", w)
				.attr("height", h)
				.style("left", topleft.x + "px")
				.style("top", topleft.y + "px");

			//create placeholder rect geometry and bind it to data
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
		    circles
		    	.attr("cx", function(d) { return projectPoint(d.geometry.coordinates[0], d.geometry.coordinates[1]).x; })
		    	.attr("cy", function(d) { return projectPoint(d.geometry.coordinates[0], d.geometry.coordinates[1]).y; })
    		;
			
		};
		
});
};


updateData();