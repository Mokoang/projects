if (!$) {
    // Need this line because Django also provided jQuery and namespaced as django.jQuery
    $ = django.jQuery;
}
$(document).ready(function() {
    $('input[Name="_addanother"]').hide();
    $('input[Name="_continue"]').hide();
    $('#view_id_landuse_type').hide();
    $('#add_id_landuse_type').hide();
    $('input[Name="_save"]').val("Next");
});
$(document).ready(function() {
    $('.btn-success').html('<i class="fa fa-plus-circle"></i> Add Lease');
    $('#myField').on('input', function(e) {
        var input = $(this).val();
        var key = e.key;

        // Allow only numbers and a dash
        if (!/^\d$|-/.test(key)) {
            // If entered character is not a number or dash, remove it
            $(this).val(input.replace(/[^\d-]/g, ''));
            return;
        }

        // Ensure the dash is only allowed at the specific position
        if (input.length === 5 && key !== "-") {
            e.preventDefault();
            return;
        }

        // Remove dashes from incorrect positions
        if (input.indexOf("-") !== -1 && input.indexOf("-") !== 5) {
            $(this).val(input.replace("-", ""));
            return;
        }

        // Insert dash at the specific position
        if (input.length === 5 && key === "-" || input.length === 6 && key !== "-") {
            $(this).val($(this).val() + "-");
        }
    });
});
$(document).ready(function() {
    $('#myField').keydown(function(e) {
        // Check if the pressed key is minus (-) or the numpad minus (109)
        if (e.which == 189 || e.which == 109) {
            // Check if the length of the input value is not equal to 5
            if ($(this).val().length !== 5) {
                // Prevent the default behavior of the key press
                e.preventDefault();

                // Replace the pressed character with whatever you want
                // For example, you can replace it with an empty string
                var cursorPosition = this.selectionStart;
                var textBefore = $(this).val().substring(0, cursorPosition);
                var textAfter = $(this).val().substring(cursorPosition + 1);
                $(this).val(textBefore + textAfter);

                // Optionally, you can also display a message to the user
                // to indicate that the input length should be 5
                // alert("Input length should be 5 characters.");
            }
        }
    });
});

$(document).ready(function() {
    $('#myField').on('keyup', function(e) {
        if (e.which != 8) {
            if ($(this).val().length == 5) {
                $(this).val($(this).val() + "-");
            }
        }
    });
});