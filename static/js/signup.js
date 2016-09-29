var planIcons = null;
var buttons = null;
$(document).ready(function(){
	$("[rel=tooltip]").tooltip({ placement: 'right'});
	buttons = $(document).find("button");
	planIcons = $(document).find("span[id^=plan]");
	buttons.on("click",{},buttonHandler);
	planIcons.on("click",{},iconHandler);
});


function buttonHandler(event){
	var id = event.currentTarget.id;
	switch (id){
		case "btnSignup": // Signing up
			sign_up();
			break;
	}
}
function iconHandler(event){
	planIcons.each(function(){$(this).removeClass("icon_selected");});
	var object = event.currentTarget;
	$(object).addClass("icon_selected");
}
function get_plan_id(){
	selected_plan = $(document).find("span.icon_selected");
	if (selected_plan.length == 0){return 0;}
	switch (selected_plan.prop("id")){
		case "planFree":return 1;
		case "planBasic":return 2;
		case "planPrem":return 3;
	}
}

function sign_up()
{
	var txtOrg = $("input#txtOrg");
	var txtEmail = $("input#txtEmail");
	var txtAdmin = $("input#txtAdmin");
	var txtPass = $("input#txtPassword");
	var txtConfpass = $("input#txtConfpassword");
	var plan_id = get_plan_id();
	
	// Checking data
	if (txtOrg.val() == ""){txtOrg.focus();return;}
	if (txtEmail.val() == ""){txtEmail.focus();return;}
	if(!isValidEmailAddress( txtEmail.val() ) ) {
		show_toast(LEVEL_WARN,error_incorrect_email);txtEmail.focus();return;}
	if (txtPass.val() == ""){txtPass.focus();return;}
	if (txtPass.val() != txtConfpass.val() ){
		show_toast(LEVEL_WARN,error_pass_mismatch);return;
	}
	if (plan_id == 0){
		show_toast(LEVEL_WARN,"Please select a plan");return;
	}

	CreateAJAX("/signup/","POST","json",JSON.stringify({
		name: txtOrg.val(),
		admin: (txtAdmin.val() == "" ? "n/a" : txtAdmin.val()),
		email: txtEmail.val(),
		pass: txtPass.val(),
		plan:plan_id
	}))
	.done(function(response){
		if (response.status == 201){
			show_toast(LEVEL_SUCCESS,"Account has been created. Redirecting to Sign In page");
			setTimeout(redirect,2000);
		}
		else{
			show_toast(LEVEL_DANGER,parse_json_response(xhr.responseText).message);
		}
	})
	.fail(function(xhr){
		show_toast(LEVEL_DANGER,parse_json_response(xhr.responseText).message);
	})
}
function redirect(){
	self.location.href = "/signin"
}
