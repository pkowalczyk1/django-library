$( document ).ready(function() {
    let display = false
    $(".like-form").submit(function(e){
        e.preventDefault()
        
        const song_id = $(this).attr('id')
        const like_text = $(`.like-text${song_id}`).text()
        const trim = $.trim(like_text)
        const url = $(this).attr('action')
        const path = $(`.path`).attr('value')
        
        let res;
        const likes = $(`.like-count${song_id}`).text()
        const trim_count = parseInt(likes)
        const me = $(this)

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'song_id': song_id,
                'path': path,
            },
            success: function(response) {
                if (trim === 'Nie lubię') {
                    $(`.like-text${song_id}`).text(' Lubię to!')
                    res = trim_count - 1
                    me.find('i').removeClass('fa-thumbs-down')
                    me.find('i').addClass('fa-thumbs-up')
                }
                else {
                    $(`.like-text${song_id}`).text(' Nie lubię')
                    res = trim_count + 1
                    me.find('i').removeClass('fa-thumbs-up')
                    me.find('i').addClass('fa-thumbs-down')
                }

                $(`.like-count${song_id}`).text(res)
            },
            error: function(response) {
                console.log('error', response)
            }
        })
    })
});