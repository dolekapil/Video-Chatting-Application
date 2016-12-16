// This is our entry-point javascript file for the video chat application.
// author: Kapil Dole and Soni Pandey

var constraints = window.constraints = {
  audio: true,
  video: true
};

navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {

	var SimplePeer = require('simple-peer');

	var simplePeerObject = new SimplePeer({
		trickle: false,
		initiator: location.hash === "#initiator"
	});

	simplePeerObject.on('signal', function (data) {
		document.getElementById('myTextareaID').value = JSON.stringify(data);
	});

	document.getElementById('sendMessageButton').addEventListener('click', function() {
		var message = document.getElementById('messageToSend').value;
		simplePeerObject.send(message);
		document.getElementById('replyLabel').textContent += "Me: " + message + "\n";
		document.getElementById('messageToSend').value = "";
	});

	document.getElementById('connectButton').addEventListener('click', function() {
		if(document.getElementById('otherTextareaID').value === " ") {
			alert("Please enter other person's ID to connect.");
		} else {
			var hideElements = document.getElementsByClassName('content')
			for (var i = 0; i < hideElements.length; i++){
				hideElements[i].style.display = 'none';
			}
			
			var unhideElements = document.getElementsByClassName('chatContent');
			for (var i = 0; i < unhideElements.length; i++){
				unhideElements[i].style.display = 'block';
			}
		}
	});

	simplePeerObject.on('data', function (data) {
		document.getElementById('replyLabel').textContent += "Friend: " + data + "\n";
	});

	document.getElementById('otherTextareaID').addEventListener('blur', function() {
		var ID = JSON.parse(document.getElementById('otherTextareaID').value);
		simplePeerObject.signal(ID);
	}, true);
	
	simplePeerObject.on('signal', function (data) {
		var videoElement = document.createElement('video');
		videoElement.style.paddingLeft = "32%";
		videoElement.style.display = 'none';
		videoElement.setAttribute("id", "videoElementID");
		document.body.appendChild(videoElement);
		videoElement.src = window.URL.createObjectURL(stream);
	});
	
	document.getElementById('startVideoChatButton').addEventListener('click', function() {
		document.getElementById('videoElementID').style.display = 'block';
	});
	
}, function (error) {
	if (error.name === 'ConstraintNotSatisfiedError') {
    errorMsg('The given resolution is not supported by your device.');
  } else if (error.name === 'PermissionDeniedError') {
    errorMsg('Permissions have not been granted to use microphone and camera.');
  }
  errorMsg('Error: ' + error.name, error);
});

