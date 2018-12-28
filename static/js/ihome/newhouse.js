function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $.get('/house/area_facility/', function(data){
        if(data.code == '200'){
            for(var i=0; i<data.areas.length; i++){
                area_str = '<option value="' + data.areas[i].id + '">' + data.areas[i].name + '</option>'
                $('#area-id').append(area_str)
            }

            for(var j=0; j<data.facilitys.length; j++){
                facility_str = '<li><div class="checkbox"><label>'
                facility_str += '<input type="checkbox" name="facility" value="' + data.facilitys[j].id + '">' + data.facilitys[j].name
                facility_str += '</label></div></li>'

                $('.house-facility-list').append(facility_str)
            }

        }
    });

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    $("#form-house-info").submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/house/newhouse/',
            dataType:'json',
            type:'POST',
            success:function(data){
                if(data.code == 200){
                    $("#form-house-image").show()
                    $('#house-id').val(data.house_id);
              }
            }
        })

    })
    $("#form-house-image").submit(function(e){
        $(this).ajaxSubmit({
            url:'/house/house_images/',
            dataType:'json',
            type:'POST',
            success:function(data){
                if(data.code == 200){
                    var img_src = '<img src="/static/images/' + data.image_url + '">'
                    $('.house-image-cons').append(img_src)
                }
                }
            })
            })
        });
})