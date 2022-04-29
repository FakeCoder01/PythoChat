$(document).ready(function(){
    setInterval(function(){
        $.ajax({
            type: "GET",
            url: "/loadChats/",
            data: {
                'room_id' : document.getElementById("room_id").value,
                'room_name': document.getElementById("room_name").value,
                'user_name': document.getElementById("user_name").value,
            },
            success: function(response){
                $("#comments").empty();
                for (var key in response.chats){           
                    var temp = '<div class="row"><div class="col-lg-12"><div class="media"><div class="media-body"><h4 class="media-heading">' + response.chats[key].user_name + '<span class="small pull-right">' + response.chats[key].created_on + '</span></h4><p>' + response.chats[key].msg + '</p></div></div></div></div><hr>';
                    $("#comments").append(temp);
                }
            },
            error: function(response){
                console.log("An error occurred")
            }
        });
    },1000); //1000
});





function addMsg(){
msg = document.getElementById("comment").value;
$.ajax({
    type: "POST",
    url: "/addChats/",
    data: {
        'msg' : msg,
        'room_id' : document.getElementById("room_id").value,
        'room_name' : document.getElementById("room_name").value,
        'user_name' : document.getElementById("user_name").value,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    },
    success: function(msg){
        document.getElementById("comment").value = '';
    }
});
}