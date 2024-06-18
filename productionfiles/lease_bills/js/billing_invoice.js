if (!$) {
    // Need this line because Django also provided jQuery and namespaced as django.jQuery
    $ = django.jQuery;
}

$(document).ready(function () {
    var loaderContainer = $('<div class="loader-container" id="loader-container">');
    var loader = $('<div class="loader"></div>');

    // Append loader to the container
    loaderContainer.append(loader);

    // Append loader container to the body
    $('body').append(loaderContainer);

    // Hide loader initially
    hideLoader();

    // Show loader
    function showLoader() {
        loaderContainer.show();
    }

    // Hide loader
    function hideLoader() {
        loaderContainer.hide();
    }

    // Use Django admin's built-in submit events to show/hide loader
    $('form').submit(function () {
        showLoader();
    });

    $('.submit-row input[type="submit"]').click(function () {
        hideLoader();
    });
});

