// Update time every second
setInterval(() => {
    const timeElement = document.getElementById("time");
    const now = new Date();
    timeElement.textContent = now.toLocaleTimeString();
}, 1000);


// Function to start the video stream
async function startCamera() {
    const video = document.getElementById('videoElement');

    // Prompt user for permission to use the camera
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;

        // Optionally, you can send frames to your Flask server for processing
        // This is where you could set up an interval to capture frames
        // setInterval(() => { sendFrame(video); }, 100);
    } catch (error) {
        console.error("Error accessing the camera: ", error);
        alert("Error accessing the camera. Please grant permission to use the camera.");

    }
}

// Update the time every second
setInterval(function () {
    document.getElementById("time").innerText = new Date().toLocaleTimeString();
}, 1000);

// Ask for permission to use the camera
window.onload = startCamera();