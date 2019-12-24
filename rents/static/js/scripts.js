$( function() {
    $( "#slider-range" ).slider({
      step: 10,
      range: true,
      min: 100,
      max: 6000,
      values: [ 700, 4000 ],
      slide: function( event, ui ) {
        $( "#amount" ).val( " " + ui.values[ 0 ] + " - " + ui.values[ 1 ] + " руб/сут" );
      }
    });
    $( "#amount" ).val(  $( "#slider-range" ).slider( "values", 0 ) +
      " - " + $( "#slider-range" ).slider( "values", 1 ) + " руб/сут");
  } );




/*Pop-up*/

$('.js-button-compaign').click(function() {
  $('.js-overlay-compaign').fadeIn();
});

$(document).mouseup(function (e) {
  var popup = $('.js-popup-compaign');
  if (e.target != popup[0] && popup.has(e.target).length === 0) {
    $('.js-overlay-compaign').fadeOut();
    $('.navigation').fadeIn();
  }
})