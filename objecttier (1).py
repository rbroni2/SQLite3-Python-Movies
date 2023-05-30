#
# File: objecttier.py
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
  def __init__(self, Movie_ID, Title, Release_Year):
    self._Movie_ID = Movie_ID; # defining class and initializing 3 var
    self._Title = Title;
    self._Release_Year = Release_Year;
  @property #these functions make them pseudo read only
  def Movie_ID(self):
    return self._Movie_ID;
  @property
  def Title(self):
    return self._Title;
  @property
  def Release_Year(self):
    return self._Release_Year;

##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
  def __init__(self,Movie_ID,Title,Release_Year,Num_Reviews,Avg_Rating):
    self._Movie_ID = Movie_ID; # defining class and initializing vars
    self._Title = Title;
    self._Release_Year = Release_Year;
    self._Num_Reviews = Num_Reviews;
    self._Avg_Rating = Avg_Rating;
  @property #these functions make them pseudo read only
  def Movie_ID(self):
    return self._Movie_ID;
  @property
  def Title(self):
    return self._Title;
  @property
  def Release_Year(self):
    return self._Release_Year;
  @property
  def Num_Reviews(self):
    return self._Num_Reviews;
  @property
  def Avg_Rating(self):
    return self._Avg_Rating;
##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
  def __init__(self,Movie_ID,Title,Release_Date,Runtime,Original_Language, Budget, Revenue, Num_Reviews, Avg_Rating, Tagline, Genres, Production_Companies):# defining Movie Details class with lots of vars
    self._Movie_ID = Movie_ID;
    self._Title = Title;
    self._Release_Date = Release_Date;
    self._Runtime = Runtime;
    self._Original_Language = Original_Language;
    self._Budget = Budget;
    self._Revenue = Revenue;
    self._Num_Reviews = Num_Reviews;
    self._Avg_Rating = Avg_Rating;
    self._Tagline = Tagline;
    self._Genres = Genres;
    self._Production_Companies = Production_Companies;
  @property #these functions make them pseudo read only
  def Movie_ID(self):
    return self._Movie_ID;
  @property
  def Title(self):
    return self._Title;
  @property
  def Release_Date(self):
    return self._Release_Date;
  @property
  def Runtime(self):
    return self._Runtime;
  @property
  def Original_Language(self):
    return self._Original_Language;
  @property
  def Budget(self):
    return self._Budget;
  @property
  def Revenue(self):
    return self._Revenue;
  @property
  def Num_Reviews(self):
    return self._Num_Reviews;
  @property
  def Avg_Rating(self):
    return self._Avg_Rating;
  @property
  def Tagline(self):
    return self._Tagline;
  @property
  def Genres(self):
    return self._Genres;
  @property
  def Production_Companies(self):
    return self._Production_Companies;
##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn): # count rows in Movies table
  row = datatier.select_one_row(dbConn,"Select count(*) From Movies")
  if(row[0] != None): # check for success 
    return row[0]
  else:
    return -1;


##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn): # get number of reviews from rows in ratings
  row = datatier.select_one_row(dbConn,"Select count(*) from Ratings")
  if(row[0] != None):
    return row[0]
  else:
    return -1;


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  cmd = """Select Movie_ID, Title, strftime('%Y', Release_Date) From Movies 
  where Title like ? 
  order by Title asc""" # get all data required for Movie class from Movies table ordered by Title 
  rows = datatier.select_n_rows(dbConn,cmd,[pattern])
  list = []
  if(rows == None):
    return list;
  for row in rows:
    list.append(Movie(row[0],row[1],row[2])) # putting all Movie class objects into a list
  return list;


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id): # gets all data for Movie Details class for one movie id
  row1 = datatier.select_one_row(dbConn,"Select count(Rating), Avg(Rating) from Ratings where Movie_ID = ?", [movie_id]) # get rating data
  cmd = """Select Movies.Movie_ID, Title, date(Release_Date), Runtime, Original_Language, Budget, Revenue from Movies 
  where Movies.Movie_ID = ? """
  rows = datatier.select_one_row(dbConn,cmd,[movie_id]) # getting data from Movies table
  cmd2 = """Select Company_Name from Movie_Production_Companies join Companies on Movie_Production_Companies.Company_ID = Companies.Company_ID where Movie_Production_Companies.Movie_ID = ? order by Company_Name asc""" # getting all companies data
  rows2 = datatier.select_n_rows(dbConn,cmd2,[movie_id])
  cmd3 = """Select Genre_Name from Movie_Genres join Genres on Movie_Genres.Genre_ID = Genres.Genre_ID where Movie_ID = ? order by Genre_Name asc""" # getting all genres data
  rows3 = datatier.select_n_rows(dbConn,cmd3,[movie_id])
  cmd4 = "Select Tagline from Movie_Taglines where Movie_ID = ?"
  row4 = datatier.select_one_row(dbConn,cmd4,[movie_id]) # getting tagline
  list2 = []
  for row3 in rows3:# these put the genres and companies into a list
    list2.append(row3[0])
  list1 = []
  for row2 in rows2:
    list1.append(row2[0])
  if(len(rows) == 0):
    return None;
  change = []
  if(len(row4) != 0): # checking if there is a tagline
    change.append(row4[0])
  else:
    change.append("")
  if(row1[1] == None): # checks if there are any ratings
    return MovieDetails(rows[0], rows[1], rows[2], rows[3],rows[4],rows[5],rows[6],row1[0],0,change[0],list2,list1)  
  return MovieDetails(rows[0], rows[1], rows[2], rows[3],rows[4],rows[5],rows[6],row1[0],row1[1],change[0],list2,list1);
##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews): 
  cmd = """Select Movies.Movie_ID, Movies.Title, strftime('%Y', Release_Date), count(Rating) as num, Avg(Rating) as ave from  Movies 
  join Ratings on Movies.Movie_ID = Ratings.Movie_ID
  group by Movies.Movie_ID
  Having num >= ?
  order by ave desc
  limit ?""" # getting the top N movies with min_num_reviews reviews
  # using a having statement along side a group by and limit statement
  list = []
  rows = datatier.select_n_rows(dbConn,cmd,[min_num_reviews, N])
  if(rows == None):
    return list; # check if no movies have enough reviews 
  for row in rows: # make MovieRating class for each movie that fits
    list.append(MovieRating(row[0], row[1], row[2], row[3], row[4]))
  return list;

##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
  cmd = "Select Movie_ID from Movies where Movie_ID = ?" # check if movie exists
  row = datatier.select_one_row(dbConn,cmd,[movie_id])
  if(len(row) != 0):
    cmd2 = "Insert into Ratings (Movie_ID, Rating) Values (?, ?)"#attempt to insert new rating into Ratings table
    row1 = datatier.perform_action(dbConn,cmd2,[movie_id, rating])
    if(row1 == -1): # check for success
      return 0;
    else:
      return 1;
  else:
    return 0;
  
  
  


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline): 
  cmd = "Select Movie_ID from Movies where Movie_ID = ?"
  row = datatier.select_one_row(dbConn,cmd,[movie_id]) # check for movies existence
  if(len(row) != 0):
    cmd2 = "Insert into Movie_Taglines (Movie_ID, Tagline) Values (?, ?) ON CONFLICT(Movie_ID) DO UPDATE SET Tagline = excluded.Tagline;"
    # try to add/change tagline for movie using on Conflict Update if tagline already exists otherwise insert normally
    row1 = datatier.perform_action(dbConn,cmd2,[movie_id, tagline])
    if(row1 == -1):# success check
      return 0;
    else:
      return 1;
  else:
    return 0;
