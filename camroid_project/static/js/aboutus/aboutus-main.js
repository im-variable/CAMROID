$(function(){

    $("input[name=sentiment]").change(function(){
        var sentiment_Value = $("input[name='sentiment']:checked").val();
        
        // alert(sentiment_Value)
        // if(sentiment_Value){
            $.ajax({
                    type:"GET",
                    data: { "sentiment_Value": sentiment_Value },
                    url: "/aboutus",
                    success: function( data )
                    {

                    }
                });
            // }
        });

});
