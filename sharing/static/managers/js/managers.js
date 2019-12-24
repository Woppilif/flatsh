$(function () {

  var reFresh = function () {
    var btn = $(this);      
    $.ajax({

      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      
      success: function (data) {
        if (data.form_is_valid) {
          $("#map-block").html(data.html_book_list);
          if(btn.attr('data-url') == '/projects/list/1')
          {
            btn.attr('value', 'Карта');
            btn.attr('data-url', '/projects/list/0');
          }
          else{
            btn.attr('value', 'Список');
            btn.attr('data-url', '/projects/list/1');
          }
          
        }
      }
    });
    return false;
  };

  var openDoor = function () {
    var btn = $(this);      
    $.ajax({

      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      
      success: function (data) {
        if (data.form_is_valid) {
          $("#rentCard").html(data.html_book_list);
        }
      }
    });
    return false;
  };

  var Buchen = function () {
    var btn = $(this);      
    $.ajax({

      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      
      success: function (data) {

        $("#flat-page").html(data.html_form);
        console.log(data);
        
      }
    });
    return false;
  };

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
        $("#modal-book .modal-content").html(data.html_form);
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
          $("#book-table tbody").html(data.html_book_list);
          $("#modal-book").modal("hide");
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
  $(".js-create-book").click(loadForm);
  $(".reFresh").click(reFresh);
  //$("#main").on("click", ".reFresh", reFresh);
  $("#main").on("click", ".reFresh", reFresh);

  $("#main").on("click", ".openDoor", openDoor);

  $("#main").on("click", ".Buchen", loadForm);

  // Update book
  $("#modal-book").on("submit", ".js-book-create-form", saveForm);

  // Update book
  $("#book-table").on("click", ".js-update-book", loadForm);
  $("#modal-book").on("submit", ".js-book-update-form", saveForm);

  // Delete book
  $("#book-table").on("click", ".js-delete-book", loadForm);
  $("#modal-book").on("submit", ".js-book-delete-form", saveForm);
});

function clickOnFlat(flat_id,ltype='map'){
  $.ajax({
    url: "/projects/flat/"+flat_id+"/"+ltype+"",
    type: 'get',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        $("#map-block").html(data.html_book_list);
      }
    }
  });
}