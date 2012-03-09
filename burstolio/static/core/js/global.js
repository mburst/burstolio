$(document).ready(function(){
    //Psuedo-fixed header
    var initialTop = 0;
    var windowScroll = 0;
    $(window).scroll(function() {
        windowScroll = $(window).scrollTop();
        $('#header').css('top', windowScroll + initialTop + 'px' );
    });
    
    $("#email").focus(function(){
        if($(this).val() == "Subscribe..."){
            $(this).val("");   
        }
    });
    
    $("#email").blur(function(){
        if($(this).val() == ""){
            $(this).val("Subscribe...");   
        }
    });    
    
    $("#subscribe").submit(function(event){
        event.preventDefault();
        var form = $(this);
        var email = form.find('input[name="email"]').val();
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if(re.test(email)){
            $.get(form.attr('action'), {'email': email},
                function(data){
                    form.replaceWith('<p class="about">'+data+'</p>');
                }
            );
        }
        else{
            alert('I think ' + email + ' is an invalid e-mail address. Please try again.');
        }
    });
    
    $("#commenters").on("click", ".reply", function(event){
        event.preventDefault();
        var form = $("#postcomment").clone(true);
        form.find('.ancestor').val($(this).parent().parent().attr('id'));
        $(this).parent().append(form);
    });
});