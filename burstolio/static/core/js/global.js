$(document).ready(function(){
    //Psuedo-fixed header only on non-mobile browsers
    if(!/Android|webOS|iPhone|iPad|iPod|BlackBerry|Windows Phone/i.test(navigator.userAgent)){
        var initialTop = 0;
        var windowScroll = 0;
        $(window).scroll(function() {
            windowScroll = $(window).scrollTop();
            $('#header').css('top', windowScroll + initialTop + 'px' );
        });
    }
    
    $("#query").focus(function(){
        if($(this).val() == "Search..."){
            $(this).val("");   
        }
    });
    
    $("#query").blur(function(){
        if($(this).val() == ""){
            $(this).val("Search...");   
        }
    });    
    
    $("#commenters").on("click", ".reply", function(event){
        event.preventDefault();
        var form = $("#postcomment").clone(true);
        form.find('.ancestor').val($(this).parent().parent().attr('id'));
        $(this).parent().append(form);
    });
});