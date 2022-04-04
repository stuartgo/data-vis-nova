

console.log(document.getElementsByClassName(".p"))
//document.getElementsByClassName(".p")[0].onclick=function(){console.log("Ass")}

console.log("dicks")


$('document').ready(function(){
    $(".p").on("click", function() {
        $(".p").css("color","red")
    }); 
    console.log($("#minge"))
    console.log("schim")


});

window.addEventListener("load", function () {
    console.log($("#presidential_toggle"))
    $("#presidential_toggle").on("click", function() {
        $(".rc-slider-handle").toggleClass("down")
        console.log("Ass")
    }); 
})