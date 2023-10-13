function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(document).ready(function(){
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        data: { "product_id": 1} // Change this so its the correct product id
    });

    var clickId = 0;

    $(".addToCartBtn").click(function(){
        $.post("add_to_cart/", data={"product_id": 1})
        $(this).parent().hide()
        $(".changeQuantityForm").show()
    })

    // Increment quantity of item
    $(".incQuantity").click(function(){
        inQuantity = $(this).parent().siblings().children(".itemQuantity")
        inQuantity[0].stepUp()

        clickId += 1;
        var thisClickId = clickId

        // Sends post request 1 second after most recent inc/dec
        setTimeout(function() {
            if(thisClickId < clickId){  // Only click if this is the most recent click
                return
            }
            clickId = 0;
            $.post("change_item_quantity/", data={"quantity": inQuantity.val(), "product_id": inQuantity.closest(".cartItem").attr("id").split("_").pop()}, callback=(data) => displayBanner(data))
        }, 1000);
    })
    
    // Decrement quantity of item
    $(".decQuantity").click(function(){
        inQuantity = $(this).parent().siblings().children(".itemQuantity")
        inQuantity[0].stepDown()

        clickId += 1;
        var thisClickId = clickId
        setTimeout(function() {
            if(thisClickId < clickId){
                return
            }
            clickId = 0;
            $.post("change_item_quantity/", data={"quantity": inQuantity.val(), "product_id": inQuantity.closest(".cartItem").attr("id").split("_").pop()}, callback=(data) => displayBanner(data))
        }, 1000);
    })

    // Enter specific quantity of item
    $(".itemQuantity").change(function(){
        inQuantity = $(this)
        if(parseInt(inQuantity.val()) > parseInt(inQuantity.attr("max"))){
            inQuantity.val(inQuantity.attr("max"))
            return
        }

        if(parseInt(inQuantity.val()) < parseInt(inQuantity.attr("min"))){
            inQuantity.val(inQuantity.attr("min"))
            return
        }
        
        $.post("change_item_quantity/", data={"quantity": inQuantity.val(), "product_id": inQuantity.closest(".cartItem").attr("id").split("_").pop()}, callback=(data) => displayBanner(data))
    })
});