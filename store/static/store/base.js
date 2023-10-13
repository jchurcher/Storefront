function displayBanner(text){
    var time = new Date().getTime().toString()
    time = time.substring(time.length - 5)
    $("#bannerSet").append("<div class='banner' id='"+time+"'>"+text+"</div>")
    console.log("created:", time)

    setTimeout(function(){
        $("#"+time).remove()
        console.log("removed:", time)
    }, 5000)
}