function confirmDeletion() {
    const selectedPortfolio = document.getElementById('portfolio_dropdown').selectedOptions[0].text;
    return confirm(`Are you sure you want to delete the portfolio: ${selectedPortfolio}?`);
}