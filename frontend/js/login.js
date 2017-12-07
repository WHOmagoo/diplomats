function processForm()
{
	//grab all of the items from the form
	var username = document.loginForm.username.value;
	var password = document.loginForm.password.value;
	
	if(username == "" || password == "")
	{
		alert("Form not filled in");
	}


	var postRequest = new XMLHttpRequest();
	var url = "submitURL";
	postRequest.open("POST",url, true);
	postRequest.setRequestHeader("Content-type", "application/json");

	postRequest.onreadystatechage = function() {
		if(this.readyState == 4 && this.status== 200)
		{
			onSuccess();
		}
		if(this.readyState == 4 && this.status == 418)
		{
			alert("invalid credentials");
		}
	}

	var data = JSON.stringify({"username":username, "password":password});
	postRequest.send(data);

	onSuccess();
}

function CreateAccount()
{
	window.location.href = "../html/signup.html";
}

function onSuccess()
{
	window.location.href = "../html/joingame.html";
}
