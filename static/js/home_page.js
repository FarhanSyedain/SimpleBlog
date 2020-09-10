if (__page__ == 'home'){

    document.getElementById('form___').addEventListener('submit',function(e){
        e.preventDefault()
        search_query()
    })

    function search_query(){
        
        var query_ = document.getElementById('search').value
        if (query_.trim().length == 0){
            return
        }
        window.location = 'search/posts/'+query_

    }

    const id_ = localStorage.getItem('history__')

    document.cookie = 'categories_visited=' + id_

    function load_first_section(){


        var url = 'api/home/get/trending'

        fetch(url,{
            method:'GET',
            headers:{'Content-Type':'application/json','X-CSRF-Token':csrftoken,'id':id_}
        })

        .then((resp)=>{
            return resp.json()
        })

        .then((data)=>{
            
            var main_post = document.createElement('div')
            main_post.classList = "col-12 col-md-6"
            
            for (i = 0; i < 1; i ++) {

                obj = data[i]
                title = obj['title']
                sub_title = obj['sub_title']
                body = obj['body']
                thumbnail = obj['thumbnail']
                slug = obj['slug']
                category = obj['category']
                created = obj['created'].split('T')[0]
                author = obj['author']

                var div_ = ('<div class="single-blog-post"><div class="post-thumbnail"><img src="static'+ thumbnail +'" alt=""><div class="post-cta"><a href="posts/category/'+category+'">' + category + '</a></div></div><div class="post-content"><a href="view_blog/'+slug+'" class="headline"><h5>'+ title +'</h5></a><p>' + sub_title + '...</p><div class="post-meta"><p><a href="view/author/'+author+'" class="post-author">'+ author +'</a> on <a class="post-date">'+ created +'</a></p></div></div></div>')

                main_post.innerHTML += div_

            }
            
            var other_posts = document.createElement('div')

            other_posts.classList = "col-12 col-md-6"

            for (i = 1; i < data.length; i++ ) {

                obj = data[i]
                title = obj['title']
                sub_title = obj['sub_title']
                body = obj['body']
                thumbnail = obj['thumbnail']
                slug = obj['slug']
                category = obj['category']
                created = obj['created'].split('T')[0]
                author = obj['author']

                var div_ = ('<div class="single-blog-post post-style-2 d-flex align-items-center mb-1"><div class="post-thumbnail"><img src="static'+thumbnail+'" alt=""></div><div class="post-content"><a href="view_blog/'+slug+'" class="headline"><h5>'+title+'</h5></a><div class="post-meta"><p><a href="view/author/'+author+'" class="post-author">'+author+'</a> on <a  class="post-date">'+created+'</a></p></div></div></div>')

                other_posts.innerHTML += div_

            }


            var row = document.createElement('div')
            row.classList = 'row'

            row.appendChild(main_post)
            row.appendChild(other_posts)

            document.getElementById('first_section____').innerHTML = ''
            document.getElementById('first_section____').appendChild(row)

        })
    }


    function load_snd_section(url){
        if (url ==  undefined){
            var url = 'api/home/get/reccomended'

        }else{
            var url = url
        }


        fetch(url,{
            method:'GET',
            headers:{'Content-Type':'application/json','X-CSRF-Token':csrftoken,'id':id_}
        })

        .then((resp)=>{
            return resp.json()
        })

        .then((data)=>{

            var row = document.createElement('div')
            row.classList = 'col-12 col-md-6'
            

            for (let i= 0; i< 3; i++ ) {

                if (data.length <= i){
                    continue
                }

                var obj = data[i]

                title = obj['title']
                sub_title = obj['sub_title']
                body = obj['body']
                thumbnail = obj['thumbnail']
                slug = obj['slug']
                category = obj['category']
                created = obj['created'].split('T')[0]
                author = obj['author']

                var div = ('<div class="single-blog-post post-style-2 d-flex align-items-center mb-1"><div class="post-thumbnail"><img src="static'+thumbnail+'" alt=""></div><div class="post-content"><a href="view_blog/'+slug+'" class="headline"><h5>'+title+'</h5></a><div class="post-meta"><p><a href="view/author/'+author+'" class="post-author">'+author+'</a> on <a class="post-date">'+created+'</a></p></div></div></div>')

                row.innerHTML += div

            }

            var row_two = document.createElement('div')

            row_two.classList = 'col-12 col-md-6'

            for (let i= 3; i< data.length; i++){

                if (data.length <= i){
                    continue
                }
                var obj = data[i]

                title = obj['title']
                sub_title = obj['sub_title']
                body = obj['body']
                thumbnail = obj['thumbnail']
                slug = obj['slug']
                category = obj['category']
                created = obj['created'].split('T')[0]
                author = obj['author']

                var div = ('<div class="single-blog-post post-style-2 d-flex align-items-center mb-1"><div class="post-thumbnail"><img src="static'+thumbnail+'" alt=""></div><div class="post-content"><a href="view_blog/'+slug+'" class="headline"><h5>'+title+'</h5></a><div class="post-meta"><p><a href="view/author/'+author+'" class="post-author">'+author+'</a> on <a class="post-date">'+created+'</a></p></div></div></div>')

                row_two.innerHTML += div

            }

            var row_ = document.createElement('div')
            row_.classList = 'row'

            row_.appendChild(row)
            row_.appendChild(row_two)


            document.getElementById('scnd_section__').innerHTML = ''
            document.getElementById('scnd_section__').appendChild(row_)


        })

    }

    function load_all_posts(url){

        if (url == undefined){
            var url = 'api/home/get/all_posts'

        }else{
            var url = url
        }


        fetch(url,{
            method:'GET',
            headers:{'Content-Type':'application/json','X-CSRF-Token':csrftoken,'id':id_}
        })

        .then((resp)=>{
            return resp.json()
        })

        .then((data)=>{

            data_ = data['results']
            
            document.getElementById('jlfdsjflksdfjsdlf').style.display = 'none'

            for (i in data_){

                obj = data_[i]

                title = obj['title']
                sub_title = obj['sub_title']
                body = obj['body']
                thumbnail = obj['thumbnail']
                slug = obj['slug']
                category = obj['category']
                created = obj['created'].split('T')[0]
                author = obj['author']

                var item = ('<div class="single-blog-post post-style-4 d-flex align-items-center wow " ><div class="post-thumbnail"><img src="static'+thumbnail+'" alt=""></div><div class="post-content"><a href="view_blog/'+slug+'" class="headline"><h5>'+ title +'</h5></a><p>'+sub_title+'...</p><div class="post-meta"><p><a href="view/author/'+author+'" class="post-author">'+author+'</a> on <a class="post-date">'+created+'</a></p></div></div></div>')

                document.getElementById('fdsfsdfsdfasdfdsfasd').innerHTML += item

                if (data['next']) {

                document.getElementById('dfsdafdsfdsf').dataset.url = data['next']
                document.getElementById('button_load_more').style = ''



                } else{
                    document.getElementById('button_load_more').innerHTML = ''
                }

            }

        })
    }

    load_all_posts()

    function load_more_posts(){

        var url = document.getElementById('dfsdafdsfdsf').dataset.url



        document.getElementById('jlfdsjflksdfjsdlf').style.display = 'block'

        load_all_posts(url)
    }
}
