function on(z) {
    $.ajax({
        url : "/project/" + '{{username}}' + '/',
        type: 'GET',
        success: function(result){
            //alert(result);
          $(".timeline").html(result);
        }   
    });
}