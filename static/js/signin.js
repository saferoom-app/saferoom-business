$(function() {
    var buttons = $(document).find("button");
	buttons.on("click",{},clickHandler);
});

function clickHandler(event)
{
	var id = event.currentTarget.id;
	switch (id)
	{
		case "btnSignin":
			sign_in();
			break;

		case "btnSignup":
			self.location.href = "/signup";
			break;
	}
}

function sign_in()
{
	// Checking the input data
	var email = $("input#txtEmail");
	var pass  = $("input#txtPassword");
	if (email.val() == ""){email.focus();return;}
	if (pass.val() == ""){pass.focus();return;}

	CreateAJAX("/signin/","POST","json",JSON.stringify({"email":email.val(),"pass":pass.val()}))
	.done(function(response){
		if (response.status == 200){
			alert("Success!")
		}
		else{
			show_toast(LEVEL_DANGER,parse_json_response(xhr.responseText).message);
		}
	})
	.fail(function(xhr){
		show_toast(LEVEL_DANGER,parse_json_response(xhr.responseText).message);
	});
}