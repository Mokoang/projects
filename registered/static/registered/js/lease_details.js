if (!$) {
    // Need this line because Django also provided jQuery and namespaced as django.jQuery
    $ = django.jQuery;
}
$(document).ready(function() {
  $('input[Name="_addanother"]').hide();
  $('input[Name="_continue"]').hide();
  $('#view_id_landuse_type').hide();
  $('#add_id_landuse_type').hide();
  $('#view_id_lease_number').hide();
$('#add_id_lease_number').hide();
  
});
