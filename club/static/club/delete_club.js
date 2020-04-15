function deleteBook() {
    var clubId = $('#delete').attr("data-id");

    // ajax call to view, that deletes the club
    $("#form-content").addClass("remove");
    $('#return').removeClass("remove");
    $.ajax('delete/',{},
        function(data){
        if(data['status'] == 'ok'){
            console.log("Deleted club instance");
            }
        else {
            console.log("Something went wrong");
        }
        }
    )
}

document.getElementById("delete").addEventListener("click", deleteBook, false);