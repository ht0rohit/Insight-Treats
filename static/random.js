$(document).ready(function(){
    $('.details2').find('#submit').click(function(event){
        

        //$('.details2').find('#uname').attr('value','{{username}}');
        event.preventDefault();
        //var uname = $(".form11").find('#uname').val()
        
        var formdata1 = {
            'uname': $(".details2").find('#uname').attr("value"),
            'p_name': $(".details2").find('#p_name').val(),
            'des': $(".details2").find('#des').val(),
            'lang': $(".details2").find('#lang').val()
        }

        $.ajax({
            url : '/save/',
            type: 'POST',
            data: formdata1,
            success: function(result){
                $(".appnd2").html(result);
                $(".details2").find('#p_name').text(''),
                $(".details2").find('#des').text(''),
                $(".details2").find('#lang').text('')
            }   
        });
    });
});

