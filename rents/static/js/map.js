


    
   
setInterval(function() {
var minprice = $(".pc-filter .irs-from").text();
var maxprice = $(".pc-filter .irs-to").text();
var minpricep = $(".pc-filter .irs-from").text();
var maxpricep = $(".pc-filter .irs-to").text();
var minpricemob = $(".mob-filter_mon .irs-from").text();
var maxpricemob = $(".mob-filter_mon .irs-to").text();
var minpricepmob = $(".mob-filter_mon .irs-from").text();
var maxpricepmob = $(".mob-filter_mon .irs-to").text();
$("#min-price").val(minprice);
$("#max-price").val(maxprice);
$("#min-price-p").text(minpricep);
$("#max-price-p").text(maxpricep);
$("#min-price-mob").val(minpricemob);
$("#max-price-mob").val(maxpricemob);
$("#min-price-p-mob").text(minpricepmob);
$("#max-price-p-mob").text(maxpricepmob);
}, 500);
// Filter ul
$(".variation-filter-ul button").click(function(e) {
    e.preventDefault();
    $(".variation-filter-ul button").removeClass('active');
    $(this).addClass('active');
  })
//   Список
$('.block7 .button-blue').click(function() {
    $('.ul-home').toggleClass('open-ul-hove close-ul-hove');
    $('.map-main').toggleClass('open-ul-hove close-map');
    // $('.ul-home').toggleClass('open-ul-hove close-ul-hove2');
});
// доп фильтр
$('.block8 button').click(function() {
    $('.level3').toggleClass('level3-open level3-close');
    $('.level1').toggleClass('level3-open close-map');
});
// hata
$('.cart-home_item').click(function() {
    $('.hata-filter').toggleClass('open-hata close-hata');
    $('.hata-cart').toggleClass('open-hata close-hata');
    $('.filter-main-full').toggleClass('open-filter-main-full close-filter-main-full');
    $('.ul-home').toggleClass('open-ul-hove close-ul-hove2');
    $('.map-main').toggleClass('open-ul-hove close-map');
    $('.level3').toggleClass('level3-open level3-close');
});
// Назад к карте
$('.rest-catt').click(function() {
    $('.hata-filter').toggleClass('open-hata close-hata');
    $('.hata-cart').toggleClass('open-hata close-hata');
    $('.filter-main-full').toggleClass('open-filter-main-full close-filter-main-full');
    $('.ul-home').toggleClass('open-ul-hove close-ul-hove2');
    $('.ul-home').toggleClass('open-ul-hove close-ul-hove');
    $('.map-main').toggleClass('open-ul-hove close-map');
    $('.level3').toggleClass('level3-open level3-close');
    $('.map-main').toggleClass('open-ul-hove close-map');
});
// Модал окно
$('.broker').click(function() {
    $('.modal-okay').toggleClass('modal-open modal-close');
});
$('.modal-contant .button-blue').click(function() {
    $('.modal-okay').toggleClass('modal-open modal-close');
});
// Радиус
$('.radius-prev').click(function() {
    $('.background-form-filter').toggleClass('radius-open radius-close');
});
var radius;
$('.content-radius-full p').on('click', function (event) {
	radius = $(this).text();
    $(".radius-prev-value span").text(radius);
})
// Gostey
$('.gostey-prev').click(function() {
    $('.background-form-gostey').toggleClass('radius-open radius-close');
});
var gostey;
$('.content-gostey-full p').on('click', function (event) {
	gostey = $(this).text();
    $(".gostey-prev-value span").text(gostey);
})
// Район
$('.raion-prev').click(function() {
    $('.background-form-raion').toggleClass('radius-open radius-close');
});
var raion;
$('.content-raion-full p').on('click', function (event) {
	raion = $(this).text();
    $(".raion-prev-value span").text(raion);
})
// Количество комнат
$(document).ready(function() {
    $('.inputminus').click(function () {
        var $input = $(this).parent().find('.inputresult');
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.inputplus').click(function () {
        var $input = $(this).parent().find('.inputresult');
        $input.val(parseInt($input.val()) + 1);
        $input.change();
        return false;
    });
});
$(document).ready(function(){
	$('.inputresult').change(function(){
		if (+$(this).attr('max') < $(this).val()) {
			$(this).val($(this).attr('max'));
		}
	});
});
// Время у даты
$('.xdsoft_timepicker .xdsoft_prev').after('<h5 class="name-callendary-time">Время выезда</h5>');
$('.xdsoft_timepicker .name-callendary-time').after('<h6 class="name-callendary-time2">Квартира свободна</h6>');
$('.xdsoft_time_box.xdsoft_scroller_box').prepend('<div id="radius-top"></div>');
$('.xdsoft_time_box.xdsoft_scroller_box').append('<div id="radius-bottom"></div>');
$('.xdsoft_time_box.xdsoft_scroller_box').append('<div class="radius-form-filter_content-button2"><button class="bottom-button"><img src="img/bottom.png" alt=""></button><button class="top-button"><img src="img/top.png" alt=""></button></div>');
// скрол
$(".bottom-button").click(function(){
	$(".content-gostey-full").animate({
    	scrollTop: $('.content-gostey-full').scrollTop() + 48
	}, 0);
});
$(".top-button").click(function(){
	$(".content-gostey-full").animate({
    	scrollTop: $('.content-gostey-full').scrollTop() - 48
	}, 0);
});

$(".bottom-button").click(function(){
	$(".content-radius-full").animate({
    	scrollTop: $('.content-radius-full').scrollTop() + 48
	}, 0);
});
$(".top-button").click(function(){
	$(".content-radius-full").animate({
    	scrollTop: $('.content-radius-full').scrollTop() - 48
	}, 0);
});

$(".bottom-button").click(function(){
	$(".content-raion-full").animate({
    	scrollTop: $('.content-raion-full').scrollTop() + 48
	}, 0);
});
$(".top-button").click(function(){
	$(".content-raion-full").animate({
    	scrollTop: $('.content-raion-full').scrollTop() - 48
	}, 0);
});

$(".bottom-button").click(function(){
	$(".xdsoft_time_variant").animate({
    	scrollTop: $('.xdsoft_time_variant').scrollTop() + 48
	}, 0);
});
$(".top-button").click(function(){
	$(".xdsoft_time_variant").animate({
    	scrollTop: $('.xdsoft_time_variant').scrollTop() - 48
	}, 0);
});  

// Дополнительные фильтры

$('.dop_filt').click(function(){
    if ($('.filters').hasClass('dis_no')) {
        $('.filters').removeClass('dis_no');
        $('.settings').addClass('dis_no');
        $('.btns').removeClass('btns-mar');
        $('.dop_filt').text("Вернуться к основным");

    } else {
        $('.filters').addClass('dis_no');
        $('.settings').removeClass('dis_no');
        $('.btns').addClass('btns-mar');
        $('.dop_filt').text("Дополнительные фильтры");
    }
});