if (!$) {
    // Need this line because Django also provided jQuery and namespaced as django.jQuery
    $ = django.jQuery;
}

$(document).ready(function() {

  $('input[Name="_addanother"]').hide();
  $('input[Name="_continue"]').hide();
  $('#add_id_landuse_type').hide();
  $('#view_id_landuse_type').hide();
  $('.btn-success').html(' <i class="fa fa-plus-circle"></i> Add Ground Rent Rates');
/*  
  $('.btn-success').html(' <i class="fa fa-plus-circle"></i> Surrender Lease');
  $('#id_lease_number').on('change',function(){
    let $this = $(this);
    let $clone = $this.clone();
    $('#input-text').html($(this).clone());
  });*/
});

