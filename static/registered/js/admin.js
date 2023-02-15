if (!$) {
    // Need this line because Django also provided jQuery and namespaced as django.jQuery
    $ = django.jQuery;
}
$(document).ready(function() {
  $('input[Name="_addanother"]').hide();
  $('input[Name="_continue"]').hide();
  $('#view_id_landuse_type').hide();
  $('#add_id_landuse_type').hide();
  
});
$(document).ready(function() {
  
  $('.btn-success').html(' <i class="fa fa-plus-circle"></i> Add Lease');
  $('#myField').on('keydown',function(e){

    if(e.which!=8){
     if($(this).val().length==5){
        $(this).val($(this).val()+"-");
     }else if($(this).val()[$(this).val().length-1]=='-'){
        $(this).val($(this).val().slice(0,-1))
     }
   }
    
  });
});
