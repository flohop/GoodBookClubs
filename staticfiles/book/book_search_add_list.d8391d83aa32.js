$(window).on('load', function() {

var chosenBookIndex;
function bookSearch() {



    var search = document.getElementById('search').value;
    search.innerHTML = "";

    if(search.length > 0) {
    document.getElementById("loading-animation").classList.remove("remove");
    document.getElementById('results').innerHTML = "";

    var results = document.getElementById('results');
    var tableBody =  document.getElementById('results-table').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = "";
    items = null;

    $.ajax({
        url: "https://www.googleapis.com/books/v1/volumes?q=" + search,
        dataType: "json",

        success: function(data) {
             // make the loading animation visible by removing the "remove" class
            document.getElementById("loading-animation").classList.add("remove");
            items = data.items;
            $("#results-table").removeClass("remove");
            $("th .remove").removeClass("remove");
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
                clickButton.innerHTML = '<i class="far fa-check-circle"></i>';
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
    else {
        console.log("To short")
    }
}

function likeBook(e) {
    e.preventDefault()
    $.post(book_like_url,
        {
            id: $(this).data('id'),
            action: $(this).data('action')
        },
        function(data){
            if (data['status'] == 'ok')
                {
                    var bookId = data['id'];
                    var prevAction = data['prev_action']
                    var $clickedElement = $("[data-id=" + bookId + "]");
    
                    // toggle action
                    $clickedElement.data('action', prevAction == 'like' ?
                                        'unlike': 'like');
                    // toggle link text
                    if(prevAction == 'like') {
                        $($clickedElement.find("a.like").find("span.like-icon")).replaceWith('<span class="like-icon"><i class="fas fa-heart"></i></span>')
                    }
                    else {
                        $($clickedElement.find("a.like").find("span.like-icon")).replaceWith('<span class="like-icon"><i class="far fa-heart"></i></span>')
                    // update total likes
                    }
            
                    var prevLikes = parseInt($($clickedElement.prev().prev()).text());
                    $($clickedElement.prev().prev()).text(prevAction == 'like' ?
                    prevLikes + 1 : prevLikes - 1);
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
    data: { 'data': JSON.stringify(current_book_json),
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()

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
            var cover = data['cover'];

            // create container div element
            var containerDiv = document.createElement("DIV");
            containerDiv.classList.add("container");
            containerDiv.id = "container";
            
            // create book div
            var bookDiv = document.createElement("DIV");
            bookDiv.classList.add(title);


            // create li element
            var bookLi = document.createElement("LI");
            bookLi.id = "options";
            bookLi.classList.add("item");
            // TODO: bookLi.setAttribute("data-index")
            bookLi.setAttribute("data-id", id);
            


            // create img element
            var imgEl = document.createElement("img");
            imgEl.classList.add("book-cover");
            $(imgEl).attr("src", cover);

            // create inner ul
            var innerUlEl = document.createElement("ul");
            innerUlEl.classList.add("inner-ul");

            // create inner li elements and append them to inner ul
            var inLi1 = document.createElement("li");
            inLi1.classList.add("inner-li");
            var inAEl = document.createElement("a");
            inAEl.classList.add("book-title");
            inAEl.setAttribute("href", url);
            inAEl.innerText = title;
            inLi1.append(inAEl);

            var inLi2 = document.createElement("li");
            inLi2.classList.add("inner-li");
            var inSpanEl2 = document.createElement("span");
            inSpanEl2.classList.add("author");
            inSpanEl2.innerText = author;
            inLi2.append(inSpanEl2);

            var inLi3 = document.createElement("li");
            inLi3.classList.add("inner-li");

            var countSpanEl = document.createElement("span");
            countSpanEl.classList.add("count");

            var totalSpanEl = document.createElement("span");
            totalSpanEl.classList.add("total");
            totalSpanEl.innerText = "0";

            var canNotLikeSpanEl = document.createElement("span");
            canNotLikeSpanEl.classList.add("can-not-like");

            var heartIEl = document.createElement("i");
            heartIEl.classList.add("far");
            heartIEl.classList.add("fa-heart");

            canNotLikeSpanEl.appendChild(heartIEl);
            countSpanEl.appendChild(canNotLikeSpanEl);

            var likeAEl = document.createElement("a");
            likeAEl.classList.add("like");
            likeAEl.classList.add("button");
            likeAEl.classList.add("remove");
            likeAEl.setAttribute("href", "#");
            likeAEl.setAttribute("data-id", id);
            likeAEl.setAttribute("data-action", "like");

            // register event listener
            likeAEl.addEventListener("click", likeBook, false);

            var likeSpanEl = document.createElement("span");
            likeSpanEl.classList.add("like-icon");

            var heartIEl2 = document.createElement("i");
            heartIEl2.classList.add("far");
            heartIEl2.classList.add("fa-heart");

            likeSpanEl.appendChild(heartIEl2);
            likeAEl.appendChild(likeSpanEl)
            
            // put it all together
            countSpanEl.appendChild(totalSpanEl);
            countSpanEl.appendChild(canNotLikeSpanEl);
            countSpanEl.appendChild(likeAEl);
            inLi3.appendChild(countSpanEl);

            var inLi4 = document.createElement("li");
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

            // append select to li
            inLi4.append(selectEl);

            // append inner-li to inner-ul
            innerUlEl.append(inLi1);
            innerUlEl.append(inLi2);
            innerUlEl.append(inLi3);
            innerUlEl.append(inLi4);

            // append img to li
            bookLi.append(imgEl)

            // append ul to li
            bookLi.append(innerUlEl);

            // append li to bookDiv
            bookDiv.append(bookLi);

             // append to container div
             containerDiv.append(bookDiv);

            document.getElementById("book-list").appendChild(containerDiv);
            $("#added-books").removeClass("remove");
            document.getElementById("book-added-info").classList.remove("remove");
            // add like event listener
            // TODO: make the like click function a named function, register the newly created <a> element to it, so that newly
            // created elements can get liked. Make the dashboard pretty and remove value from search field after user selects book
            
            // when form changes, update value in database



        }
        else if(data['status'] == 'already_exists') {
                console.log("Book already exists");
        }
       }
    });
    }




document.getElementById("button").addEventListener("click", bookSearch, false);
});