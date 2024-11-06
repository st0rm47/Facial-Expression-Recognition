// Update time every second
setInterval(() => {
    document.getElementById("time").textContent = new Date().toLocaleTimeString();
}, 1000);

// Start the video stream and capture frames for emotion detection
async function startCamera() {
    const video = document.getElementById("videoElement");

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;

        // Capture and process a frame every 100ms
        setInterval(() => captureFrame(video), 100);
    } catch (error) {
        console.error("Error accessing the camera:", error);
        alert("Camera access denied. Please grant permission to continue.");
    }
}

function captureFrame(video) {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL("image/jpeg");

    // Send frame to server
    fetch("/process_frame", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: dataURL.split(",")[1] })  // Only the base64 data
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("emotion").textContent = data.emotion;
        } else {
            document.getElementById("emotion").textContent = "No face detected";
        }
    })
    .catch(err => console.error("Error processing frame:", err));
}

// Start the camera on page load
window.onload = startCamera;