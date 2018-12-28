function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function() {
    $("#form-auth").submit(function(e){
        e.preventDefault();
        var id_name = $("#real-name").val();
        var id_card = $("#id-card").val();

        $.ajax({
            url:'/user/auth/',
            data:{'id_name':id_name,'id_card':id_card},
            dataType:'json',
            type:'POST',
            success:function(data){
                if(data.code == '200'){
                        auth()

    }}

})
})})

function auth(){
    $.get('/user/auth_info/',function(data){
        if(data.code==200){
             $("#real-name").val(data.user.id_name);
             $("#id-card").val(data.user.id_card);
             if(data.user.id_name){
                $('.btn-success').hide()
                $('#real-name').attr("disabled",true);
             }
             if(data.user.id_card){
                $('#id-card').attr("disabled",true);
             }
        }
    })
}
auth()