"""
HW4: Movie Trivia

This homework deals with the following topics:
- Dictionaries
- Sets
- Databases using dictionaries (not too far from how they really work!)
- Test driven development (TDD)

In this HW, we will deal with representing movie data using dictionaries,
with the goal of answering some simple movie trivia questions. For example,
“what is the name of the movie that both Tom Hanks and Leonardo DiCaprio
acted in?”

We will use 2 dictionaries. The first corresponds to information about
an actor and all the movies that he/she has acted in.  The second
corresponds to information about the critics’ score and the audience
score from https://www.rottentomatoes.com/, about the movies.  

Given that information, we will then want to answer some typical movie
trivia questions.

"""

#Use these first 2 functions to create your 2 dictionaries
import csv
def create_actors_DB(actor_file):
    """
    Creates a dictionary keyed on actors from a text file.
    """
    
    f = open(actor_file)
    movieInfo = {}
    for line in f:
        line = line.rstrip().lstrip()
        actorAndMovies = line.split(',')
        actor = actorAndMovies[0]
        movies = [x.lstrip().rstrip() for x in actorAndMovies[1:]]
        movieInfo[actor] = movies
    f.close()
    
    return movieInfo

def create_ratings_DB(ratings_file):
    """
    Makes a dictionary from the rotten tomatoes csv file.
    """
    
    scores_dict = {}
    with open(ratings_file, 'r', encoding = 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        reader.__next__()
        for row in reader:
            scores_dict[row[0]] = [row[1], row[2]]
            
    return scores_dict


def insert_actor_info(actor, movies, actordb):
    """Function that adds actor related information to the actor database"""
    actor = actor.strip()
    #If actor is already in the database
    movies = [m.strip() for m in movies]
    
    if check_element_in_db(actor, actordb):
        for i in movies:
            #If movie is not already part of the list, then add it
            if i not in actordb[actor]:
                actordb[actor].append(i)
    else:
        #If actor is not in the database, then add actor along with movie list
        actordb[actor] = movies


def insert_rating(movie, ratings, ratingsdb):
    """Function that adds movie rating info to the ratings db"""
    movie = movie.strip()
    #If movie is not in db, add it, if it is already there - replace its ratings
    if len(ratings) == 2:
        try:
            int(ratings[0])
            try:
                int(ratings[1])
                ratingsdb[movie] = ratings
            except:
               print("Invalid ratings provided\n") 
        except:
            print("Invalid ratings provided\n")
    else:
        return False

def select_where_actor_is(actor_name, actordb):
    """Function that takes an actors name as input, and outputs a list of movies for that actor"""
    #if actor in in db, return movie list
    if check_element_in_db(actor_name, actordb):
        return actordb[check_key_in_db(actor_name, actordb)]
    else:
        #if actor is not in db, return False
        return False


def select_where_movie_is(movie_name, actordb):
    """Function that given the name of a movie, returns a list of all actors in the movie"""
    if check_element_in_db(movie_name, actordb):
        return check_key_in_db(movie_name, actordb)
    else:
        #if movie is not in db, return False
        return False

def select_where_rating_is(comparison, targeted_rating, is_critic, ratingsdb):
    """Function that returns a list of movies that satisfy an particular condition on ratings"""
    #create empty movie list
    movie_list = []
    try:
        #convert rating input to int
        targeted_rating = int(targeted_rating)
        #check if valid comparison requested
        if comparison == '=' or comparison == '>' or comparison == '<':
            for i in ratingsdb:
                #add movies to movie list based on the conditions specified
                if comparison == '=':
                    if is_critic and int(ratingsdb[i][0]) == targeted_rating:
                        movie_list.append(i)
                    elif (is_critic is False) and int(ratingsdb[i][1]) == targeted_rating:
                        movie_list.append(i)
                elif comparison == '>':
                    if is_critic and int(ratingsdb[i][0]) > targeted_rating:
                        movie_list.append(i)
                    elif (is_critic is False) and int(ratingsdb[i][1]) > targeted_rating:
                        movie_list.append(i)
                elif comparison == '<':
                    if is_critic and int(ratingsdb[i][0]) < targeted_rating:
                        movie_list.append(i)
                    elif (is_critic is False) and int(ratingsdb[i][1]) < targeted_rating:
                        movie_list.append(i)
            return movie_list
        else:
            #Print error message
            print("Sorry, only =, <, or > comparisons are possible\n")
            return False
    except:
        #Print error message
        print("Sorry, the comparison rating must be an integer\n")
        return False


##FUN FUNCTIONS!

def get_co_actors(actor_name, actor_db):
    """Function that returns a list of all actors that a given actor has worked with"""
    co_actor_list = []
    #if actor exists in db
    if check_element_in_db(actor_name, actor_db):
        #look at list of movies, and find other actors in those movies
        for i in select_where_actor_is(actor_name, actor_db):
            for j in range(len(select_where_movie_is(i, actor_db))):
                co_actors = select_where_movie_is(i, actor_db)[j]
                #return list of actors in those movies, besides the input actor
                if co_actors not in co_actor_list and co_actors.lower() != actor_name.lower():
                    co_actor_list.append(co_actors)
    return sorted(co_actor_list)
                    
def get_common_movie(actor1, actor2, actor_db):
    """Function that returns a list of movies in which both actors were cast together"""
    if check_element_in_db(actor1, actor_db) and check_element_in_db(actor2, actor_db):
        return sorted(list(set(select_where_actor_is(actor1, actor_db)).intersection(set(select_where_actor_is(actor2, actor_db)))))
    else:
        return False

def good_movies(ratingsdb):
    """Function that returns the set of movies that both critics and audiences
    have rated greater that or equal to 85"""
    critic_greater_than_85 = set(select_where_rating_is('>', '85', True, ratingsdb))
    critic_equal_to_85 = set(select_where_rating_is('=', '85', True, ratingsdb))
    audience_greater_than_85 = set(select_where_rating_is('>', '85', False, ratingsdb))
    audience_equal_to_85 = set(select_where_rating_is('=', '85', False, ratingsdb))
    
    critic_good_movies_set = critic_greater_than_85.union(critic_equal_to_85)
    audience_good_movies_set = audience_greater_than_85.union(audience_equal_to_85)
    good_movies_set = critic_good_movies_set.intersection(audience_good_movies_set)
    return good_movies_set

def get_common_actors(movie1, movie2, actor_db):
    """Function that returns a list of actors that acted in both movies"""
    if check_element_in_db(movie1, actor_db) and check_element_in_db(movie2, actor_db):
        movie1_actors_set = set(select_where_movie_is(movie1, actor_db))
        movie2_actors_set = set(select_where_movie_is(movie2, actor_db))
        common_actors_set = movie1_actors_set.intersection(movie2_actors_set)
        common_actors_list = sorted(list(common_actors_set))
        return common_actors_list
    else:
        return False

## EXTRA FUNCTIONS TO PROVIDE USER FUNCTIONALITY

def find_top_rated_actor(actordb, ratingsdb):
    """Function that returns the top rated actor in the database"""
    avg_db = avg_actor_ratings_db(actordb, ratingsdb)
    keys = list(avg_db.keys())
    values = list(avg_db.values())
    #Find actor with maximum avg rating
    index = values.index(max(values))
    return keys[index]

def find_lowest_rated_actor(actordb, ratingsdb):
    """Function that returns the lowest rated actor in the database"""
    avg_db = avg_actor_ratings_db(actordb, ratingsdb)
    keys = list(avg_db.keys())
    values = list(avg_db.values())
    #Find actor with minimum avg rating
    index = values.index(min(values))
    return keys[index]


def find_top_rated_movie(ratingsdb):
    """Function that returns the top rated movie in the database"""
    avg_db = avg_movie_ratings_db(ratingsdb)
    keys = list(avg_db.keys())
    values = list(avg_db.values())
    #Find movie with maximum avg rating
    index = values.index(max(values))
    return keys[index]
    
def find_lowest_rated_movie(ratingsdb):
    """Function that returns the lowest rated movie in the database"""
    avg_db = avg_movie_ratings_db(ratingsdb)
    keys = list(avg_db.keys())
    values = list(avg_db.values())
    #Find movie with minimum avg rating
    index = values.index(min(values))
    return keys[index]
          

##HELPER FUNCTIONS

def avg_actor_ratings_db(actordb, ratingsdb):
    """Function that returns a db with avg ratings for actors"""
    actor_list = list(actordb.keys())
    movie_list = list(actordb.values())
    avg_rating_db = avg_movie_ratings_db(ratingsdb)
    new_values_list = []
    #Using avg movie ratings db, calculates an avg rating for each actor
    for movie_group in movie_list:
        sum_rating = 0
        counter = 0
        for movie in movie_group:
            if movie in avg_rating_db:
                sum_rating += float(avg_rating_db.get(movie))
                counter += 1
        if counter > 0:
            avg_rating = sum_rating/counter
        else:
            #considers average rating of 0 for actors who's movie ratings are not in the db
            avg_rating = 0
        new_values_list.append(avg_rating)

    new_actor_ratings_db = dict(zip(actor_list, new_values_list))
    return new_actor_ratings_db
        


def avg_movie_ratings_db(ratingsdb):
    """Function that returns a db with avg ratings for movies"""
    keys_list = list(ratingsdb.keys())
    values_list = list(ratingsdb.values())
    new_values_list = []
    #Calculate the avg of a movies ratings and add to new values list
    for val in values_list:
        avg_rating = (int(val[0]) + int(val[1])) / 2
        new_values_list.append(avg_rating)
    new_ratingsdb = dict(zip(keys_list, new_values_list))
    #Return the new db with integer values for avg movie ratings
    return new_ratingsdb

def check_element_in_db(element, db):
    """Function that returns True if element is a key/value element in the db, else False"""
    element = element.strip()
    keys = list(db.keys())
    values = list(db.values())
    #If element is a key in the db, return true
    for key in keys:
        if element.lower() == key.lower():
            return True
    #If element is a part of any value list in the db, return true
    for val in values:
        for i in val:   
            if element.lower() == i.lower():
                return True
    return False

def check_key_in_db(element,db):
    """Function that returns all the reference key/s corresponding to an element (actor/movie) in a db"""
    element = element.strip()
    keys = list(db.keys())
    values = list(db.values())
    #Check key value for entered element
    for key in keys:
        if element.lower() == key.lower():
            return key

    actor_keys_list = []
    #Check key value for entered value element
    for index in range(len(values)):
        for i in values[index]:   
            if element.lower() == i.lower():
                if keys[index] not in actor_keys_list:
                    actor_keys_list.append(keys[index])
    return actor_keys_list


## MAIN FUNCTION
    
def main():
    actor_DB = create_actors_DB('moviedata.txt')
    ratings_DB = create_ratings_DB('movieratings.csv')

    #Welcome user and explain the db
    print("Welcome! This database contains information about actors and movie ratings.\n")

    #While the user chooses not to quit, show possible options
    quit_program = False
    while quit_program == False:
        print(" #INSERT DATA#\n",
              "Enter 1 to add actors and their movies to the database\n",
              "Enter 2 to add movies and their ratings to the database\n",
              "\n",
              "#ASK A QUESTION#\n",
              "Enter 3 to find out all co-actors of an actor\n",
              "Enter 4 to find the common movies of two actors\n",
              "Enter 5 to find out movies with a rating of 85+ from both critics and audiences\n",
              "Enter 6 to find out the common actors in two movies\n",
              "Enter 7 to find out all the movies for a particular actor\n",
              "Enter 8 to find out all the actors in a particular movie\n",
              "Enter 9 to find all movies that satisfy a certain condition on rating out of 100\n",
              "\n",
              "#BEST AND WORST#\n",
              "Enter 10 to find out the top rated movie\n",
              "Enter 11 to find out the lowest rated movie\n",
              "Enter 12 to find out the top rated actor\n",
              "Enter 13 to find out the lowest rated actor\n",
              "Enter 'quit' to Exit\n",
              "\n")
        
        user_input = input("Enter option: ").lower().strip()
        
        if user_input == 'quit':
            quit_program = True

        elif user_input == '1':
            #Take user input for actor and movies to add to db
            actor = input("Enter actor name: ")
            movie = input("Enter movies separated by a comma (','): ")
            movie = movie.split(',')
            insert_actor_info(actor,movie, actor_DB)

        elif user_input == '2':
            #Take user input for movie and ratings to add to db
            movie = input("Enter movie name: ")
            critic_rating = input("Enter critic rating: ")
            audience_rating = input("Enter audience rating: ")
            insert_rating(movie, [critic_rating, audience_rating], ratings_DB)
            
        elif user_input == '3':
            #Proceed to take user actor input and find all co-actors
            actor_input = input("Enter actor name: ").lower().strip()
            if check_element_in_db(actor_input, actor_DB):
                print(get_co_actors(actor_input, actor_DB))
            else:
                print("Not Present in the DB\n")
            
        elif user_input == '4':
            #Take input of 2 actors and find common movies
            actor_input_1 = input("Enter actor 1 name: ").lower().strip()
            actor_input_2 = input("Enter actor 2 name: ").lower().strip()
            if check_element_in_db(actor_input_1, actor_DB) and check_element_in_db(actor_input_2, actor_DB):
                print(get_common_movie(actor_input_1, actor_input_2, actor_DB))
            elif check_element_in_db(actor_input_1, actor_DB) is False and check_element_in_db(actor_input_2, actor_DB) is False:
                print("Both these actors are Not Present\n")
            elif check_element_in_db(actor_input_1, actor_DB) is False:
                print("Actor 1 is Not Present in the DB\n")
            else:
                print("Actor 2 is Not Present in the DB\n")


        elif user_input == '5':
            #List movies with 85+ ratings
            print(good_movies(ratings_DB))

        elif user_input == '6':
            #Take user input of 2 movies and provide list of common actors
            movie_input_1 = input("Enter movie 1 name: ").lower().strip()
            movie_input_2 = input("Enter movie 2 name: ").lower().strip()
            if check_element_in_db(movie_input_1, actor_DB) and check_element_in_db(movie_input_2, actor_DB):
                print(get_common_actors(movie_input_1, movie_input_2, actor_DB))
            elif check_element_in_db(movie_input_1, actor_DB) is False and check_element_in_db(movie_input_2, actor_DB) is False:
                print("Both these movies are Not Present in the Actor DB\n")
            elif check_element_in_db(movie_input_1, actor_DB) is False:
                print("Movie 1 is Not Present in Actor DB\n")
            else:
                print("Movie 2 is Not Present in Actor DB\n")


        elif user_input == '7':
            #Print the list of all movies for an actor
            actor_input = input("Enter actor name: ").lower().strip()
            if check_element_in_db(actor_input, actor_DB):
                print(select_where_actor_is(actor_input, actor_DB))
            else:
                print("Not Present in Actor DB\n")

        elif user_input == '8':
            #Print all actors in a given movie
            movie_input = input("Enter movie name: ").lower().strip()
            if check_element_in_db(movie_input, actor_DB):
                print(select_where_movie_is(movie_input, actor_DB))
            else:
                print("Not Present in Actor DB\n")

        elif user_input == '9':
            #Take rating and comparison input from user
            comparison_input = input("Pick between <, > or = : ").strip()
            rating_input = input("Pick a rating from 0 to 100 to compare with: ").strip()
            critic_input = input("Enter 'Critic' or 'Audience' - which rating is to be considered: ").lower().strip()
            if critic_input == 'critic':
                if select_where_rating_is(comparison_input, rating_input, True, ratings_DB) is not False:
                    print(select_where_rating_is(comparison_input, rating_input, True, ratings_DB))
            elif critic_input == 'audience':
                if select_where_rating_is(comparison_input, rating_input, False, ratings_DB) is not False:
                    print(select_where_rating_is(comparison_input, rating_input, False, ratings_DB))
            else:
                print("Sorry you must enter valid parameters!")

        elif user_input == '10':
            #Proceed to find out top rated movie
            print(find_top_rated_movie(ratings_DB))

        elif user_input == '11':
            #Proceed to find out lowest rated movie
            print(find_lowest_rated_movie(ratings_DB))
            
        elif user_input == '12':
            #Proceed to find out the top rated actor
            print(find_top_rated_actor(actor_DB, ratings_DB))

        elif user_input == '13':
            #Proceed to find out the lowest rated actor
            print(find_lowest_rated_actor(actor_DB, ratings_DB))

        print("\n\n")
        
if __name__ == '__main__':
    main()
