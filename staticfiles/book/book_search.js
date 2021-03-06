$(window).on('load', function() { 

var chosenBookIndex;
var items;
function bookSearch() {

    // make the loading animation visible by removing the "invisible" class
    document.getElementById("loading-animation").classList.remove("invisible-animation");

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

            // if successful, remove the loading animation, by adding the "invisible" class to it
            document.getElementById("loading-animation").classList.add("invisible-animation");

            items = data.items;
            count = 10
            if (10 >= data.items.length) {
                count = data.items.length
            }

            for(i=0; i<count; i++) {
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
                clickButton.innerHTML = '<i class="far fa-check-circle"></i>';
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

function submitForm(e) {
    // get all the group infos and the book infos, send them to a view, create the book and the club there
    // and then redirect the user to his newly created club
    e.preventDefault();
    console.log("Trying to submit group form")

    if(validateForm()){
        // get all the data from the form
        var groupName = document.forms['club-form']['group_name'].value;
        var groupDescription = document.forms['club-form']['group_description'].value;
        var groupImage = document.forms['club-form']['group_image'].value;
        var groupType = document.forms['club-form']['group_type'].value;
        try {
            var current_book_json = items[chosenBookIndex];
        }
        catch(e){
            var current_book_json = "None";
        }


        // save all values in a json object which will be send to the view via ajax

       var allData = {"name": groupName,
                        'description': groupDescription,
                        'image': groupImage,
                        'type': groupType,
                        'book': current_book_json
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
            console.log("Success, created new book and new group");
            window.location.replace(data.url);

            // redirect user to new group
        }
        });

    }
}

function validateForm() {
    debugger;
    var name = document.forms['club-form']['group_name'].value;
    var description = document.forms['club-form']['group_description'].value;
    var type = document.forms['club-form']['group_type'].value;

    try {
        debugger;
        var current_book_json = items[chosenBookIndex];
        }
    catch(err) {
        if(type == 'reading_club') {
            alert("Please pick a book");
            return false;
        }
        else {
            return true;
        }
    }

    if(name == "") {
        alert("Please enter a name");
        return false;
    }
    if (description == "") {
        alert("Please enter a description");
        return false;
    }
    if (current_book_json == "" && type == "reading_club"){
        alert("Please select a book");
        return false;
    }
    return true;
}

function prepareUpload(e) {
    files = event.target.files
}

$('input[type=file]').on('change', prepareUpload);
document.getElementById("button").addEventListener("click", bookSearch, false);
document.getElementById("club-form").addEventListener("submit", submitForm, false);
});