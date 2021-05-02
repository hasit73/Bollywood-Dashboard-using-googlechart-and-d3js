from flask import Flask,render_template
import pandas as pd
import numpy as np
import json



app = Flask(__name__)

movieDataPath = "Dataset/BollywoodMovieDetail.csv"
movieData = pd.DataFrame()

actorGenreDataPath = "Dataset/ActorsGenreTable.csv"
actorGenreData = pd.DataFrame()

preprocessedDataPath = "Dataset/PreprocessedActors.csv"
preprocessedData = pd.DataFrame()

yearwiseactorsperformanceDataPath = "Dataset/YearWiseActorsHistory.csv"
yearWiseActorsPerformanceData = pd.DataFrame()


movieBudgetDataPath = "Dataset/MovieBudgetDetails.csv"
movieBudgetData = pd.DataFrame()

movieProfitDataPath = "Dataset/MovieProfitDetails.csv"
movieProfitData = pd.DataFrame()

movieReleasedDataPath = "Dataset/MovieReleasedTimeData.csv"
movieReleasedData = pd.DataFrame()

overallActorsMoviesDataPath = "Dataset/OverallActorsMovies.csv"
overallActorsMoviesData = pd.DataFrame()

@app.route("/")
def home():
    context = {}
    
    # get the ready data
    yearWise,yearWiseMoviesCount = getYearWiseMovieData()
    topMovies = getTopRatedMoviesData()
    actorsHitsFlops = getActorsPreprocessedData()
    yearWiseActorsPerformance,yearWiseActorsPerformanceList = getYearWiseActorPerformaceData()
    genreWiseMovieBudget = getMovieBudgetGenreWise()
    genreWiseBudgetDistribution,genreWiseProfitDistribution = getGenreWiseBudgetAndProfitDistribution()
    movieReleasedData = getMovieReleasedData()
    ageAndGenreData = getAgeGroupAndGenreRelationData()
    overallActorsData = overallActorsMoviesData.values.tolist()

    topRatedActors = getTopRatedGenreWiseActors()

    # set the data in context
    context["yearWise"] = yearWise
    context["topMovies"] = topMovies
    context["topRatedActors"] = topRatedActors
    context["genreWiseBudgetDistribution"] = genreWiseBudgetDistribution
    context["genreWiseProfitDistribution"] = genreWiseProfitDistribution
    context["genreWiseMovieBudget"] = genreWiseMovieBudget
    context["listOfActors"] = actorGenreData["actor"].unique().tolist()
    context["listOfGenres"] = actorGenreData["genre"].unique().tolist()
    context["actorsHitsFlops"] = actorsHitsFlops.tolist()
    context["yearWiseActorsPerformance"] = yearWiseActorsPerformance.tolist()
    context["yearWiseActorsPerformanceList"] = yearWiseActorsPerformanceList
    context["movieReleasedData"] = movieReleasedData
    context["ageAndGenreData"] = ageAndGenreData
    context["overallActorsData"] = overallActorsData
    context["yearWiseMoviesCount"] = yearWiseMoviesCount
    context["getGenreDataForCirclePackingChart"] = getGenreDataForCirclePackingChart()
    context["ActorsBudgetData"] = getActorsBudgetData()

    return render_template("home.html",context =context)

def loadDataset():
    global movieData
    movieData = pd.read_csv(movieDataPath)

    global actorGenreData
    actorGenreData = pd.read_csv(actorGenreDataPath)

    global preprocessedData
    preprocessedData = pd.read_csv(preprocessedDataPath)

    global yearWiseActorsPerformanceData
    yearWiseActorsPerformanceData = pd.read_csv(yearwiseactorsperformanceDataPath)

    global movieBudgetData
    movieBudgetData = pd.read_csv(movieBudgetDataPath)
    
    global movieProfitData
    movieProfitData = pd.read_csv(movieProfitDataPath)

    global movieReleasedData
    movieReleasedData = pd.read_csv(movieReleasedDataPath)

    global overallActorsMoviesData
    overallActorsMoviesData= pd.read_csv(overallActorsMoviesDataPath)

def getYearWiseMovieData():
    t = movieData["releaseYear"].value_counts().sort_index().reset_index().values
    t1 = []
    for i,v in enumerate(t):
        s1 = int(sum(t[:i+1,1]))
        s2 = int(s1+t[i,1])
        t1.append([str(t[i][0]),s1,s1,s2,s2])
    return t1,t.tolist()

def getTopRatedGenreWiseActors():
    t = actorGenreData[["genre","actor","normalizedRating"]].sort_values(by="normalizedRating",ascending=False).values.tolist()
    return t

def getTopRatedMoviesData():
    t = movieData[["title","hitFlop","genre","actors"]].sort_values(by="hitFlop",ascending = False)
    t = t.dropna(subset=["genre"])
    t["genre"] = t["genre"].apply(lambda x: x.lower().strip())
    t = t.values.tolist()
    return t

def getActorsPreprocessedData():
    t = preprocessedData[["actorName","totalHits","totalFlops"]].values
    return t

def getYearWiseActorPerformaceData():
    
    t =yearWiseActorsPerformanceData.copy()
    t = t.pivot(index="year",columns="name",values="Hit").reset_index()
    t["year"] = t["year"].apply(lambda x: x[:4])
    cols = np.array([t.columns])
    t = np.concatenate([cols,t.values])


    t1 = yearWiseActorsPerformanceData.copy()
    t1 = t1.groupby("name")["HitPercentage"].mean().reset_index().sort_values(by="HitPercentage",ascending=False).values.tolist()
    return t,t1


def getMovieBudgetGenreWise():
    return movieBudgetData[["genre","min","25%","75%","max"]].values.tolist()

def getGenreWiseBudgetAndProfitDistribution():
    t1 = [movieBudgetData.columns.values.tolist()] + movieBudgetData.values.tolist()
    t2 = [movieProfitData.columns.values.tolist()] + movieProfitData.values.tolist()
    return t1,t2

def getMovieReleasedData():
    t  = movieReleasedData.copy()
    t["releaseYear"] = t["releaseYear"].astype("str")
    t = t.values.tolist()[::-1] + [t.columns.tolist()]
    t = t[::-1]
    return t

def getAgeGroupAndGenreRelationData():
    t = pd.read_csv("./Dataset/ageGroupAndGenreRelation.csv")
    t1 = [t.columns.tolist()]+t.values.tolist()
    return t1

def getGenreDataForCirclePackingChart():
    t = pd.read_csv("./Dataset/GenreDataForCirclePacking.csv")
    t = t.sort_values("size",ascending=False)
    t = [{"id":"All","parentId":None,"size":None}] + [{"id":x[0],"parentId":x[1],"size":x[2]} for x in t.values]
    return t

def getActorsBudgetData():
    t = pd.read_csv("./Dataset/ActorsBudgetData.csv")
    return t.values.tolist()
if __name__=="__main__":
    loadDataset()
    app.run(debug=True)

