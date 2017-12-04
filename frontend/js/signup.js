function processForm()
{
        //grab all of the items from the form
        var username = document.signupForm.username.value;
        var password = document.signupForm.password.value;
        var confpassword = document.signupForm.passwordverify.value;

        if(password != confpassword)
        {
                alert("Passwords do not match!");
        }


        var postRequest = new XMLHttpRequest();
        var url = "submitURL";
        postRequest.open("POST",url, true);
        postRequest.setRequestHeader("Content-type", "application/json");
	//what to do when request is done
	postRequest.onreadystatechange = function() {
		//success
		if(this.readyState == 4 && this.status == 200)
		{
			onSuccess();
		}
		//failure
		if(this.readyState == 4 && this.status == 418)
		{
			alert("invalid credentials");
		}

	}
	var data = JSON.stringify({"username": username, "password": password});
	postRequest.send(data);

}

function cancel()
{
	window.location.href = "../html/login.html";
}

function onSuccess()
{
	window.location.href = "../html/joingame.html";
}
