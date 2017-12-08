//all of the countries on the gameboard
var countries = ["OffMap", "Liverpool", "Ireland", "Wales", "Edinburgh", "London", "Norway", "Sweden", "Finland",
    "Vologda", "Leningrad", "Smolensk", "Moscow", "Bellorussia", "Presov", "Kiev", "Holland", "Kiel", "Berlin",
    "Siliesia", "Ruhr", "Munich", "Belgium", "Picardy", "Brest", "Paris", "Marseille", "Gacony", "Bilboa", "Lugo",
    "Portugal", "Seville", "Valancia", "Barcelona", "Ust", "Pechora", "Komi", "Gorki", "Crimea", "Rostov",
    "Czechoslovakia", "Austria", "Hungary", "Bosnia", "Albania", "Serbia", "Banat", "Romania", "Bulgaria", "Macedonia",
    "Greece", "Istanbul", "Samsun", "Kras", "Izmir", "Lebanon", "Israel", "Jordan", "Piedmont", "Venice", "Tuscany",
    "Rome", "Apulia", "Naples", "Sicily", "Sardinia", "Casablanca", "Algiers", "Setif", "Aflou", "Sahara", "Fazzar",
    "Murzq", "Benghazi", "Sallum", "Tobruk", "Cairo", "Nile", "Sawhaj", "Crete", "IrishSea", "NorthSea", "BalticSea",
    "EnglishChannel", "AtlanticOcean", "BayofBiscay", "Gibraltar", "WesternMediterranean", "GulfofLyons",
    "TyrrhenianSea", "IonianSea", "AdriaticSea", "AgeanSea", "EasternMediterranean", "RedSea", "LakeCherkassy",
    "WestBlackSea", "EastBlackSea"];



function onLeave()
{
	window.location.href = "../html/joingame.html"
    //send a leave post request
}

//loads the game
function loadGame()
{

    console.log("Loading Game");

    var url = "/api/get_game";

    makeGetRequest(url, function (data) {
        updateBoard(data);
    }, function () {
        alert("There was a problem connecting to the server")
    });

}

var apiUrl = 'http://127.0.0.1:5000';

var makeGetRequest = function(url, onSuccess, onFailure) {
    $.ajax({
        type: 'GET',
        url: apiUrl + url,
        dataType: "json",
        success: onSuccess,
        error: onFailure
    });
};

var makePostRequest = function(url, data, onSuccesss, onFailure)
{
    $.ajax({
        type: 'POST',
        url: apiUrl + url,
        data: JSON.stringify(data),
        contentType: "application/json",
        dataType: "json",
        success: onSuccesss,
        error: onFailure
    });
};

//clears the board
function clearBoard()
{

    for(var index in countries)
    {
        removeTeam(countries[index]);
        removeUnit(countries[index]);
    }
    $(".attackCountriesCnt").hide();

}

function test()
{
    var test = {"teams":
            [{"army":["Lugo","IrishSea","London"],"navy":["NorthSea","Wales"],"score":"25","name":"batman"},
             {"army":["Paris","Nile","Kiev"],"navy":["AtlanticOcean","Wales"],"score":"25","name":"notbatman"}]};
    //send a get request for the inital positions
    updateBoard(test);
}

function updateBoard(json)
{


    removeUnits();
    $(".bottomBar").empty();
    //parse through all the teams

    $("#origin").empty()
    $("#origin").append('<option selected disabled hidden >Choose a Unit</option>');
    $("#origin").prop('disabled', false);

    $("#action").prop('disabled', true);
    $("#submit").prop('disabled', true);
    $("#targetCountries").prop('disabled', true);

    var units = [];
    for(var teamIndex in json.teams) {
        
        //generate teams
        $(".bottomBar").append(
        '<div class="team team' + (Number(teamIndex) + 1) +'"><div class="teamName">Team: '+ json.teams[teamIndex].name +'</div><div class="teamScore">Score: 0</div></div>');

        //fill army
        for (var index in json.teams[teamIndex].army)
        {
            removeUnit(json.teams[teamIndex].army[index]);
            addArmy(json.teams[teamIndex].army[index]);
            changeTeam(json.teams[teamIndex].army[index], Number(teamIndex) + 1);
            units.push(json.teams[teamIndex].army[index]);
        }
        //fill navy
        for (var index in json.teams[teamIndex].navy)
        {
            removeUnit(json.teams[teamIndex].navy[index]);
            addNavy(json.teams[teamIndex].navy[index]);
            changeTeam(json.teams[teamIndex].navy[index], Number(teamIndex) + 1);
            units.push(json.teams[teamIndex].navy[index]);
        }
        updateScore(Number(teamIndex) + 1, Number(json.teams[teamIndex].score));
    }

    units.sort();

    for (var i in units){
        $("#origin").append('<option value="' + units[i] + '">' + units[i] + '</option>');
    }


    $("#origin").append('<option selected disabled hidden >Choose a Unit</option>');
    $("#action").prop('disabled', true);

    $("#submit").prop('disabled', true);
    $("#targetCountries").prop('disabled', true);
    $("#origin").prop('disabled', false);
}

function onChooseOrigin(){
    $("#origin").prop('disabled', false);

    $("#action").prop('disabled', false);
    $("#action").prop('selectedIndex', 0);

    $("#targetCountries").prop('disabled', true);
    $("#targetCountries").empty();

    $("#attackCountries").prop('disabled', true);

    $("#submit").prop('disabled', true);
}

