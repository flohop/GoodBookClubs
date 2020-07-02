function bookSearch() {

    console.log("Hello world");
    var search = document.getElementById('search').value;
    document.getElementById('results').innerHTML = "";
    var results = document.getElementById('results');
    var tableBody =  document.getElementById('results-table').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = "";
    items = null;

    $.ajax({
        url: "https://www.googleapis.com/books/v1/volumes?q=" + search,
        dataType: "json",

        success: function(data) {
            items = data.items;
            for(i=0; i< data.items.length; i++) {
                var newRow = tableBody.insertRow();
                newRow.className = "data-row"

                var newCell = newRow.insertCell(0);
                try {
                    var newText = document.createTextNode(data.items[i].volumeInfo.title);
                }
                catch(TypeError) {
                    newCell.className = document.createTextNode(" ");
                }
                newCell.appendChild(newText);

                var newCell = newRow.insertCell();
                newCell.className = "author";
                try{
                    var newText = document.createTextNode(data.items[i].volumeInfo.authors[0]);
                }
                catch(TypeError) {
                    var newText = document.createTextNode("author not found");
                }
                newCell.appendChild(newText);

                // create button which to click
                var clickButton = document.createElement("BUTTON");
                clickButton.innerText = "Select";
                clickButton.type = "button";
                clickButton.onclick = "#";

                var newCell = newRow.insertCell();
                newCell.className = "select-book"
                newCell.appendChild(clickButton);
            }
            $(document.getElementById("results-table")).on('click', "tr", onRowClicked);
            $('tr.data-row').show();
    }
    });
}

function onRowClicked(e) {
    console.log($(e.currentTarget.parentNode));
    rowItemIndex = $(e.currentTarget).index();

    // detach event listener from rows
    $(document.getElementById("results-table")).off("click", "tr", onRowClicked);

    // assign value to global variable
    chosenBookIndex = rowItemIndex;

    // hide all rows except the one clicked and hide the select button
    $('tr.data-row').hide();
    $(this).attr("style", "display: show;");
    $('.select-book').hide();
}



function submitChangeForm(e) {
    // get all the group infos and the book infos, send them to a view, create the book and the club there
    // and then redirect the user to his newly created club

    if(document.getElementById("club-form").reportValidity()){
        // get all the data from the form
        var groupName = document.forms['club-form']['group_name'].value;
        var groupDescription = document.forms['club-form']['group_description'].value;

        try {
            var current_book_json = items[chosenBookIndex];
            console.log("Current book: " + current_book_json);
        }
        catch(e){
            console.log("Error:" + e)
            var current_book_json = "None";
        }


        // save all values in a json object which will be send to the view via ajax
        debugger;
        var allData = {"name": groupName,
                        'description': groupDescription,
                        'book': current_book_json,

                    }

        // setup ajax with CSRF
        var csrftoken = Cookies.get('csrftoken');
        function csrfSafeMethod(method) {
          // these HTTP methods do not require CSRF protection
          return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
          beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
          }
        });


        // send the data with ajax to the view
        $.ajax({
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        url: 'response/',
        data: JSON.stringify(allData),

        success: function(data) {
            if(data['status'] == 'ok')
            {
                // redirect user to new group
                window.location.replace(data.url);
            }
            else
            {
                console.log("Something went wrong")
            }

        }
        });

    }
}
document.getElementById("button").addEventListener("click", bookSearch, false);
document.getElementById("submit-change").addEventListener("click", submitChangeForm, false);