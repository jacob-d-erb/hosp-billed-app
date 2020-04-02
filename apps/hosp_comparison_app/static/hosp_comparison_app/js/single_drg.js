$(document).ready(function () {
    $("#drg_input").select2({
        width: '100%'
    });
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

$(window).resize(function(){

    if($('#drg_input').val()!=""){
        $.ajax({
            url: "/genspecificdrg",
            method: "post",
            data: $('#sd_gen').serialize(),
            success: function(serverResponse){
                $('.graph_container').html(serverResponse)
            }
        })
    }
})
