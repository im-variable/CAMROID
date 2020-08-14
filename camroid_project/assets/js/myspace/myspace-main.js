 $(function() {
    		$('.pop_img').on('click', function() {
		    var img = $(this).find('img').attr('src')
		    console.log(img)
			$('.imagepreview').attr('src', $(this).first('img').attr('src'));
			$('#imagemodal').modal('show');
		});

/*for profile photo preview in profile tab*/
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#user-photo').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#profile-upload").change(function(){
        readURL(this);
    });


});
/* for delete of image from processing/collection tab */
        function img_del(pk){
        var id = pk

        console.log(id)
        $('#confirm_del').val(pk)
        console.log($('#confirm_del').val(pk))
        }

