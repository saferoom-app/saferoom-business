// Messages
error_incorrect_email = "Incorrect email address";
error_pass_mismatch = "Passwords don't match"

// Message levels
LEVEL_SUCCESS = 1;
LEVEL_WARN = 2;
LEVEL_DANGER = 3;

function CreateAJAX(url,requestType,dataType,data){
    
    contentType = ""
    switch (requestType)
    {
    	case "GET":
    		contentType = "text/html";
    		break;
    	case "POST":
    		if (dataType == "json"){contentType = "application/json; charset=utf-8";}
    		else{contentType = "application/x-www-form-urlencoded; charset=utf-8";}
    		break;
    }

	return $.ajax({
     	// The URL for the request
    	url: url, 
    	data: data,
    	type: requestType,
    	contentType: contentType,
    	// The type of data we expect back
    	dataType : dataType
	});
}

function show_toast(type,message){
    toastr.options = {
        "closeButton": false,
        "debug": false,"newestOnTop": false,"progressBar": false,
        "positionClass": "toast-bottom-center","preventDuplicates": false,
        "onclick": null,"showDuration": "300","hideDuration": "1000",
        "timeOut": "6000","extendedTimeOut": "1000","showEasing": "swing",
        "hideEasing": "linear","showMethod": "fadeIn","hideMethod": "fadeOut"
    }

    switch (type)
    {
        case LEVEL_SUCCESS: // success
            toastr['success'](message);
            break;
        case LEVEL_WARN: //warning
            toastr['warning'](message);
            break;
        case LEVEL_DANGER: // error
            toastr['error'](message);
    }
}

function isValidEmailAddress(emailAddress) {
    var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
    return pattern.test(emailAddress);
};

function parse_json_response(response){
    return jQuery.parseJSON(response);
}

function load_modal(mode,filter)
{
    $("div#modalWindow").modal("show");
    CreateAJAX("/modal/"+mode,"GET","html",filter)
    .done(function(response){
        $("div#modalContent").html(response);
    })
    .fail(function(xhr){
        $("div#modalContent").html(xhr.responseText);
    });
}