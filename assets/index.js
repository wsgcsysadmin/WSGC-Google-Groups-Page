$(document).ready(function() {
    $('input[type="text"]').keyup(function(e) {
        if(e.keyCode == 27) {
            $(this).val('');
            userList.search();
        }
    });
});
