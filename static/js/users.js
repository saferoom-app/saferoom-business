$(document).ready(function(){
	// Getting the list of users
	list_users();
});

function buttonHandler(event)
{
	var id = event.currentTarget.id
	switch (id){
		case "btnAdd":
			load_modal("createuser",{});
			break;
		case "btnImport":
			break;
		case "btnCreate":
			create_user();
			break;
	}
}

function hrefHandler(event){
	load_modal("getuser",{uid:event.currentTarget.id});
	return false;	
}
function list_users(){
	$("div#listUsers").html("<img src=\"/static/images/89.gif\"/>");
	CreateAJAX("/admin/users","POST","html",{})
	.done(function(response){
		$("div#listUsers").html(response);
	})
	.fail(function(xhr){
		$("div#listUsers").html(response);
	});
}
$(document).on("click","a.table_href",hrefHandler);
$(document).on("click","button",buttonHandler);
function create_user()
{
	services = new Array();
	// Getting a list of selected services
	checkboxes = $(document).find("input[id^=service]");
	checkboxes.each(function(){
		services.push({id:$(this).val(),"enabled":$(this).is(":checked")});
	});
	var txtName = $("input#txtName");
	var txtEmail = $("input#txtEmail");
	var txtPass = $("input#txtPass");
	var txtConfpass = $("input#txtConfpass");

	// Checking user input
	if (txtName.val() == ""){txtName.focus();return;}
	if(!isValidEmailAddress( txtEmail.val() ) ) {
		show_toast(LEVEL_WARN,error_incorrect_email);txtEmail.focus();return;}
	if (txtPass.val() == ""){txtPass.focus();return;}
	if (txtPass.val() != txtConfpass.val() ){show_toast(LEVEL_WARN,error_pass_mismatch);return;}
	// Preparing the object
	user = {
		name: txtName.val(),
		email:txtEmail.val(),
		pass: txtPass.val(),
		services: services
	}
	
	// Sending a HTTP POST request
	CreateAJAX("/admin/users/create","POST","json",JSON.stringify(user))
	.done(function(response){
		// Closing modal window and updating the list of users
		$("div#modalWindow").modal('toggle');		
		if (response.status != 201){
			show_toast(LEVEL_DANGER,parse_json_response(response).message);
			return;
		}
		
		list_users()
	})
	.fail(function(xhr){
		$("div#modalWindow").modal('toggle');
		show_toast(LEVEL_DANGER,parse_json_response(xhr.responseText).message);
	});

	// Getting a list 
}