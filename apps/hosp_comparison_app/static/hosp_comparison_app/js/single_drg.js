$(document).ready(function () {
    $("#sidebar").mCustomScrollbar({
        theme: "minimal"
    });

    $("#dismiss").on('click', function () {
        // hide sidebar
        $('#sidebar').addClass('active');
        // hide overlay
        $('.overlay').removeClass('active');
    });

    $('#sidebarCollapse').on('click', function () {
        // open sidebar
        $('#sidebar').removeClass('active');
        // fade in the overlay
        $('.overlay').addClass('active');
    });

    $("#drg_input").select2();
});

$('#sd_gen').change(function(event){

    if($('#drg_input').val()!=""){
        $.ajax({
            url: "/genspecificdrg",
            method: "post",
            data: $(this).serialize(),
            success: function(serverResponse){
                $('.graph_container').html(serverResponse)
            }
        })
    }
})
