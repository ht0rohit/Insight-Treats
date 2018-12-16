$(document).ready(function(){
    $('.details2').find('#submit').click(function(event){
        

        //$('.details2').find('#uname').attr('value','{{username}}');
        event.preventDefault();
        //var uname = $(".form11").find('#uname').val()
        if ($(".details2").find('#python').prop('checked')) {
            var python = 'y';
        }
        if ($(".details2").find('#cpp').prop('checked')) {
            var cpp = 'y';
        }
        if ($(".details2").find('#java').prop('checked')) {
            var java = 'y';
        }
        if ($(".details2").find('#js').prop('checked')) {
            var js = 'y';
        }
        if ($(".details2").find('#iot').prop('checked')) {
            var iot = 'y';
        }
        if ($(".details2").find('#ml').prop('checked')) {
            var ml = 'y';
        }
        if ($(".details2").find('#vr').prop('checked')) {
            var vr = 'y';
        }
        if ($(".details2").find('#ar').prop('checked')) {
            var ar = 'y';
        }
        if ($(".details2").find('#cc').prop('checked')) {
            var cc = 'y';
        }
        if ($(".details2").find('#eh').prop('checked')) {
            var eh = 'y';
        }

        var formdata1 = {
            'uname': $(".details2").find('#uname').attr("value"),
            'p_name': $(".details2").find('#p_name').val(),
            'des': $(".details2").find('#des').val(),
            'python': python,
            'cpp': cpp,
            'java': java,
            'js': js,
            'iot': iot,
            'ml': ml,
            'vr': vr,
            'ar': ar,
            'cc': cc,
            'eh': eh
        }

        $.ajax({
            url : '/save/',
            type: 'POST',
            data: formdata1,
            success: function(result){
                $(".appnd2").html(result);
                $(".details2").find('#p_name').text('');
                $(".details2").find('#des').text('');
                $(".details2").find('#python').prop('checked', false);
                $(".details2").find('#cpp').prop('checked', false);
                $(".details2").find('#java').prop('checked', false);
                $(".details2").find('#js').prop('checked', false);
                $(".details2").find('#iot').prop('checked', false);
                $(".details2").find('#ml').prop('checked', false);
                $(".details2").find('#vr').prop('checked', false);
                $(".details2").find('#ar').prop('checked', false);
                $(".details2").find('#cc').prop('checked', false);
                $(".details2").find('#eh').prop('checked', false);
                //$(".appnd2").html(result);
            }   
        });
    });
});

