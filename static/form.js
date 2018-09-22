$(document).ready(function(){
    $('#signin').click(function(){
        req = $.ajax({
            url : '/log1/',
            type: 'GET',
            success: function(result){
                $(".parallax-w").html(result);
            }
        });
    });

    $('#signup').click(function(){
        req = $.ajax({
            url : '/reg1/',
            type: 'GET',
            success: function(result){
                $(".parallax-w").html(result);
            }
        });
    });
});