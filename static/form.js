$(document).ready(function(){
    $('#signin').click(function(){
        $.ajax({
            url : '/login/',
            type: 'GET',
            success: function(result){
                $(".parallax-w").html(result);
            }
        });
    });

    $('#signup').click(function(){
        $.ajax({
            url : '/register/',
            type: 'GET',
            success: function(result){
                $(".parallax-w").html(result);
            }
        });
    });

    $(".form11").find('#submit').click(function(event){
        event.preventDefault();
        var uname = $(".form11").find('#uname').val()
        var formdata1 = {
            'uname': $(".form11").find('#uname').val(),
            'pwd': $(".form11").find('#pwd').val(),
            'cook': $(".form11").find('#cook').val()
        }

        $.ajax({
            url : '/login/',
            type: 'POST',
            data: formdata1,
            success: function(result){
                if(result=='success') {
                    location.href = '/success/' + uname;
                }
                else if (result=='edit') {
                    location.href = '/edit/' + uname;
                }
                else {
                    $(".parallax-w").html(result);
                }
            }   
        });
    });

    $(".form22").find('#submit').click(function(event){
        event.preventDefault();
        var formdata2 = {
            'fname': $(".form22").find('#fname').val(),
            'uname': $(".form22").find('#uname').val(),
            'emailid': $(".form22").find('#emailid').val(),
            'pwd': $(".form22").find('#pwd').val()
        }

        $.ajax({
            url : '/register/',
            type: 'POST',
            data: formdata2,
            success: function(result){
                $(".parallax-w").html(result);
            }   
        });
    });
});