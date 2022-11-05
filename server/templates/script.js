var canvas = document.getElementById("canvas_diagramm");
var canvasWidth = 400;
var canvasHeight = 350;
canvas.setAttribute('width', canvasWidth);
canvas.setAttribute('height', canvasHeight);
var cv = canvas.getContext("2d");
//Options Grid
var graphGridSize = 20;
var graphGridX = (canvasWidth / graphGridSize).toFixed();
//Draw Grid
for(var i = 0; i < graphGridX; i ++){
	cv.moveTo(canvasWidth, graphGridSize*i);
	cv.lineTo(0, graphGridSize*i);
}
cv.strokeStyle = "#dbdbdb";
cv.stroke();





let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 8,
  });
}

window.initMap = initMap;