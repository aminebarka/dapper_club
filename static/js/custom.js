$(document).ready(function(){

    // Product Variation
	$(".choose-size").hide();
	$(".out-of-stock").hide();

	// Show size according to selected color
	$(".choose-color").on('click',function(){
		$(".choose-size").removeClass('active');
		$(".choose-size").removeClass('prod-id');
		$(".choose-color").removeClass('color-title');


		// $(".choose-color").removeClass('focused');
		// $(this).addClass('focused');

		var _color=$(this).attr('data-color');
		var _color_name=$(this).attr('color');

		// var _size=$('.choose-size').attr('data-size');
		console.log(_color+" color")
		console.log(_color_name+" cn")

		$(".choose-size").hide();
		$(".color"+_color).show();
		$(".color-"+_color).addClass('color-title');

		// $(".color"+_color).first().addClass('active');

		

	});
	// End

	// get product id
	$(".choose-size").on('click',function(){

		var _pId=$(this).attr('prod-id');
		var stock=$('.stock-'+_pId).attr('stock'); 
        var product_qty = $("#qty-input").val();
		

		if(stock<=0){

			$(".addtocart").hide();
			$(".out-of-stock").show();

			console.log("out of stock")
		}
		
		else{
		console.log("in stock")
		$(".addtocart").show();
		$(".out-of-stock").hide();
		}

		if(stock<product_qty){

			$(".addtocart").hide();
			$(".out-of-stock").show();

			console.log("out of stock")
		}
		
		else{
		console.log("in stock")
		$(".addtocart").show();
		$(".out-of-stock").hide();
		}


		$(".choose-size").removeClass('active');
		$(".choose-size").removeClass('prod-id');

		$(".size"+_pId).addClass('active');
		$(".size"+_pId).addClass('prod-id');

		console.log(_pId+'prod-id')
		console.log(stock+' stock')
		console.log(product_qty)


		// $(".choose-size").hide();
		// $(".color"+_color).show();
		// $(".color"+_color).first().addClass('active');

		

 	});
	//end
    // Show the first selected color
	$(".choose-color").first().addClass('focused');
	var _color=$(".choose-color").first().attr('data-color');
	var _price=$(".choose-size").first().attr('data-price');

	$(".color"+_color).show();
	// $(".color"+_color).first().addClass('active');
	// $(".product-price").text(_price);

	// apply coupon
	$(document).on('click',"#apply_coupon",function() {
        var coupon_code = $("[name='coupon_code']").val();
		var order_number = $('.order_number').attr('order_number');
		console.log(coupon_code, order_number)

        // Ajax
        $.ajax({
            url: '/cart/apply-coupon',
            data:{
                'coupon_code':coupon_code,
				'order_number':order_number
            },
            dataType:'json',
            success:function(res){
				if(res.msg=='Coupon applied successfully'){
					swal.fire("Congratulations !", res.msg, "success")
                	$("#Payment").html(res.data);

				}
				else{
					Swal.fire({
						icon: 'error',
						title: 'Sorry',
						text: res.msg,
					  })
				}
				
            }

        }); 
        //end ajax

    });



});