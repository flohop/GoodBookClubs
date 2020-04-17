// need: <span class="total likes">
// need: <a href="#" data-id="{{ book.id }}" data-action="{% if user_liked_book %}un{% endif %}like"
//          class="like toggle button">
// need: <script>var like_toggle_url = "{% url 'book:like' %}"</script>
function likeBook(e)
{
    console.log("Wanting to like book");
    e.preventDefault();

    $.post(like_toggle_url,
        {
            id: $(this).data('id'),
            action: $(this).data('action')
        },
        function(data){
            if (data['status'] == 'ok'){

                var previousAction = $('a.like').data('action');

                // toggle data-action
                $('a.like').data('action', previousAction == 'like' ?
                'unlike': 'like');
                // toggle link text
                $('a.like').text(previousAction == 'like' ? 'Unlike':
                'Like');

                // update total_likes
                var previousLikes = parseInt($('span.likes.total').text());

                $('span.likes.total').text(previousAction == 'like' ?
                previousLikes + 1 : previousLikes - 1);
            }
        }
        );
    }
console.log("Loaded like script");
$('a.toggle').on("click", likeBook);