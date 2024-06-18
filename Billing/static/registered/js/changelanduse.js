if (!$) {
    // Need this line because Django also provided jQuery and namespaced as django.jQuery
    $ = django.jQuery;
}
$(document).ready(function() {
  $('#add_id_lease_number').hide();
  $('#view_id_lease_number').hide();
  $('input[Name="_addanother"]').hide();
  $('input[Name="_continue"]').hide();
$('.btn-success').html(' <i class="fa fa-plus-circle"></i> Change Land-use');

  
});