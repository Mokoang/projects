if (!$) {
    // Need this line because Django also provided jQuery and namespaced as django.jQuery
    $ = django.jQuery;
}

$(document).ready(function () {
    $('#add_id_bill_period').hide();
    $('#view_id_bill_period').hide();
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

    // Show loader when clicking a button with the .btn class
    $('.btn').on('click', function () {
      
        showLoader();
        setTimeout(function(){
            loaderContainer.fadeOut('slow');
        }, 1000); // 3000 milliseconds = 3 seconds
    });
});
$(document).ready(function () {
    // Show loader when the page loads
    $('#loader-container').show();

    // Hide the loader after a delay
    setTimeout(function() {
        $('#loader-container').hide();
    }, 1000); // Adjust the delay time as needed
});



$(document).ready(function(){
    // Change button value to "Next"
    $('.btn-success').attr('value', 'Next');
});

$(document).ready(function(){
    $('#leases_div').hide();
});
$(document).ready(function(){
$('.btn-success').attr('value', 'Next');
});

$(document).ready(function(){
    $("input[name='_save']").on('click', function(e){
        // Prevent the default form submission
        e.preventDefault(); 

        // Find the form element
        var form = $('form#bill_form');
        
        if (form.length > 0) { // Check if form exists
            // Trigger form validation
            var isValid = form[0].checkValidity();

            if (isValid) {
                // Hide the form
                $('#content-main').hide();
            
                // Show the leases_div
                $('#leases_div').show();
            } else {
                // Form is invalid, display error messages
                form[0].reportValidity(); // Use reportValidity to show validation errors
            }
        } else {
            console.error("Form not found.");
        }
    });
});


$(function(){
    $('#save-button').on('click', function(e){
        e.preventDefault(); // Prevent the default form submission

        var ids = '';
        var count = 0;
        $('.cb:checked').each(function(){
            ids += $(this).closest('tr').find('#id').text() + ";";
            count+=1
        });
        if(count==0){
        alert("Please select a lease record before continuing!");
        }else{   
        $('#id_custom_data').text(ids); // Set the text of the custom data element

        var form = $('#bill_form');
                // Create a hidden input field and append it to the form
            var customDataInput = $('<input>').attr('type', 'hidden').attr('name', 'custom_data').val(ids);
        
        $('#bill_form').append(customDataInput);

        // Submit the form
        $('#bill_form').submit();

        }
    });
});


  $(function(){
    $('#acb').click(function(){
        if($(this).prop('checked')==true){
            $('.cb').each(function(){
                $(this).prop('checked',true);
          });
        }else if($(this).prop('checked')==false){
            $('.cb').each(function(){
               $(this).prop('checked',false);
        });  
        }
     });        
    });

    $(function(){
    $('.cb').click(function(){
       if($(this).prop('checked')==false){
         if($('#acb').prop('checked')==true){
            $('#acb').prop('checked',false);
         }  
        }
     });        
    });   
    
function myFunction() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[3];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}