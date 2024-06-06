
$(document).ready(function () {
    $('#editPortfolioBtn').click(function () {
        var form = $('#editPortfolioForm');
        var formData = form.serialize();
        var portfolioId = form.data('portfolio-id'); // Dynamically get the portfolio ID

        $.ajax({
            url: '/portfolio/edit/' + portfolioId + '/',
            type: 'POST',
            data: formData,
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val() // Include CSRF token
            },
            success: function (response) {
                if (response.status === 'success') {
                    $('#editPortfolioModal').modal('hide');
                    // Redirect to the portfolio detail page with the new portfolio ID
                    window.location.href = '/portfolio/details/' + response.portfolio_id + '/';
                } else {
                    console.log('Updating Portfolio failed.');
                }
            },
            error: function (xhr) {
                console.log('Error:', xhr.responseText);
            }
        });
    });
});
