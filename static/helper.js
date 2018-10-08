function mClick (y) {
  //alert(username)
      $.ajax({
          url : "/hover/" + '{{username}}' + '/',
          type: 'GET',
          success: function(result){
              //alert(result);
              $('.timeline').html(result);
          }
      });
  }

  