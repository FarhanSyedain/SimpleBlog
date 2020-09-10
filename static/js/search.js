var tag = '';
var category = '';

document.getElementById('form___').addEventListener('submit',function(e){
    e.preventDefault()
    search_query()
})

function search_query(){
    
    var query_ = document.getElementById('search').value
    if (query_.trim().length == 0){
        return
    }
    window.location = '../'+query_

}

function apply_filters(){

    
    var tag_ = document.getElementById('tag__').value
    var category_ = document.getElementById('category__').value
    
    if (tag_ == tag && category_ == category){
        return
    }
    tag = tag_
    category = category_


    document.getElementById('appling_filters').classList.remove('hidden')
    document.getElementById('__main_posts__').innerHTML = ''

    load_posts(get_url())

}

function load_posts(url){

    if (url == undefined){

        var url = get_url()

    } else { 

       var url = url

    }

    fetch(url,{
        method:'GET',
        headers:{
            'Content-Type':'application/json',
            'X-CSRF-Token':csrftoken
        }
    })

    .then((resp)=>{

        return resp.json()

    })

    .then((data)=>{

        if (data['count'] == 0){
            document.getElementById('appling_filters').classList.add('hidden')
            document.getElementById('__main_posts__').innerHTML += '<p>No results found </p>'
           
            return
        }

        posts = data['results']


        for (key in posts){

            obj = posts[key]

            thumbnail = obj['thumbnail']
            title = obj['title']
            sub_title = obj['sub_title']
            author = obj['author']
            created = obj['created'].split('T')[0]
            slug = obj['slug']

            var item = ('<div class="single-blog-post post-style-4 d-flex align-items-center wow " ><div class="post-thumbnail"><img src="../../../static'+thumbnail+'" alt=""></div><div class="post-content"><a href="../../../view_blog/'+slug+'" class="headline"><h5>'+ title +'</h5></a><p>'+sub_title+'...</p><div class="post-meta"><p><a href="../../../view/author/'+author+'" class="post-author">'+author+'</a> on <a class="post-date">'+created+'</a></p></div></div></div>')

            document.getElementById('__main_posts__').innerHTML += item

        }

        document.getElementById('appling_filters').classList.add('hidden')

        if (data['next'] !== null) {
           
            document.getElementById('button_load-more').dataset.url = data['next']
            document.getElementById('load_more_button').style.display = 'block'

        } else { 

            document.getElementById('load_more_button').innerHTML = ' '

        }
    })
}

function get_url(url){

    if (url == undefined){
        var url = '../../../api/get/query/?'
    } else {
        if (url[url.length] !== '&'){
            var url = url + '&'
        }
    }

    if (tag.trim().length !== 0){
        url = url + 'tag='+tag + '&'

    }

    if (category.trim().length !== 0){
        url = url + 'category='+category + '&'

    }
    url = url + 'search=' +search_query +'&'

    return url
}

function load_more_posts(){

    document.getElementById('load_more_button').style.display = 'none'
    var url_ = document.getElementById('button_load-more').dataset.url

    url = get_url(url_)

    load_posts(url)

}

load_posts()