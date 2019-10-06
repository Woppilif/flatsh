$(function () {

  /* Functions */

  var updateForm = function () {
    var btn = $(this);      
    $.ajax({

      url: '/projects/refresh',
      type: 'get',
      dataType: 'json',
      
      success: function (data) {
        $("#book-table tbody").html(data.html_book_list);
      }
    });
  };

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
  $(".refresh").click(updateForm);

  //setInterval(updateForm,10000);
  $("#modal-book").on("submit", ".js-book-create-form", saveForm);

  // Update book
  $("#book-table").on("click", ".js-update-book", loadForm);
  $("#modal-book").on("submit", ".js-book-update-form", saveForm);

  // Delete book
  $("#book-table").on("click", ".js-delete-book", loadForm);
  $("#modal-book").on("submit", ".js-book-delete-form", saveForm);


  DG.then(function() {
    $.ajax({
      url: "/flats/",
      type: 'get',
      dataType: 'json',
      success: function (data) {
        console.log(data);
      }
    });

    var map,markers = DG.featureGroup();
    map = DG.map('map', {
        center: [55.797602, 49.099868],
        zoom: 13,
        fullscreenControl: false,
        zoomControl: false
    });
    

    map.locate({setView: true, watch: false})
        .on('locationfound', function(e) {
            DG.marker([e.latitude, e.longitude]).addTo(map);
        })
        .on('locationerror', function(e) {
            DG.popup()
              .setLatLng(map.getCenter())
              .setContent('Доступ к определению местоположения отключён')
              .openOn(map);
        });
    
    
    DG.control.location({position: 'bottomright'}).addTo(map);
  });
});


