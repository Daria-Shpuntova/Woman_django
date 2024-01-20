$(function(){
    $("#menu").click(function(){
        if ($(".menu-li").hasClass("show") && $(".header").hasClass("header2") && $(".mainmenu").hasClass("header2") && $(".logo").hasClass("logo2")){
            $(".menu-li").removeClass("show");
            $(".header").removeClass("header2");
            $(".mainmenu").removeClass("header2");
            $(".logo").removeClass("logo2");
        } else {
            $(".menu-li").addClass("show");
            $(".header").addClass("header2");
            $(".mainmenu").addClass("header2");
            $(".logo").addClass("logo2");
        }
    });
});