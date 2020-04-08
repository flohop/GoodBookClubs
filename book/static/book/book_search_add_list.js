$(window).on('load', function() {

var chosenBookIndex;
function bookSearch() {

    var search = document.getElementById('search').value;
    search.innerHTML = "";
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
            $(document.getElementById("results-table")).removeClass("hide");
            $(document.getElementById("results-table")).on('click', "tr", onRowClicked);
            $('tr.data-row').show();
    }
    });
}

function sendValuesToServer(e) {
    // send the changed value for the list to the server
    target = e.target;
    if($(target).hasClass("book-status")){
        value = target.value;
        id = $(target).parent().data("id");
        console.log("Send data with id: " + id + " value: " + value)

        $.post(book_change_status_url,
        {
                id : id,
                value: value
        },
        function(data){
        if (data['status'] == 'OK')
            {
            if(data['can_like'] == "True") {
                var bookId = data['id'];
                $('li').find("[data-id='" + bookId + "']").removeClass("hide")
            }
            else {
                var bookId = data['id'];
                $('li').find("[data-id='" + bookId + "']").addClass("hide")
            }
            }
        }
    );
    }
}

function likeBook(e, myId, myAction) {
    $.post(book_like_url,
        {
            id: myId,
            action: myAction
        },
        function(data) {
            if(data['status'] == 'ok'){

                // TODO: find correct Link to Like, so it can change depending on the action
                // TODO: atm, i can't get it to work, user can't add new book and like it instantly,
                // TODO: he has to reload the page to make it work, FIX LATER!

                var bookId = data['id'];
                var prevAction = data['prev_action'];
                console.log("Likes to added books will be implemented later");
            }
        }
    );
}

function onRowClicked(e) {

    rowItemIndex = $(e.currentTarget).index();

    // detach event listener from rows
    $(document.getElementById("results-table")).off("click", "tr", onRowClicked);

    // assign value to global variable
    chosenBookIndex = rowItemIndex;

    // get the current book
    var current_book_json = items[chosenBookIndex];
    // hide all rows hide the select button, add the chosen item to the database and add it to the list
    $('#results-table').addClass("remove");

    $.ajax({
    type: 'POST',
    dataType: 'json',
    contentType: 'application/json;charset=utf-8',
    url: 'add-book/',
    data: JSON.stringify(current_book_json),

    // create the new row, append it to the list and add event listeners
    success: function(data) {
        // add new book to list
        if(data['status'] == 'new_book'){
            // add new book to top of the list
            console.log("Success, added book to library");


            // extract data from response
            var title = data['title'];
            var id = data['id'];
            var author = data['author'];
            var url = data['url'];

            // create div element
            var bookDiv = document.createElement("DIV");

            // create li element
            var bookLi = document.createElement("LI");

            var bookLinkEl = document.createElement("a");
            bookLinkEl.href = url;
            bookLinkEl.innerHTML = title;
            bookLi.innerHTML = " | " + author + " | ";
            bookLi.setAttribute('data-id', id);

            bookLi.insertBefore(bookLinkEl, bookLi.childNodes[0]);

            var countEl = document.createElement("SPAN");
            countEl.classList.add("count");

            var innerCounterEl = document.createElement("SPAN");
            innerCounterEl.classList.add("total");
            innerCounterEl.innerHTML = "0 ";

            countEl.appendChild(innerCounterEl);
            countEl.appendChild(document.createTextNode("likes "));

            // create the link to like
            likeLinkEl = document.createElement("a");
            likeLinkEl.href = "#";
            likeLinkEl.id = "like-link-id";
            var action = "like"
            likeLinkEl.setAttribute("data-action", action);
            likeLinkEl.setAttribute("data-id", id);
            likeLinkEl.classList.add("like");
            likeLinkEl.classList.add("button");
            likeLinkEl.classList.add("hide"); // hide like option for as long as user isnt reading the book
            likeLinkEl.innerHTML = "Like";

            likeLinkEl.addEventListener("click", function(e) {
                    likeBook(e, id, action);
            }, false);

            // create the select element
            var selectEl = document.createElement("SELECT");
            selectEl.id = "book-status";
            selectEl.classList.add("book-status");

            // create the options
            var optEl1 = document.createElement("OPTION");
            optEl1.value = "reading";
            optEl1.classList.add("status");
            optEl1.innerHTML = "Currently reading";

            var optEl2 = document.createElement("OPTION");
            optEl2.value = "read";
            optEl2.classList.add("status");
            optEl2.innerHTML = "Read";

            var optEl3 = document.createElement("OPTION");
            optEl3.value = "want-to-read";
            optEl3.classList.add("status");
            optEl3.innerHTML = "Want to read";

            var optEl4 = document.createElement("OPTION");
            optEl4.value = "blank";
            optEl4.classList.add("status");
            optEl4.innerHTML = "";
            optEl4.setAttribute("selected", "selected");

            // append <option>'s to <select>
            selectEl.appendChild(optEl1);
            selectEl.appendChild(optEl2);
            selectEl.appendChild(optEl3);
            selectEl.appendChild(optEl4);

            // append all elements
            bookLi.appendChild(countEl);
            bookLi.appendChild(likeLinkEl);
            bookLi.appendChild(selectEl);
            bookDiv.appendChild(bookLi);

            // append new <div> to <ul>
            document.getElementById("book-list").appendChild(bookDiv);
            
            // add like event listener
            // TODO: make the like click function a named function, register the newly created <a> element to it, so that newly
            // created elements can get liked. Make the dashboard pretty and remove value from search field after user selects book
            
            // when form changes, update value in database
            document.getElementById("book-list").addEventListener("change", sendValuesToServer, false);



        }
        else if(data['status'] == 'already_exists') {
                console.log("Book already exists");
        }
       }
    });
    }




document.getElementById("button").addEventListener("click", bookSearch, false);
});