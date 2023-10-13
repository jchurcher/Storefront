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
        headers: { "X-CSRFToken": getCookie("csrftoken") },
    });

    var clickIds = {};

    // Increment quantity of item
    $(".incQuantity").click(function(){
        var inQuantity = $(this).parent().siblings().children(".itemQuantity")
        inQuantity[0].stepUp()

        var productId = inQuantity.closest(".cartItem").attr("id").split("_").pop()

        clickIds[productId] = new Date().getTime()
        var thisClickId = clickIds[productId]
<<<<<<< HEAD

        // Sends post request 1 second after most recent inc/dec
        setTimeout(function() {
            if(thisClickId != clickIds[productId]){  // Only click if this is the most recent click
                return
            }
=======

        console.log("new timer:", thisClickId, "for", productId)

        // Sends post request 1 second after most recent inc/dec
        setTimeout(function() {
            console.log("check timer: ", thisClickId, "for", productId, "against", clickIds[productId])
            if(thisClickId != clickIds[productId]){  // Only click if this is the most recent click
                return
            }
            console.log("send", thisClickId, "for", productId)
>>>>>>> 88e37fe6cb2314444fd707d96632822ae527d15c
            delete clickIds[productId];
            $.post("change_item_quantity/", data={"quantity": inQuantity.val(), "product_id": productId}, callback=(data) => displayBanner(data))
        }, 1000);
    })
    
    // Decrement quantity of item
    $(".decQuantity").click(function(){
        var inQuantity = $(this).parent().siblings().children(".itemQuantity")
        inQuantity[0].stepDown()

        var productId = inQuantity.closest(".cartItem").attr("id").split("_").pop()

        clickIds[productId] = new Date().getTime()
        var thisClickId = clickIds[productId]

        // Sends post request 1 second after most recent inc/dec
        setTimeout(function() {
            if(thisClickId != clickIds[productId]){  // Only click if this is the most recent click
                return
            }
            delete clickIds[productId];
            $.post("change_item_quantity/", data={"quantity": inQuantity.val(), "product_id": productId}, callback=(data) => displayBanner(data))
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

    $(".delItem").click(function(){
        var product_id = $(this).closest(".cartItem").attr("id").split("_").pop()
        $.post("delete_from_cart/", data={"product_id": product_id}, callback=(data) => {
            $(this).closest(".cartItem").remove()
            displayBanner(data)
        })
    })
});