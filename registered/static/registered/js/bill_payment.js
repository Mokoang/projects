if (!$) {
    // Need this line because Django also provided jQuery and namespaced as django.jQuery
    $ = django.jQuery;
}
$(document).ready(function() {
  $('#add_id_lease_number').hide();
  $('#view_id_lease_number').hide();
  $('#change_id_lease_number').hide();
});
