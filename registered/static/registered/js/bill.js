if (!$) {
    // Need this line because Django also provided jQuery and namespaced as django.jQuery
    $ = django.jQuery;
}

$(document).ready(function() {
  $('.btn-success').html(' <i class="fa fa-plus-circle"></i> New Bill');
  $('#add_id_lease_number').hide();
  $('#view_id_lease_number').hide();
  $('input[Name="_addanother"]').hide();
  $('input[Name="_continue"]').hide();
  $('input[Name="_save"]').val("Generate Bill");
 
 
  
/*  $('.btn-success').html(' <i class="fa fa-plus-circle"></i> Surrender Lease');
  $('#id_lease_number').on('change',function(){
    let $this = $(this);
    let $clone = $this.clone();
    $('#input-text').html($(this).clone());
  });*/
});

