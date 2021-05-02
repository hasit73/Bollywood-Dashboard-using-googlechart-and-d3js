// This function is created to manage different tabs of vertical tabbar

console.log("data in js file : ",movieData);


function activateBodyof(s) {       
    var actors = $("#actorsbody")[0];
    var movies = $("#moviesbody")[0];
    var directors = $("#directorsbody")[0];
    if (s == "movies") {
      movies.style.display = "block";
      actors.style.display = "none";
      directors.style.display = "none";
    } else if (s == "actors") {
      actors.style.display = "block";
      movies.style.display = "none";
      directors.style.display = "none";
    } else {
      directors.style.display = "block";
      movies.style.display = "none";
      actors.style.display = "none";
    }
  }

  console.log("data : ",context);

