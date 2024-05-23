// Function to refresh the page every 5 minutes (300,000 milliseconds)
function autoRefresh() {
    setTimeout(function() {
        location.reload();
    }, 300000); // 300,000 milliseconds = 5 minutes
}

// Call the autoRefresh function when the page loads
window.onload = autoRefresh;