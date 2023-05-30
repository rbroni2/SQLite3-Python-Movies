#Robert Broniarczyk project 2 fall 2022
import sqlite3
import objecttier

def Movie_list_print(list=[]): # prints all data from a list of Movie Class
  i = 0
  while(i < len(list)):
    print(str(list[i].Movie_ID) + " : " + list[i].Title + " ("+str(list[i].Release_Year) +")")
    i = i + 1
def detail_print(data): # prints all data from one Movie Detail object
  print()
  print(str(data.Movie_ID) + " : " + data.Title)
  print(" Release date: " + data.Release_Date)
  print(" Runtime: " + str(data.Runtime) + " (mins)")
  print(" Orig language: " + data.Original_Language)
  print(" Budget: " + f"${data.Budget:,}" + " (USD)")
  print(" Revenue: " + f"${data.Revenue:,}" + " (USD)")
  print(" Num reviews: " + str(data.Num_Reviews))
  average_rating = "{:.2f}".format(data.Avg_Rating)
  print(" Avg rating: " + average_rating + " (0..10)")
  print(" Genres:", end="")
  i = 0
  while(i < len(data.Genres)):
    print(" " + data.Genres[i] +",",end="")
    i = i + 1
  print()
  print(" Production companies: ", end="")
  i = 0
  while(i < len(data.Production_Companies)):
    print(" " + data.Production_Companies[i] +",", end="")
    i = i + 1
  print()
  print(" Tagline: " + data.Tagline)

def rating_print(list = []): # prints list a MovieRating objects
  i = 0
  while(i < len(list)):
    average_rating = "{:.2f}".format(list[i].Avg_Rating)
    print(str(list[i].Movie_ID) + " : " + list[i].Title + " ("+str(list[i].Release_Year) +")" + ", avg rating = " + average_rating +" (" + str(list[i].Num_Reviews)+" reviews)")
    i = i +1;

def general_stats(dbConn): # print general stats and welcome message
  print("** Welcome to the MovieLens app **")
  print()
  print("General stats:")
  print("  # of movies: " + f"{objecttier.num_movies(dbConn):,}")
  print("  # of reviews: " + f"{objecttier.num_reviews(dbConn): ,}")
  print()

dbConn = sqlite3.connect('MovieLens.db')
general_stats(dbConn)
user = input("Please enter a command (1-5, x to exit): ")
while (user.lower() != 'x'):# loop till exit command is given
  print()
  if(user == "1"):
    user1 = input("Enter Movie name (wildcards _ and % supported): ")
    print()
    list1  = []
    list1 = objecttier.get_movies(dbConn, user1)#get list of movies like user input
    print("# of movies found: " + str(len(list1)))
    if(len(list1) <= 100):
      Movie_list_print(list1) # print out all movies data gathered if <= 100 are gathered
    else:
      print("There are too many movies to display, please narrow your search and try again...")
  elif(user == "2"):
    user2 = input("Enter movie id: ")
    data = objecttier.get_movie_details(dbConn, user2)# get all details about 1 movie
    if(data == None):# check if movie id was valid
      print()
      print("No such movie...")
    else:
      detail_print(data)# print gathered movie data
  elif(user == "3"):
    user3 = input("N? ")
    if(user3.isdigit() == False):#checking for valid user inputs
      print("Please enter a positive value for N...")
    else:
      user4 = input("min number of reviews? ")
      if(int(user4) < 1):
        print("Please enter a positive value for min number of reviews...")
      else:
        print()
        list3 = []
        list3 = objecttier.get_top_N_movies(dbConn,int(user3),int(user4))#get N movies with user4 reviews at least
        rating_print(list3)
  elif(user == "4"):
    user5 = input("Enter rating (0..10): ")
    if(int(user5) > 10 or int(user5) < 0):#check for valid rating
      print("Invalid Rating...")
    else:
      user6 = input("Enter movie id: ")
      ret = objecttier.add_review(dbConn,int(user6),int(user5))# add new rating
      print()
      if(ret == 0):# check if add was successful
        print("No such movie...")
      else:
        print("Review successfully inserted")
  elif(user == "5"):
    user7 = input("tagline? ")
    user8 = input("movie id? ")
    val = objecttier.set_tagline(dbConn,user8,user7)# add new tagline
    print()
    if(val == 0):# check if user supplied id was valid or if error occured
      print("No such movie...")
    else:
      print("Tagline successfully set")
  print()
  user = input("Please enter a command (1-5, x to exit): ")
  
  