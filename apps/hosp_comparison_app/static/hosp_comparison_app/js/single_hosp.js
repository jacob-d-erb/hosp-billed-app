var DRG_name_array = JSON.parse(document.getElementById('DRG_name_array').textContent);
var DRG_description_array = JSON.parse(document.getElementById('DRG_description_array').textContent);
var DRG_id_array = JSON.parse(document.getElementById('DRG_id_array').textContent);

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
});

$('#sh_gen').change(function(event){
    event.preventDefault()
    currSelectValue1 = $('#drg1_input').val();
    currSelectValue2 = $('#drg2_input').val();
    currSelectValue3 = $('#drg3_input').val();
    currSelectValue4 = $('#drg4_input').val();
    currSelectValue5 = $('#drg5_input').val();

    resetSelectLists(1, currSelectValue1);
    resetSelectLists(2, currSelectValue2);
    resetSelectLists(3, currSelectValue3);
    resetSelectLists(4, currSelectValue4);
    resetSelectLists(5, currSelectValue5);
    
    removeSelected(currSelectValue1, 2, 3, 4, 5);
    removeSelected(currSelectValue2, 1, 3, 4, 5);
    removeSelected(currSelectValue3, 1, 2, 4, 5);
    removeSelected(currSelectValue4, 1, 2, 3, 5);
    removeSelected(currSelectValue5, 1, 2, 3, 4);

    if($('#hosp_input').val()!=""){
        $.ajax({
            url: "/genspecifichosp",
            method: "post",
            data: $(this).serialize(),
            success: function(serverResponse){
                $('.graph_container').html(serverResponse)
            }
        })
    }
})

function resetSelectLists(selectInd, currentValue){
    $('#drg'+selectInd+'_input').children('option:not(:first)').remove();
    for (var i = 0; i < DRG_name_array.length; i++){
        var optValue = DRG_id_array[i];
        var optText = DRG_name_array[i] + " - " + DRG_description_array[i];
        $('#drg'+selectInd+'_input').append(`<option value="${optValue}">${optText}</option>`);
    }
    $('#drg'+selectInd+'_input').val(currentValue);
}

function removeSelected(currentValue, otherSelInd1, otherSelInd2, otherSelInd3, otherSelInd4){
    if(currentValue != ''){
        $("#drg"+otherSelInd1+"_input option[value='"+currentValue+"']").remove();
        $("#drg"+otherSelInd2+"_input option[value='"+currentValue+"']").remove();
        $("#drg"+otherSelInd3+"_input option[value='"+currentValue+"']").remove();
        $("#drg"+otherSelInd4+"_input option[value='"+currentValue+"']").remove();
    }
}