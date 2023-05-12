/*  ---------------------------------------------------
    Template Name: Male Fashion
    Description: Male Fashion - ecommerce teplate
    Author: Colorib
    Author URI: https://www.colorib.com/
    Version: 1.0
    Created: Colorib
---------------------------------------------------------  */

'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");

        /*------------------
            Gallery filter
        --------------------*/
        $('.filter__controls li').on('click', function () {
            $('.filter__controls li').removeClass('active');
            $(this).addClass('active');
        });
        if ($('.product__filter').length > 0) {
            var containerEl = document.querySelector('.product__filter');
            var mixer = mixitup(containerEl);
        }
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    //Search Switch
    $('.search-switch').on('click', function () {
        $('.search-model').fadeIn(400);
    });

    $('.search-close-switch').on('click', function () {
        $('.search-model').fadeOut(400, function () {
            $('#search-input').val('');
        });
    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*------------------
        Accordin Active
    --------------------*/
    $('.collapse').on('shown.bs.collapse', function () {
        $(this).prev().addClass('active');
    });

    $('.collapse').on('hidden.bs.collapse', function () {
        $(this).prev().removeClass('active');
    });

    //Canvas Menu
    $(".canvas__open").on('click', function () {
        $(".offcanvas-menu-wrapper").addClass("active");
        $(".offcanvas-menu-overlay").addClass("active");
    });

    $(".offcanvas-menu-overlay").on('click', function () {
        $(".offcanvas-menu-wrapper").removeClass("active");
        $(".offcanvas-menu-overlay").removeClass("active");
    });

    /*-----------------------
        Hero Slider
    ------------------------*/
    $(".hero__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 1,
        dots: false,
        nav: true,
        navText: ["<span class='arrow_left'><span/>", "<span class='arrow_right'><span/>"],
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: false
    });

    /*--------------------------
        Select
    ----------------------------*/
    $("select").niceSelect();

    /*-------------------
		Radio Btn
	--------------------- */
    $(".product__color__select label, .shop__sidebar__size label, .product__details__option__size label").on('click', function () {
        $(".product__color__select label, .shop__sidebar__size label, .product__details__option__size label").removeClass('active');
        $(this).addClass('active');
    });

    /*-------------------
		Scroll
	--------------------- */
    $(".nice-scroll").niceScroll({
        cursorcolor: "#0d0d0d",
        cursorwidth: "5px",
        background: "#e5e5e5",
        cursorborder: "",
        autohidemode: true,
        horizrailenabled: false
    });

    /*------------------
        CountDown
    --------------------*/
    // For demo preview start
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    if(mm == 12) {
        mm = '01';
        yyyy = yyyy + 1;
    } else {
        mm = parseInt(mm) + 1;
        mm = String(mm).padStart(2, '0');
    }
    var timerdate = mm + '/' + dd + '/' + yyyy;
    // For demo preview end


    // Uncomment below and use your date //

    /* var timerdate = "2020/12/30" */

    $("#countdown").countdown(timerdate, function (event) {
        $(this).html(event.strftime("<div class='cd-item'><span>%D</span> <p>Days</p> </div>" + "<div class='cd-item'><span>%H</span> <p>Hours</p> </div>" + "<div class='cd-item'><span>%M</span> <p>Minutes</p> </div>" + "<div class='cd-item'><span>%S</span> <p>Seconds</p> </div>"));
    });

    /*------------------
		Magnific
	--------------------*/
    $('.video-popup').magnificPopup({
        type: 'iframe'
    });

    /*-------------------
		Quantity change
	--------------------- */
    var proQty = $('.pro-qty');
    proQty.prepend('<span class="fa fa-angle-up dec qtybtn"></span>');
    proQty.append('<span class="fa fa-angle-down inc qtybtn"></span>');
    proQty.on('click', '.qtybtn', function () {
        var $button = $(this);
        var oldValue = $button.parent().find('input').val();
        if ($button.hasClass('inc')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            // Don't allow decrementing below zero
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        $button.parent().find('input').val(newVal);
    });

    var proQty = $('.pro-qty-2');
    proQty.prepend('<span class="fa fa-angle-left dec qtybtn"></span>');
    proQty.append('<span class="fa fa-angle-right inc qtybtn"></span>');
    proQty.on('click', '.qtybtn', function () {
        var $button = $(this);
        var oldValue = $button.parent().find('input').val();
        if ($button.hasClass('inc')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            // Don't allow decrementing below zero
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        $button.parent().find('input').val(newVal);
    });

    /*------------------
        Achieve Counter
    --------------------*/
    $('.cn_num').each(function () {
        $(this).prop('Counter', 0).animate({
            Counter: $(this).text()
        }, {
            duration: 4000,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now));
            }
        });
    });
    //Add to Cart using ajax
    $(document).on('click',"#addToCartBtn",function() {
        var _vm = $(this);
        // var product_id = $(".prod_id").val();
        var product_id = $(".prod-id").attr('prod-id');
        var product_qty = $("#qty-input").val();

        //Ajax
        $.ajax({
            url: '/cart/add-to-cart',
            data:{
                'id':product_id,
                'qty' :product_qty, 
            },
            dataType:'json',
            beforeSend:function() {
                _vm.attr('disabled', true);
            },
            success:function(res){
                _vm.attr('disabled', false);  
                swal.fire("Congratulations !", res.status, "success").then((value) => {
                    window.location.reload()
                  });
            }

        });
        //end ajax

    });

    //End of add to cart
    // Delete item from cart
    $(document).on('click',".delete-item",function(){
        var _pId=$(this).attr('data-item');
        var _vm=$(this);
        //Ajax
        $.ajax({
            url: '/cart/delete-from-cart',
            data:{
                'id':_pId,
            },
            dataType:'json',
            beforeSend:function() {
                _vm.attr('disabled', true);
            },
            success:function(res){
                console.log(res);
                _vm.attr('disabled', false);           
            },
            success:function(res){
                $("#cartList").html(res.data);
                console.log(res.data)
            }

        });
        //end ajax
    });
    // end of delete item

    // update cart item
    $(document).on('click',".update-item",function(){
        var _pId=$(this).attr('data-item');
        var _pQty=$(".product-qty-"+_pId).val();
        var _vm=$(this); 
        console.log(_pQty)
        //Ajax
        $.ajax({
            url: '/cart/update-cart',
            data:{
                'id':_pId,
                'qty':_pQty
            },
            dataType:'json',
            beforeSend:function() {
                _vm.attr('disabled', true);
            },
            success:function(res){
                console.log(res);
                _vm.attr('disabled', false);           
            },
            success:function(res){
                swal.fire("Congratulations !", res.status, "success")  
                $("#cartList").html(res.data);
            }

        });
        //end ajax
    });// end of update cart

    //add to wishlist using ajax
    $(document).on('click',"#addtowishlist",function() {
        var _vm = $(this);
        var product_id = $(this).attr('prod-id');


        console.log(product_id+'prod id')


          

        // Ajax
        $.ajax({
            url: '/cart/wishlist/add-to-wishlist',
            data:{
                'id':product_id,
            },
            dataType:'json',
            beforeSend:function() {
                _vm.attr('disabled', true);
            },
            success:function(res){
                console.log(res.status)
                console.log(res);
                _vm.attr('disabled', false);
                if(res.message == 'Item added to wishlist'){
                swal.fire("Congratulations !", res.message, "success").then((value) => {
                    window.location.reload()
                  });
                }
                else{
                    Swal.fire(res.message)
                }
            }

        });
        // end ajax

    });

    // end of add to wishlist 

    // Delete item from wishlist
    $(document).on('click',".delete-wish",function(){
        var _pId=$(this).attr('data-item');
        var _vm=$(this);
        //Ajax
        console.log(_pId)
        $.ajax({
            url: '/cart/delete-from-wishlist',
            data:{
                'id':_pId,
            },
            dataType:'json',
            beforeSend:function() {
                _vm.attr('disabled', true);
            },
            success:function(res){
                console.log(res);
                _vm.attr('disabled', false);
                window.location.reload();         
            }

        });
        //end ajax
    });
    // end of delete item

})(jQuery);

setTimeout(function(){
    $('#message').fadeOut('slow')
}, 4000)

