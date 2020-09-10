function load_posts (route) {
    
    document.getElementById('load_more_button').style.display = 'none'

    if ( route === undefined ) {
    
        var url = get_url()

    } else {

        var url = route

    }
    

    fetch(url,{
        method:'GET',
        headers:{
            'Content-Type':'application/json',
            'X-CSRF-Token':csrftoken
        },
    })

    .then((resp)=>{
        return resp.json()
    })

    .then((data)=>{

        if ( data['count'] == 0 ) {

            return  //We don't have any posts.

        }

        posts = data['results']

        for ( key in posts ) {

            var post = posts[key]

            thumbnail  =   post['thumbnail']
            title      =   post['title']
            sub_title  =   post['sub_title']
            author     =   post['author']
            created    =   post['created'].split('T')[0]
            slug       =   post['slug']

            var item = ('<div class="single-blog-post post-style-4 d-flex align-items-center wow " ><div class="post-thumbnail"><img src="../../../static'+thumbnail+'" alt=""></div><div class="post-content"><a href="../../../view_blog/'+slug+'" class="headline"><h5>'+ title +'</h5></a><p>'+sub_title+'...</p><div class="post-meta"><p><a href="../../../view/author/'+author+'" class="post-author">'+author+'</a> on <a  class="post-date">'+created+'</a></p></div></div></div>')
            document.getElementById('__main_posts__').innerHTML += item


        }

        if (data['next'] === null ) {

            //if we don't have another page.
            document.getElementById('load_more_button').style.display = 'none'

        } else { 

            document.getElementById('button_load-more').dataset.url = data['next']
            display_load_more_btn()
        }
    })
}

function load_more_posts(){

    var url = document.getElementById('button_load-more').dataset.url 
    
    document.getElementById('load_more_button').style.display = 'none'

    load_posts(url)
    
}

function display_load_more_btn(){

    document.getElementById('load_more_button').style.display = 'block'

}

function get_url(){

    
    var url = '../api/get/posts/my-uploads?'


    var search_query = document.getElementById('search_bar').value

    if ( search_query.trim().length !== 0 ) {

        url = url+ 'search='+search_query+'&'

    }

    var released = document.getElementsByName('released')

    for (let i = 0 ; i < released.length; i ++){

        if (released[i].checked){
            released = released[i].value 
            break
        }
    }

    if ( released !== "-1" ) {

        url = url + 'released='+released + '&'

    }

    var relivence = document.getElementsByName('relivence') 

    for (let i = 0 ; i < relivence.length; i ++){

        if (relivence[i].checked){
            relivence = relivence[i].value 
            break
        }
    }

    url = url + 'ordering=' + relivence + '&'

    return url

}


function apply_filters(){
    document.getElementById('button_load-more').dataset.url  = ''
    document.getElementById('__main_posts__').innerHTML = ''

    load_posts()

    document.getElementById('submit_button').removeAttribute('disabled')
    document.getElementById('submit_button').innerHTML = 'Apply Filters'
    document.getElementById('submit_button').classList.remove('disabled')

}


document.getElementById('filter_form').addEventListener('submit',function(e){

    e.preventDefault()

    document.getElementById('submit_button').setAttribute('disabled','disabled')
    document.getElementById('submit_button').innerHTML = 'Applying Filters....'
    document.getElementById('submit_button').classList.add('disabled')


    apply_filters()

})


load_posts()