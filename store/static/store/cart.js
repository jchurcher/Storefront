// function calc_total_price(quantity, price) {
//     return quantity * price
// }

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

function calculate_total_price(itemId) {
    console.log(cartJS);

    formElement = document.getElementById("quantity_"+itemId);
    formElement.parentElement.submit();

    var newQuantity = formElement.value;
    console.log(newQuantity);

    var total = 0;
    for(item in cartJS) {
        if(item == itemId) {
            total += cartJS[item].price * newQuantity;
            continue;
        }

        total += cartJS[item].price * cartJS[item].quantity;
        console.log(cartJS[item].price)
    }

    total = total.toFixed(2);

    var t = document.getElementById("totalPrice");
    t.innerHTML = "Total: £"+total;

    console.log(total);
}

$(document).ready(function(){
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    var clickId = 0;

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
            $.post("change_item_quantity/", data={"quantity": inQuantity.val(), "product_id": inQuantity.closest(".cartItem").attr("id").split("_").pop()})
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
            $.post("change_item_quantity/", data={"quantity": inQuantity.val(), "product_id": inQuantity.closest(".cartItem").attr("id").split("_").pop()})
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
        
        $.post("change_item_quantity/", data={"quantity": inQuantity.val(), "product_id": inQuantity.closest(".cartItem").attr("id").split("_").pop()})
    })

    $(".delItem").click(function(){
        var product_id = $(this).closest(".cartItem").attr("id").split("_").pop()
        $.post("delete_from_cart/", data={"product_id": product_id}, callback=() => {
            $(this).closest(".cartItem").remove()
        })
    })
});