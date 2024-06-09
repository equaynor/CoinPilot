# Testing

This is the TESTING file for the [CoinPilot](https://coinpilot.herokuapp.com/) website.

Return back to the [README.md](README.md) file.

## Testing Contents  

- [Testing](#testing)
  - [Testing Contents](#testing-contents)
  - [Validation](#validation)
    - [HTML Validation](#html-validation)
    - [JavaScript Validation](#javascript-validation)
    - [Python Validation](#python-validation)
    - [CSS Validation](#css-validation)
    - [Lighthouse Scores](#lighthouse-scores)
    - [Wave Accessibility Evaluation](#wave-accessibility-evaluation)
  - [Manual Testing](#manual-testing)
    - [User Input/Form Validation](#user-inputform-validation)
    - [Browser Compatibility](#browser-compatibility)
    - [Testing User Stories](#testing-user-stories)
    - [Dev Tools/Real World Device Testing](#dev-toolsreal-world-device-testing)
  - [Bugs](#bugs)
    - [Known Bugs](#known-bugs)

## Validation

### HTML Validation

For my HTML files, I have used the [HTML W3C Validator](https://validator.w3.org) to validate all of my HTML files.

I have had to follow a different approach for validating my HTML for this project as the majority of my pages are developed using Django templating syntax such as `{% extends "base.html" %}` and `{{ form|crispy }}` and most require user authentication. The HTML validator will throw errors if I were to use my website's URL, so I have had to follow the below approach for every page:

- Via the deployed Heroku app link, I have navigated to each individual page.
- Right clicking on the screen/CTRL+U/⌘+U on Mac, allows a menu to appear, giving me the option to 'View page source'.
- The complete HTML code for the deployed page will appear, allowing me to select the entire code using CTRL+A/⌘+A on Mac.
- Paste the copied code into the [validate by input](https://validator.w3.org/#validate_by_input) option.
- Check for errors and warnings, fix any issues, revalidate by following the above steps and record the results.

![html validation](documentation/testing/html_valid.png)  

All HTML pages were validated and received a 'No errors or warnings to show' result as shown above.

Initially, my Portfolio and Trade pages were receiving validator errors due to certain custom elements and Django-specific tags. I fixed these issues by ensuring proper nesting and closing of tags, re-deploying, and checking for any styling issues. All clear on re-validation thankfully.

| HTML Source Code/Page | Errors | Warnings |
| ---- | ------ | -------- | 
| Home | 0 | 0 |
| Sign In | 0 | 0 |
| Sign Up | 0 | 0 |
| Portfolios | 0 | 0 |
| Create Portfolio Modal| 0 | 0 |
| Edit Portfolio Modal | 0 | 0 |
| Delete Portfolio | 0 | 0 |
| Holding Details | 0 | 0 |
| Trade History | 0 | 0 |
| Add Trade | 0 | 0 |
| Edit Trade | 0 | 0 |
| Delete Trade | 0 | 0 |
| Coin List | 0 | 0 |
| Error 403 | 0 | 0 |
| Error 404 | 0 | 0 |
| Error 500 | 0 | 0 |

<hr>

### JavaScript Validation

[JSHint](https://jshint.com/) was used to validate the JavaScript code added to the project. External JS files, such as those for Bootstrap purposes, obtained via [CDN](https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.2.3/js/bootstrap.min.js), were not validated through JSHint.

| File | Screenshot | Errors | Warnings |
| ---- | ---------- | ------ | -------- |
| auto_refresh.js | ![js from auto_refresh.js](documentation/testing/auto_refresh_js.png) | none | none |
| create_portfolio.js | ![js from create_portfolio.js](documentation/testing/create_portfolio_js.png) | none | none |
| edit_portfolio.js | ![js from edit_portfolio.js](documentation/testing/edit_portfolio_js.png) | none | none |
| message.js | ![js from message.js](documentation/testing/message_js.png) | none | none |
| portfolio_selector.js | ![js from portfolio_selector.js](documentation/testing/portfolio_selector_js.png) | none | none |
| select2.js | ![js from select2.js](documentation/testing/select2_js.png) | none | none |
| trade_form.js | ![js from trade_form.js](documentation/testing/trade_form_js.png) | none | 10 |

All JavaScript files were validated as shown in the screenshots above.

<hr>

### Python Validation

[CI Python Linter](https://pep8ci.herokuapp.com/#) was used to validate the Python files that were created or edited by myself. No issues were presented, and line lengths were double-checked. Below is a screenshot with the results as an example.

![python validation](documentation/testing/python_valid.png)

<hr>

### CSS Validation 

[W3C CSS Validator](https://jigsaw.w3.org/css-validator/) was used to validate my CSS file. External CSS for Bootstrap, provided by [CDN](https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css) was not tested. Warnings were present, these were related to my use of variables for colors and fonts in my CSS file.

![css validation](documentation/testing/css_valid.png)
  
<hr> 