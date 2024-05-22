document.addEventListener('DOMContentLoaded', function() {
    var portfolioDropdown = document.getElementById('portfolio_dropdown');
    if (portfolioDropdown) {
        portfolioDropdown.addEventListener('change', function() {
            var selectedPortfolioId = this.value;
            var form = this.form;
            var newAction = form.action.replace(/portfolio\/details\/\d+/, 'portfolio/details/' + selectedPortfolioId);
            form.action = newAction;
            form.submit();
        });
    }
});