function onRules()
{
	window.open("../html/rules.html");
}

function onJoinQueue()
{
	//sends post request to join game then takes you to game
	window.location.href = "../html/game.html";
}

function onLogout()
{
	//sends post request to logout takes you to the main page
	window.location.href = "../html/login.html";
}
