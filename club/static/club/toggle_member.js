// need: <a class="toggle" data-id="club-id" data-action="join/leave" data-group_type="reading/discussion"></a>
// need: <span class="count"></span>
// need: <script>var toggle_view_url = {% url 'club:toggle' %}</script> before this script is loaded

function joinClub(e) {

    target = e.target; // the <a> element
    e.preventDefault();

    $.post(toggle_view_url, 
        {
            id:  $(this).data("id"),
            action: $(this).data("action"),
            group_type: $(this).data("group_type")
        },
        function(data) {
            if(data['status'] == 'ok') 
            {   
                var previousAction = $('a.join-toggle').data("action");

                // toggle data-action
                $('a.join-toggle').data('action', previousAction == 'join' ?
                'leave': 'join');
                // toggle link text
                $('a.join-toggle').text(previousAction == 'join' ?
                 "Leave": "Join");

                 // update total_members
                 var previousMembers = parseInt($('span.count-members').text());
                 $('span.count-members').text(previousAction == 'join' ? previousMembers + 1: previousMembers -1);

            }
        }
        )
}


console.log("loaded member toggle script");
$('a.join-toggle').on("click", joinClub);