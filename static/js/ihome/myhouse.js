$(document).ready(function(){
    $(".auth-warn").show();
    auth()
})
function auth(){
    $.get('/user/house_info/',function(data){
        if(data.code==200){
            if(data.user1.id_name){
                $(".auth-warn").hide();
                }
            for(i=0;i<data.house_info.length;i++){

                html= '<li><a href="/house/detail/?house_id=' + data.house_info[i].id + '"><div class="house-title"><h3>房屋ID:'+data.house_info[i].id+'</h3></div>'
                     + '<div class="house-content"><img src="/static/images/'+data.house_info[i].index_image_url+'"><div class="house-text">'
                     + '<ul><li>位于：'+data.house_info[i].address+'</li><li>价格：'+data.house_info[i].price+'</li><li>发布时间：'+data.house_info[i].create_time+'</li></ul>'
                     +'</div> </div> </a></li>'

                $('#houses-list').append(html);
            }
        };
        });
        }