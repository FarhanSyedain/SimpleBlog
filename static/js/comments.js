if (c){

   


    var loaded_comments = false
    var category = '{{blog.category}}'

    if (localStorage.getItem('history__') == undefined){

        var id_ = null

    } else {

        var id_ = localStorage.getItem('history__')

    }

    url = '../../api/create/cookie-model/history'

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'id':id_,'category':category})
    })

    .then((resp)=>{
        return resp.json()
    })

    .then((data)=>{
        if (data['do'] == undefined){
           if (data['id']!== undefined){
               localStorage.setItem('history__',data['id'])
           }
            
        }else{
           
        }
    })
}

function getCookie(name) {

    // Split cookie string and get all individual name=value pairs in an array

    var cookieArr = document.cookie.split(";");

    // Loop through the array elements

    for (var i = 0; i < cookieArr.length; i++) {

        var cookiePair = cookieArr[i].split("=");

        /* Removing whitespace at the beginning of the cookie name

        and compare it with the given string */

        if (name == cookiePair[0].trim()) {

            // Decode the cookie value and return

            return decodeURIComponent(cookiePair[1]);

        }
    }
}

const csrftoken__ = getCookie('csrftoken')

function load_posts(route) {

    if ( route == undefined ) { 
        var url = '../../api/get/comments?post='+post_id
    } else {
        var url = route
    }

    fetch(url,{
        method:'GET',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        }
    })

    .then((resp)=>{
        return resp.json()
    })
    
    .then((data)=>{

        if ( data['count'] == 0 ) {
            //break , we dont have any comments
            document.getElementById('loading__').outerHTML = ''
        }

        comments = data['results']

        for (key in comments){

            var comment = comments[key]//Access the comment array
            var username = comment['user']
            var body = comment['comment_body']
            var posted = comment['posted'].split('T')[0]

            item = ('<li class="single_comment_area"><div class="comment-content"><div class="comment-meta d-flex align-items-center justify-content-between"><p><a class="post-author">'+username+'</a> on <a class="post-date">'+posted+'</a></p></div><p>'+body+'</p></div></li>')

            document.getElementById('all_comments').innerHTML += item

        }

        if ( data['next'] !== null ) {

            document.getElementById('load_more_button').dataset.url = data['next'] 

            //Shoe load-more button
            document.getElementById('load_more_button').style.display = 'block'

            document.getElementById('loading__').style.display = 'none'


        } else {
            
            document.getElementById('extra_').dataset.loaded = 'true'
            document.getElementById('extra_').innerHTML = ''

        }
    })
}


function load_more_comments() {

    url = document.getElementById('load_more_button').dataset.url

    //Hide load-more button
    document.getElementById('load_more_button').style.display = 'none'

    document.getElementById('loading__').style.display = 'block'

    load_posts(url)

}

load_posts()

document.getElementById('post_commen__t').addEventListener('submit',function(e){
    e.preventDefault()
    post_comment()
})




function post_comment() {

    var body = document.getElementById('message').value
   
    var url = '../../api/post/comment'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken__
        },
        body:JSON.stringify({'body':body,'post':post_id})
    })

    .then((resp)=>{
        return resp.json()
    })


    .then((data)=>{

        if (data['success']) {

            document.getElementById('message').value = ''


            var username = data['author']
            var body = data['Comment_body']
            var posted = data['dated'].split('T')[0]


            if (document.getElementById('extra_').dataset.loaded = 'true'){
                item = ('<li class="single_comment_area"><div class="comment-content"><div class="comment-meta d-flex align-items-center justify-content-between"><p><a class="post-author">'+username+'</a> on <a class="post-date">'+posted+'</a></p></div><p>'+body+'</p></div></li>')
                document.getElementById('all_comments').innerHTML += item   
            } else {
                
            }
                

        } else {

            window.alert('Failed to post comment!')

        }
    })
}


function follow_unfollow_user(){

    var button_ = document.getElementById('follow_unfollow_button')

    button_.setAttribute('disabled','disabled')
    button_.classList.add('disabled')

    if (button_.dataset.current === 'follow' ){

        //Then we need to follow the author

        var url = "../api/blog/post/user/follow"

        fetch(url,{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken__
            },
            body:JSON.stringify({'blog_post_id':post_id})
        })

        .then((resp)=>{
            return resp.json()
        })
        
        .then((data)=>{
            
            if (data['success']){


                button_.dataset.current = 'unfollow'
                button_.innerHTML = 'UnFollow'
                button_.removeAttribute('disabled')
                button_.classList.remove('disabled')


            } else {

                button_.removeAttribute('disabled')
                button_.classList.remove('disabled')

                window.alert('Can\'t Follow Author')

            }

        })
 
    } else {

        //We need to unfollow the author

        var url = "../api/blog/post/user/unfollow"

        fetch(url,{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken__
            },
            body:JSON.stringify({'blog_post_id':post_id})
        })

        .then((resp)=>{
            return resp.json()
        })
        
        .then((data)=>{
            
            if (data['success']){


                button_.dataset.current = 'follow'
                button_.innerHTML = 'Follow'
                button_.removeAttribute('disabled')
                button_.classList.remove('disabled')


            } else {

                button_.removeAttribute('disabled')
                button_.classList.remove('disabled')

                window.alert('Can\'t Un-Follow Author')

            }

        })

    }

    
}

function like_this_post(){

    var like_button = document.getElementById('like_unlike_button')

    like_button.removeAttribute('onclick')

    if (like_button.dataset.current == 'liked'){

        //Then Un-like the post

        var url = '../api/blog/post/stars/unlike'

        fetch(url,{

            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken__
            },
            body:JSON.stringify({'post_id':post_id})
            
        })
        
        .then((resp)=>{
            return resp.json()
        })

        .then((data)=>{

            if (data['success']){

                like_button.setAttribute('onclick','like_this_post()')
                
                like_button.dataset.current = "unrated"

                like_button.classList.remove('text-danger')


            } else {

                like_button.setAttribute('onclick','like_this_post()')

                window.alert('Cannot Like The Post , Sorry!')

            }

        })



    } else {

         //Then Un-like the post

         var url = '../api/blog/post/stars/like'

         fetch(url,{
 
             method:'POST',
             headers:{
                 'Content-Type':'application/json',
                 'X-CSRFToken':csrftoken__
             },
             body:JSON.stringify({'post_id':post_id})
             
         })
         
         .then((resp)=>{
             return resp.json()
         })
 
         .then((data)=>{
 
             if (data['success']){
 
                 like_button.setAttribute('onclick','like_this_post()')
                 
                 like_button.dataset.current = "liked"
 
                 like_button.classList.add('text-danger')
 
 
             } else {
 
                 like_button.setAttribute('onclick','like_this_post()')
 
                 window.alert('Cannot Un-Like The Post , Sorry!')
 
             }
 
         })
 

    }

}