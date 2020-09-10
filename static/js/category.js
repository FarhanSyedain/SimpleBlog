
if (__page__ == 'category' || __page__ == 'tag'){

    document.getElementById('form___').addEventListener('submit',function(e){
        e.preventDefault()
        search_query()
    })

    function search_query(){
        
        var query_ = document.getElementById('search').value
        if (query_.trim().length == 0){
            return
        }
        window.location = '../../../search/posts/'+query_

    }

    function get_url(){
        
        if (__page__ == 'tag'){

            var url = '../../../api/get/query?tag='+tag

        } else {

            var url = '../../../api/get/query?category='+category

        }

        return url

    }


    function load_posts(url_){


        if (url_ !== undefined){
            var url = url_
        } else {
            var url = get_url()
        }

        fetch(url,{
            method:'GET',
            headers:{
                'Content-Type':'application/json',
                'X-CSRF-Token':csrftoken
            }
        })

        .then((response)=>{
            return response.json()
        })
        
        .then((data)=>{

            posts = data['results']
            
            if (url_ === undefined && data['count'] === 0){

                document.getElementById('__main_posts__').innerHTML += '<h1 class="text-center">No Posts Found.</h1>'
                return
            }

            for (post in posts){

                obj = posts[post]

                thumbnail = obj['thumbnail']
                title = obj['title']
                sub_title = obj['sub_title']
                author = obj['author']
                created = obj['created'].split('T')[0]
                slug = obj['slug']

                var item = ('<div class="single-blog-post post-style-4 d-flex align-items-center wow " ><div class="post-thumbnail"><img src="../../../static'+thumbnail+'" alt=""></div><div class="post-content"><a href="../../../view_blog/'+slug+'" class="headline"><h5>'+ title +'</h5></a><p>'+sub_title+'...</p><div class="post-meta"><p><a href="../../../view/author/'+author+'" class="post-author">'+author+'</a> on <a  class="post-date">'+created+'</a></p></div></div></div>')

                document.getElementById('__main_posts__').innerHTML += item

            }

            if (data['next'] !== null) {
            
                document.getElementById('button_load-more').dataset.url = data['next']
                document.getElementById('load_more_button').style.display = 'block'

            } else {

                document.getElementById('load_more_button').innerHTML = ' '

            }

        })
    }
        load_posts()


        function load_more_posts(){

            document.getElementById('load_more_button').style.display = 'none'
            var url_ = document.getElementById('button_load-more').dataset.url

            load_posts(url_)

        }
}