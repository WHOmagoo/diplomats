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
    //sends a get request for the board
    var getrqst = new XMLHttpRequest();

    var url = "url";

    getrqst.open("GET", url, true);
    getrqst.setRequestHeader("Content-type", "application/json");
    getrqst.onreadystatechage = function () {
        if(getrqst.readyState === 4 && getrqst.status === 200) {
            var json = JSON.parse(getrqst.responseText);
            updateBoard(json);
        }
    };

    //fill select options
    var selectCountries = $("#selectCountries");
    var targetCountries = $("#targetCountries");
    var attackCountries = $("#attackCountries");
    for(var index in countries.sort())
    {
        selectCountries.append('<option value="' + countries[index] + '">' + countries[index] + '</option>');
        targetCountries.append('<option value="' + countries[index] + '">' + countries[index] + '</option>');
        attackCountries.append('<option value="' + countries[index] + '">' + countries[index] + '</option>');
    }

}

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
            [{"army":["Lugo","IrishSea","London"],"navy":["NorthSea","Wales"],"score":"25"},
             {"army":["Paris","Nile","Kiev"],"navy":["AtlanticOcean","Wales"],"score":"25"}]};
    //send a get request for the inital positions
    updateBoard(test);
}

function updateBoard(json)
{
    //parse through all the teams
    for(var teamIndex in json.teams) {
        //fill army
        for (var index in json.teams[teamIndex].army)
        {
            removeUnit(json.teams[teamIndex].army[index]);
            addArmy(json.teams[teamIndex].army[index]);
            changeTeam(json.teams[teamIndex].army[index], Number(teamIndex) + 1);
        }
        //fill navy
        for (var index in json.teams[teamIndex].navy)
        {
            removeUnit(json.teams[teamIndex].navy[index]);
            addNavy(json.teams[teamIndex].navy[index]);
            changeTeam(json.teams[teamIndex].navy[index], Number(teamIndex) + 1);
        }
        updateScore(Number(teamIndex) + 1, Number(json.teams[teamIndex].score));
    }



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
    //https://stackoverflow.com/questions/24468459/sending-a-json-to-server-and-retrieving-a-json-in-return-without-jquery
    var postrqst = new XMLHttpRequest();
    var url = "url";

    postrqst.open("POST", url, true);
    postrqst.setRequestHeader("Content-type", "application/json");
    postrqst.onreadystatechage = function (){
        if (postrqst.readyState === 4 && postrqst.status === 200)
        {
            unitOrdered(select);
        }
        else if(postrqst.readyState === 4 && postrqst.status === 418)
        {
            alert("Invalid order");
        }
    };

    var form = $(".sendOrderForm");


    form.submit(function(e) {
        e.preventDefault();
    });

    //selected country
    var select = document.getElementById("selectCountries");
    select = select.options[select.selectedIndex].text;

    //action
    var action = document.getElementById("action");
    action = action.options[action.selectedIndex].value;

    if(action === "support")
    {
        //targeted country
        var target = document.getElementById("targetCountries");
        target = target.options[target.selectedIndex].text;

        //supporting attack on a country
        var attack = document.getElementById("attackCountries");
        attack = attack.options[attack.selectedIndex].text;

        //need to send selected country action and target with post request
        var json = JSON.stringify({"select":select, "action":action, "target":target, "attack":attack});
    }
    else
    {
        //targeted country
        var target = document.getElementById("targetCountries");
        target = target.options[target.selectedIndex].text;

        //need to send selected country action and target with post request
        var json = JSON.stringify({"select": select, "action": action, "target": target});
    }
    postrqst.send(json);
}






