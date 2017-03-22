    var new_posts = 0;
    var latest_post_id = 0;
    var Posts = [];
    var User_Object = {};

    var startApp = function(){

        setInterval(function(){getPostsFromId(fetchLatestPostId());},5000)
        $('#posts_container').bind('click',function(event){doButtonAction(event)})
    }
    var fetchLatestPostId = function(){
        if(document.getElementById("posts_container").childNodes.length>0){
            latest_post_id = document.getElementById("posts_container").getElementsByClassName("post_id")[0].value
        }
        else{
            latest_post_id = 0;
        }
        return latest_post_id
    }

    var getPostsFromId = function(postId){
        console.log("get new posts")
        console.log(postId)
        var view = $('#page_view').val()
        $.ajax({
            url:'/new_posts/'+view+'/'+postId,
            success : function(result){
                console.log(result);
                addPoststoContainer(result);
                
            },
            failure: function(result){
                console.log(result)

            }

        });
    }

    var loadNewPosts = function(){
        loadLatestPoststoPage()

    }

    var loadLatestPoststoPage = function(){
        console.log(Posts)

    }

    var addPoststoContainer = function(postsHTML){
        console.log(postsHTML)
        if(postsHTML.length != 0){
            //updatePostsCount(Object.keys(posts).length)
            var temp = document.createElement("div")
            temp.innerHTML = postsHTML;
            var container = document.getElementById('posts_container')
            container.insertBefore(temp,container.childNodes[0])
        }
        
    }

    var doButtonAction = function(event){
        event.preventDefault();
        targetElement = event.target
        if(targetElement.id == "create_comment")
        {
            commentCreate =document.getElementById('comment_create')
            document.getElementById('comment_text').value = ""
            document.getElementById('comment_post_id').value = targetElement.getAttribute('post')
            targetElement.parentNode.insertBefore(commentCreate,targetElement.previousSibling)
            commentCreate.style.display="block";
        }
        else if(targetElement.id == "postComment")
        {
            comment = (targetElement.previousElementSibling.value)
            postId = (targetElement.nextElementSibling.value)
            csrftoken = getCookie('csrftoken')
            if(comment.length != 0 )
            {
                $.ajax({
                        url:"/create_comment",
                        type:"POST",
                        headers: { 
                            "X-CSRFToken" : csrftoken,
                            "Content-Type": "application/x-www-form-urlencoded"
                        },
                        data:{ "comment": comment, postId: postId },
                        dataType:"html",
                        success : function(result){
                        console.log(result);
                        addCommenttoPost(result);
                        }
                        });
            }
        }
        else if( event.target.value == "Follow")
        {
            csrftoken = getCookie('csrftoken')
            user = event.target.parentElement.action.split('/').reverse()[0]
            $.ajax({url:"/follow/"+user, type:"POST",headers: {"X-CSRFToken" : csrftoken},success:function(result){console.log(result);location.reload()}});
        }
        else if( event.target.value == "UnFollow")
        {
            csrftoken = getCookie('csrftoken')
            user = event.target.parentElement.action.split('/').reverse()[0]
            $.ajax({url:"/unfollow/"+user, type:"POST",headers: {"X-CSRFToken" : csrftoken},success:function(result){console.log(result);location.reload()}});
        }
        //event.stopImmediatePropagation()
    }
    
    var addCommenttoPost = function(commentHTML){
        console.log(commentHTML)
        if(commentHTML.length != 0){
            var temp = document.createElement("div")
            temp.innerHTML = commentHTML;
            postId = temp.getElementsByTagName('input')[0].value;
            var container = document.getElementById('display_post_'+postId).getElementsByClassName("comments_div")[0]
            container.insertAdjacentHTML('beforeend',commentHTML)
            document.getElementById('comment_text').value = "";
        }
    }

    var getCookie = function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