function onSelectCommand(){

    function onSuccess(data) {
        target= $("#targetCountries");
        target.empty();

        target.append('<option selected hidden disabled> Select a location to target </option>')
        if (data['status'] == '200'){

            data['targetable'].sort();
            for (var index in data["targetable"]){
                target.append('<option value="' + data['targetable'][index] + '">' + data['targetable'][index] +'</option>')
            }


            $("#origin").prop('disabled', false);
            $("#action").prop('disabled', false);
            $("#targetCountries").prop('disabled', false);
            $("#attackCountries").prop('disabled', true);
            $("#attackCountries").empty();
            $("#submit").prop('disabled', true);

        } else {
            alert("Server Error");
        }

    }

    function onFail() {
        alert("Error communicating with server");
    }



    var origin = $("#origin").val();
    var type = $("#action").val();
    var data = {"origin":origin, "type":type};

    makePostRequest('/api/get_targetable', data, onSuccess, onFail);
}

function onChooseTarget(){
    $("#origin").prop('disabled', false);

    $("#action").prop('disabled', false);

    $("#targetCountries").prop('disabled', false);


    var attack = document.getElementById("attackCountries");

    orderType = $("#action").val();

    if(orderType == "support") {
        $("#submit").prop('disabled', true);

        var origin = $("#origin").val();
        var supporting = $("#targetCountries").val();

        var data = {"origin":origin, "supporting":supporting};

        function onSuccess(data) {
            $("#attackCountries").prop('disabled', false);

            data['targetable'].sort();

            $("#attackCountries").append('<option selected hidden disabled>Select a location to attack</option>');

            for (var index in data["targetable"]){
                $("#attackCountries").append('<option value="' + data['targetable'][index] + '">' + data['targetable'][index] +'</option>');
            }
        }

        function onFail(){
            alert("Error communicating with the server")
        }

        makePostRequest('/api/get_attackable_in_common', data, onSuccess, onFail)
    } else {
        $("#submit").prop('disabled', false);
    }
}

function onChooseSecondTarget(){
    $("#origin").prop('disabled', false);

    $("#action").prop('disabled', false);
    $("#targetCountries").prop('disabled', false);

    $("#attackCountries").prop('disabled', false);
    $("#submit").prop('disabled', false);
}

//removes the unit from the country
function removeUnit(country)
{
    var country = $("." + country);
    country.empty();
}

//adds an army to the country
function addArmy(country)
{
    var country = $("." + country);
    country.prepend('<img class=\"army\" src=\"../sources/Army.png\">');
}

//adds an army to the country
function addNavy(country)
{
    var country = $("." + country);
    country.prepend('<img class=\"navy\" src=\"../sources/Navy.png\">');
}

//changes the countries team
//string country
//number teamNum
function changeTeam(country, teamNum)
{
    var country = $("." + country);
    //removes all other teams
    country.removeClass("team1");
    country.removeClass("team2");
    country.removeClass("team3");
    country.removeClass("team4");
    country.addClass("team" + teamNum);
}

//tells if the unit has been ordered
function unitOrdered(country)
{
    var country = $("." + country);
    country.removeClass("ordered");
    country.addClass("ordered");
}

//removes the countries team
function removeTeam(country)
{
    var country = $("." + country);
    country.removeClass("team1");
    country.removeClass("team2");
    country.removeClass("team3");
    country.removeClass("team4");
}

//updates the score based on the team number and score
function updateScore(teamNum, score)
{
    $(".team.team"+teamNum +" .teamScore").text("score: " + score);
}

//other functions/////////////////////////////////////////////////////////////////////////////////
function onSubmit()
{
    var url = "/api/send_order";


    var form = $(".sendOrderForm");
    form.submit(function(e) {
        e.preventDefault();
    });

    //selected country
    var select = document.getElementById("origin");
    select = select.options[select.selectedIndex].text;

    //action
    var action = document.getElementById("action");
    action = action.options[action.selectedIndex].value;

    if(action === "support")
    {
        //targeted country
        var supporting = document.getElementById("targetCountries");
        supporting = supporting.options[supporting.selectedIndex].text;

        //supporting attack on a country
        var attack = document.getElementById("attackCountries");
        attack = attack.options[attack.selectedIndex].text;

        //need to send selected country action and target with post request
        var json = {"origin":select, "action":action, "target":attack, "supporting":supporting};
    }
    else
    {
        //targeted country
        var target = document.getElementById("targetCountries");
        target = target.options[target.selectedIndex].text;

        //need to send selected country action and target with post request
        var json = {"origin": select, "action": action, "target": target};
    }
    makePostRequest(url, json,
        function (data) {
            if (data.status == 200) {
                $("#origin").prop('disabled', false);
                $("#origin").prop('selectedIndex', 0);

                $("#action").prop('disabled', true);
                $("#action").prop('selectedIndex', 0)

                $("#targetCountries").prop('disabled', true);

                $("#attackCountries").prop('disabled', true);
                $("#submit").prop('disabled', true);

                unitOrdered(select);
            } else {
                alert("Invalid Order was entered");
            }
        },
        function () {
            alert("Server Error");
        });
}

function onResolveOrders()
{
    var url = "/api/resolve_orders";
    makeGetRequest(url,
        function (data) {
            console.log("Update game board");
            updateBoard(data);
        },
        function ()
        {
            alert("Server Failure");
        })
}

//removes the units from the board
function removeUnits()
{
    for(var index in countries)
    {
        removeUnit(countries[index]);
    }
}

//populates the board
function populate()
{
    for(var index in countries)
    {
        changeTeam(countries[index], 4);
    }

}






