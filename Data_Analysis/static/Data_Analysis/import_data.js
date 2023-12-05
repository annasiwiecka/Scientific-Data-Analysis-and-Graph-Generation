$(document).ready(function () {
    var loadingSpinner = $("#loading-spinner");

    function startLoadingSpinner() {
        loadingSpinner.show();
        animateDots();
    }

    function animateDots() {
        var dotsElement = $("#dots");
        var dots = 1;

        var dotsInterval = setInterval(function() {
            dotsElement.text(".".repeat(dots));

            dots = (dots % 3) + 1;
        }, 250);

        loadingSpinner.data("dotsInterval", dotsInterval);
    }

    $("form").submit(function() {
        startLoadingSpinner();
    })
});