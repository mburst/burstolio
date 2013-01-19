$(document).ready(function(){
    
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
    
    !function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");
});