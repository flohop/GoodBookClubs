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

    success: function(data) {
        // add new book to list
        if(data['status'] == 'new_book'){
            // add new book to top of the list
            console.log("Success, added book to library")


            // extract data from response
            var title = data['title'];
            var id = data['id'];
            var author = data['author'];
            var url = data['url'];
            var likes = 0;

            // create li element
            var bookLi = document.createElement("LI")

            var bookLinkEl = document.createElement("a");
            bookLinkEl.href = url;
            bookLinkEl.innerHTML = title;
            bookLi.innerHTML = " | " + author + " | ";
            bookLi.setAttribute('data', 'id: ' + id)

            bookLi.insertBefore(bookLinkEl, bookLi.childNodes[0]);

            var countEl = document.createElement("SPAN");
            countEl.classList.add("count");

            var innerCounterEl = document.createElement("SPAN");
            innerCounterEl.classList.add("total")
            innerCounterEl.innerHTML = "0 ";

            countEl.appendChild(innerCounterEl);
            countEl.appendChild(document.createTextNode("likes "));

            // create the link to like
            var likeLinkEl = document.createElement("a");
            likeLinkEl.href = "#"
            $(likeLinkEl).data('action', 'like');
            $(likeLinkEl).data('id', id);
            likeLinkEl.classList.add("like");
            likeLinkEl.classList.add("button");
            likeLinkEl.innerHTML = "Like";

            // append all elements
            bookLi.appendChild(countEl);
            bookLi.appendChild(likeLinkEl);

            // append new <li> to <ul>
            document.getElementById("book-list").appendChild(bookLi);
            
            // add like event listener
            // TODO: make the like click function a named function, register the newly created <a> element to it, so that newly
            // created elements can get liked. Make the dashboard pretty and remove value from search field after user selects book
            likeLinkEl.addEventListener("click",)
        }
        else if(data['status'] == 'already_exists') {
                console.log("Book already exists");
        }
       }
    });
    }


document.getElementById("button").addEventListener("click", bookSearch, false);
});