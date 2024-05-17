
$(document).ready(function () {
    $('#createPortfolioBtn').click(function () {
        var form = $('#createPortfolioForm');
        var formData = form.serialize();

        $.ajax({
            url: '{% url "create_portfolio" %}',
            type: 'POST',
            data: formData,
            success: function (response) {
                if (response.status === 'success') {
                    $('#createPortfolioModal').modal('hide');
                    // Redirect to the portfolio detail page with the new portfolio ID
                    window.location.href = '/portfolio/' + response.portfolio_id + '/';
                } else {
                    console.log('Portfolio creation failed.');
                }
            },
            error: function (xhr) {
                console.log('Error:', xhr.responseText);
            }
        });
    });
});
