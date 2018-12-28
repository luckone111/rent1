function logout() {
    $.get("/user/logout/", function(data){
        if (code == 200) {
            location.href = "/user/login/";
        }
    })
}

$(document).ready(function(){
    $.get('/user/my_info/',function(data){

        if(data.code == 200){
            $('#user-name').text(data.my_info.name)
            $('#user-mobile').text(data.my_info.phone)
            $('#user-avatar').attr('src', '/static/images/' + data.my_info.avatar)
        }
    })

})