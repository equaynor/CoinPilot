document.addEventListener('DOMContentLoaded', function() {
  // Check if there are any success messages
  const successMessages = JSON.parse(document.getElementById('messages').textContent);
  if (successMessages.length > 0) {
    successMessages.forEach(function(message) {
      if (message.tags === 'success') {
        // Display the success message in the modal
        document.getElementById('successMessage').textContent = message.message;
        document.getElementById('successModal').style.display = 'block';

        // Close the modal after 2 seconds
        setTimeout(function() {
          document.getElementById('successModal').style.display = 'none';
        }, 2000);
      }
    });
  }
});