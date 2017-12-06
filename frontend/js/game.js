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

}

//clears the board
function clearBoard()
{

    for(var index in countries)
    {
        removeTeam(countries[index]);
        removeUnit(countries[index]);
    }

}

function test()
{
    var test = {"team1":{"army":["Lugo","IrishSea","London"],"navy":["NorthSea"]}};
    //send a get request for the inital positions
    updateBoard(test);
}

function updateBoard(json)
{

    for(var index in json.team1.army)
    {
        removeUnit(json.team1.army[index]);
        //document.getElementsByClassName(json.team1.army[index]).remove();
        addNavy(json.team1.army[index]);
        changeTeam(json.team1.army[index], 3);
        unitOrdered(json.team1.army[index]);
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