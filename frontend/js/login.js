function processFormSubmit()
{
	alert("Submit button was pressed");
	//grab all of the items from the form
	var username = document.signupForm.username;
	var password = document.signupForm.password;
	var confpassword = document.signupForm.passwordVerify;
	
	if(username == "" || password == "" || confpassword == "")
	{
		alert("Form not filled in");
	}
	if(password != confpassword)
	{
		alert("Passwords do not match!");
	}


	var postRequest = new XMLHttpRequest();
	var url = "submitURL";
	postRequest.open("POST",url, true);
	postRequest.setRequestHeader("Content-type", "application/json");
}

function CreateAccount()
{
	window.location.href = "../html/signup.html";
}
