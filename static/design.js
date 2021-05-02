// This function is created to manage different tabs of vertical tabbar
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



  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawCharts);

  function showTopRatedMovieChart() {
    var data = google.visualization.arrayToDataTable([
        ['Year', 'Sales', 'Expenses'],
        ['2013',  1000,      400],
        ['2014',  1170,      460],
        ['2015',  660,       1120],
        ['2016',  1030,      540]
      ]);
  
      var options = {
        title: 'Company Performance',
        hAxis: {title: 'Year'},
        vAxis: {minValue: 0  },
      };
  
      var chart = new google.visualization.AreaChart(document.getElementById('topratedmovies'));
      chart.draw(data, options);

  }
  function drawCharts() {
    
    showTopRatedMovieChart()

  }