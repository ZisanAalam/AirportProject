function myFunction(){
    var blur = document.getElementById('del');
    blur.classList.add("active");
}

$( function() {
    $( "#id_start_date" ).datepicker({
        changeYear:true,
        changeMonth:true,
        dateFormat:'yy-mm-dd'
    });
} );

$( function() {
    $( "#id_end_date" ).datepicker({
        changeYear:true,
        changeMonth:true,
        dateFormat:'yy-mm-dd'
    });
} );