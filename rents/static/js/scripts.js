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