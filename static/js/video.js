// Update time every second
setInterval(() => {
    const timeElement = document.getElementById("time");
    const now = new Date();
    timeElement.textContent = now.toLocaleTimeString();
}, 1000);