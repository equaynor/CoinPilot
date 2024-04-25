// Hide the success message after 3 seconds (adjust the duration as needed)
$(document).ready(function() {
  setTimeout(function() {
      $('#successMessage').fadeOut('slow');
  }, 3000);
});