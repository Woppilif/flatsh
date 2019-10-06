$(function () {

    /* Functions */  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-book .modal-content").html("");
          $("#modal-book").modal("show");
        },
        success: function (data) {
          $("#modal-book .modal-content").html(data.html_book_list);
          //$("#flat-info").html(data.html_book_list);
        }
      });
    };
  
    var saveForm = function () {
      var form = $(this);
      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            $("#modal-book").modal("hide");
            $("#flat-info").html(data.html_book_list);
          }
          else {
            $("#modal-book .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };
  
  
    /* Binding */
  
    // Create book
    $(".flats-filter").click(loadForm);
  
    //setInterval(updateForm,10000);
    $("#modal-book").on("submit", ".js-book-create-form", saveForm);
  
    // Update book
    $("#book-table").on("click", ".js-update-book", loadForm);
    $("#modal-book").on("submit", ".js-book-update-form", saveForm);
  
    // Delete book
    $("#book-table").on("click", ".js-delete-book", loadForm);
    $("#modal-book").on("submit", ".js-book-delete-form", saveForm);
  
  });
  
  
  function clickOnFlat(flat_id){
    $.ajax({
      url: "/flat/"+flat_id+"",
      type: 'get',
      dataType: 'json',
      success: function (data) {
        $("#flat-info").html(data.html_book_list);
      }
    });
    var element = document.getElementById("flat-info");

    element.scrollIntoView({behavior: "smooth",  inline: "nearest"});
  }

  function rentStart(flat_id){
    $.ajax({
      url: "/flat/"+flat_id+"/start",
      type: 'get',
      dataType: 'json',
      success: function (data) {
        $("#flat-info").html(data.html_book_list);
      }
    });
  }