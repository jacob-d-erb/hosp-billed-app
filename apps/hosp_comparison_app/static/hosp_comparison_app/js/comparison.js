var hosp_name_array = JSON.parse(document.getElementById('hosp_name_array').textContent);
var hosp_id_array = JSON.parse(document.getElementById('hosp_id_array').textContent);

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


$('#comp_gen').change(function(event){
    event.preventDefault();
    
    // Dynamically changes dropdowns.

    currSelectValue1 = $('#hosp1_input').val();
    currSelectValue2 = $('#hosp2_input').val();
    currSelectValue3 = $('#hosp3_input').val();
    currSelectValue4 = $('#hosp4_input').val();
    currSelectValue5 = $('#hosp5_input').val();

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

    // Ajax call for graph.

    if(($('#hosp1_input').val()!="" || $('#hosp2_input').val()!="" || $('#hosp3_input').val()!="" || $('#hosp4_input').val()!="" || $('#hosp5_input').val()!="") && $('#drg_input').val()!=""){
        $.ajax({
            url: "/gencomparison",
            method: "post",
            data: $(this).serialize(),
            success: function(serverResponse){
                $('.graph_container').html(serverResponse)
            }
        })
    };

});

function resetSelectLists(selectInd, currentValue){
    $('#hosp'+selectInd+'_input').children('option:not(:first)').remove();
    for (var i = 0; i < hosp_name_array.length; i++){
        var optValue = hosp_id_array[i];
        var optText = hosp_name_array[i];
        $('#hosp'+selectInd+'_input').append(`<option value="${optValue}">${optText}</option>`);
    }
    $('#hosp'+selectInd+'_input').val(currentValue);
}

function removeSelected(currentValue, otherSelInd1, otherSelInd2, otherSelInd3, otherSelInd4){
    if(currentValue != ''){
        $("#hosp"+otherSelInd1+"_input option[value='"+currentValue+"']").remove();
        $("#hosp"+otherSelInd2+"_input option[value='"+currentValue+"']").remove();
        $("#hosp"+otherSelInd3+"_input option[value='"+currentValue+"']").remove();
        $("#hosp"+otherSelInd4+"_input option[value='"+currentValue+"']").remove();
    }
}