$(document).ready(function() {
  var canvas, context;

  // Find the canvas element.
  canvas = document.getElementById('imageView');
  if (!canvas) {
    alert('Error: I cannot find the canvas element!');
    return;
  }
  if (!canvas.getContext) {
    alert('Error: no canvas.getContext!');
    return;
  }
  // Get the 2D canvas context.
  context = canvas.getContext('2d');
  if (!context) {
    alert('Error: failed to getContext!');
    return;
  }

  var started = false;
  var ws = new WebSocket("ws://127.0.0.1:5000/echo");
  ws.onopen = function() {
    ws.send("socket open");
    console.log("opened console");
  }
  ws.onmessage = function(evt) {
    data = evt.data.split(',');
    cmd = data[0];

    if (cmd == 'log') {
      console.log(data[1]);
    } else if (cmd == 'point') {
      var x = data[1];
      var y = data[2];
      newPath = data.length > 3;
      if (!started || newPath) {
        context.beginPath();
        context.moveTo(x, y);
        started = true;
      } else {
        context.lineTo(x, y);
        context.stroke();
      }
    }
  }
});
