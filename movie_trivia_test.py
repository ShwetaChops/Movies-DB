"""
HW4: Movie Trivia Test

"""
#Import module
import unittest

#Import the program to be tested
from movie_trivia import *

class Test_Movie_Trivia(unittest.TestCase):

    def test_insert_actor_info_new(self):
        #Define db
        actordb = {'SRK':['K3G', 'K2H2'], 'Salman Khan': ['Dabangg']}
        #Run function
        insert_actor_info('Kajol', ['K2H2', 'K3G', 'DDLJ'], actordb)
        #Ensure new actor is in db
        self.assertIn('Kajol', actordb)
        #Ensure all movies entered for actor, are present in db
        self.assertIn('K2H2', actordb['Kajol'])
        self.assertIn('K3G', actordb['Kajol'])
        self.assertIn('DDLJ', actordb['Kajol'])
        #Ensure the value for newly inserted actor is correct
        self.assertListEqual(['K2H2', 'K3G', 'DDLJ'],actordb['Kajol'], ["Movie list should be exactly the same"])
        #Ensure the length of the list of movies is accurate
        self.assertEqual(len(actordb['Kajol']), 3)
        self.assertNotEqual(len(actordb['Kajol']), 2)

    def test_insert_actor_info_old(self):
        #Define db
        actordb = {'SRK':['K3G', 'K2H2'], 'Salman Khan': ['Dabangg']}
        #Run function
        insert_actor_info('SRK', ['DDLJ', 'Ra1'], actordb)
        #Ensure old actor is in db
        self.assertIn('SRK', actordb)
        #Ensure new movie entered for actor, is present in db
        self.assertIn('Ra1', actordb['SRK'])
        self.assertIn('DDLJ', actordb['SRK'])
        #Ensure old movies already stored, are still present
        self.assertIn('K3G', actordb['SRK'])
        self.assertIn('K2H2', actordb['SRK'])     
        #Ensure the value for newly inserted actor is correct
        self.assertListEqual(['K3G', 'K2H2', 'DDLJ', 'Ra1'], actordb['SRK'], ["Movie list should be exactly the same"])
        #Ensure the length of the list of movies is accurate
        self.assertEqual(len(actordb['SRK']), 4)
        self.assertNotEqual(len(actordb['SRK']), 2)

    def test_insert_rating_new(self):
        #Define db
        ratingsdb = {'K3G': ['80', '81'], 'K2H2': ['90','95'], 'Dabangg': ['5', '0']}
        #Run function
        insert_rating('DDLJ', ['65', '70'], ratingsdb)
        #Ensure movies are in db
        self.assertIn('DDLJ', ratingsdb)
        #Ensure all ratings entered for movie, are present in db
        self.assertIn('65', ratingsdb['DDLJ'])
        self.assertIn('70', ratingsdb['DDLJ'])
        #Ensure the value for newly inserted movie is correct
        self.assertListEqual(['65','70'], ratingsdb['DDLJ'], ["Ratings list should be exactly the same"])
        #Ensure the length of the list of movies is correct
        self.assertTrue(len(ratingsdb['DDLJ']) == 2)
        #Ensure invalid ratings are rejected
        insert_rating('ABCD', ['a', '70'], ratingsdb)
        self.assertFalse('ABCD' in ratingsdb)

        
    def test_insert_rating_old(self):
        #Define db
        ratingsdb = {'K3G': ['80', '81'], 'K2H2': ['90','95'], 'Dabangg': ['5', '0']}
        #Run function
        insert_rating('K3G', ['79', '80'], ratingsdb)
        #Ensure movies are in db
        self.assertIn('K3G', ratingsdb)
        #Ensure the value for already inserted movie is updated correctly
        self.assertNotEqual(['80','81'], ratingsdb['K3G'], ["Ratings list should be exactly the same"])
        self.assertListEqual(['79','80'], ratingsdb['K3G'], ["Ratings list should be exactly the same"])
        #Ensure the length of the list of movies is correct
        self.assertTrue(len(ratingsdb['K3G']) == 2)


    def test_check_element_in_db(self):
        #Define db
        db = {'SRK':['K3G', 'K2H2'], 'Salman Khan': ['Dabangg']}
        #Check both keys and values are present
        self.assertTrue(check_element_in_db('SRK', db))
        self.assertTrue(check_element_in_db('Dabangg', db))
        #Check non-existent values return False
        self.assertFalse(check_element_in_db('Jeopardy', db))
        
    def test_check_key_in_db(self):
        #Define db
        db = {'SRK':['K3G', 'K2H2'], 'Salman Khan': ['Dabangg', 'K2H2']}
        #Check both keys and values are present wih case insensitive inputs
        self.assertEqual('SRK', check_key_in_db('SRK', db))
        self.assertEqual(['SRK', 'Salman Khan'], check_key_in_db('K2h2', db))
        #Check non-existent values return False
        self.assertEqual([], check_key_in_db('ABC', db))

    def test_select_where_actor_is(self):
        #Define db
        actordb = {'SRK':['K3G', 'K2H2'], 'Salman Khan': ['Dabangg']}
        #return correct lists of movies for valid actor
        self.assertEqual(['K3G', 'K2H2'], select_where_actor_is('SRK', actordb))
        #return empty list for actor who is not present in db
        self.assertFalse(select_where_actor_is('MadhUri', actordb))
        #Ensure length of returned list is accurate, case insensitive test
        self.assertTrue(len(select_where_actor_is('SrK', actordb)) == 2)
        self.assertTrue(len(select_where_actor_is('Salman Khan', actordb)) == 1)
        
    def test_select_where_movie_is(self):
        #Define db
        actordb = {'SRK':['K3G', 'K2H2'], 'Salman Khan': ['Dabangg', 'K2H2']}
        #return correct lists of actors for valid movie, case insensitive test
        self.assertListEqual(['SRK', 'Salman Khan'], select_where_movie_is('K2h2', actordb))
        self.assertListEqual(['Salman Khan'], select_where_movie_is('Dabangg', actordb))
        #return False for movie that is not present in db
        self.assertFalse(select_where_movie_is('ABCD', actordb))
        #Ensure length of returned list is accurate
        self.assertTrue(len(select_where_movie_is('K2H2', actordb)) == 2)
        self.assertTrue(len(select_where_movie_is('Dabangg', actordb)) == 1)
        
        
    def test_select_where_rating_is(self):
        #Define db
        ratingsdb = {'K3G': ['30', '51'], 'K2H2': ['90','95'], 'Dabangg': ['5', '0']}
        ratingsdb2 = {}
        #return correct lists of movies for rating condition
        self.assertListEqual(['K3G','Dabangg'], select_where_rating_is('<', '50', True, ratingsdb))
        self.assertListEqual(['K2H2'], select_where_rating_is('>', '90', False, ratingsdb))
        self.assertListEqual(['K3G'], select_where_rating_is('=', '51', False, ratingsdb))
        #return empty list of movies for unsatisfied rating condition
        self.assertListEqual([], select_where_rating_is('>', '90', True, ratingsdb))
        self.assertListEqual([], select_where_rating_is('>', '90', True, ratingsdb2))
        #Return false for incorrect comparison input
        self.assertFalse(select_where_rating_is('less than', '50', True, ratingsdb))
        #Return false for incorrect rating input
        self.assertFalse(select_where_rating_is('=', 'abc', True, ratingsdb))
        #returns same list for two conditions that should return the same list
        self.assertListEqual(select_where_rating_is('>', '80', False, ratingsdb), select_where_rating_is('=', '90', True, ratingsdb))
        #Ensure length of returned list is accurate
        self.assertTrue(len(select_where_rating_is('<', '50', True, ratingsdb)) == 2)
        self.assertFalse(select_where_rating_is("", "", "", ""))
        
    def test_get_co_actors(self):
        #Define db
        actordb = {'SRK':['K3G', 'K2H2', 'DDLJ'],
                   'Salman Khan': ['Dabangg', 'K2H2'],
                   'Kajol':['K2H2', 'DDLJ'],
                   'Rajkumar': ['Newton']
                   }
        #Check if correct actor is present in list
        self.assertTrue('Kajol' in get_co_actors('SRK', actordb))
        #Check if list is returned in proper form
        self.assertListEqual(['Kajol', 'Salman Khan'], get_co_actors('SRK', actordb))
        self.assertListEqual([], get_co_actors('Rajkumar', actordb))
        #Check if invalid actor input returns empty list
        self.assertListEqual([], get_co_actors('ABC', actordb))
        #Check if actors share two movies in common, list doesn't repeat actor name
        self.assertListEqual(['SRK', 'Salman Khan'], get_co_actors('Kajol', actordb))
        
    def test_get_common_movie(self):
        #Define db
        actordb = {'SRK':['K3G', 'K2H2', 'DDLJ'],
                   'Salman Khan': ['Dabangg', 'K2H2'],
                   'Kajol':['K2H2', 'DDLJ'],
                   'Rajkumar': ['Newton']
                   }
        #Ensure correct movie lists are returned
        self.assertListEqual(['K2H2'],get_common_movie('SRK','Salman Khan', actordb))
        self.assertListEqual(['DDLJ', 'K2H2'],get_common_movie('SRK','Kajol', actordb))
        #Ensure empty list returned in case of no common movies
        self.assertListEqual([],get_common_movie('SRK','Rajkumar', actordb))
        #Ensure false is returned in case invalid actors mentioned
        self.assertFalse(get_common_movie('ABC','DEF', actordb))
        #Check if two common movies lists with different actors, are equal
        self.assertListEqual(get_common_movie('Salman Khan','SRK', actordb),get_common_movie('Salman Khan','Kajol', actordb))


    def test_good_movies(self):
        #Define db
        ratingsdb = {'K3G': ['30', '90'], 'K2H2': ['90', '95'], 'Dabangg': ['5', '0']}
        #Ensure correct result is provided
        self.assertEqual({'K2H2'}, good_movies(ratingsdb))
        #Ensure length of returned set is correct
        self.assertEqual(1, len(good_movies(ratingsdb)))
        #Ensure movie where only one of the ratings is above 85, is not included
        self.assertNotIn('K3G', good_movies(ratingsdb))
        self.assertFalse(good_movies(""))

    def test_get_common_actors(self):
        #Define db
        actordb = {'SRK':['K3G', 'K2H2', 'DDLJ'],
                   'Salman Khan': ['Dabangg', 'K2H2'],
                   'Kajol' :['K3G', 'K2H2', 'DDLJ'],
                   'Rajkumar': ['Newton']
                   }
        #Ensure correct movie lists are returned
        self.assertListEqual(['Kajol', 'SRK'], get_common_actors('K2H2', 'DDLJ', actordb))
        self.assertListEqual(['Salman Khan'], get_common_actors('Dabangg','K2H2', actordb))
        #Ensure empty list returned in case of no common movies
        self.assertListEqual([],get_common_actors('Newton','DDLJ', actordb))
        #Ensure empty list return in case invalid actors mentioned
        self.assertFalse(get_common_actors('ABC','DEF', actordb))
        #Check if two common movies lists with different actors, are equal
        self.assertListEqual(get_common_actors('K3G','K2H2', actordb),get_common_actors('K2H2','DDLJ', actordb))


    def test_find_top_rated_actor(self):
        #Define dbs
        actordb = {'SRK':['K3G', 'K2H2', 'DDLJ'],
                   'Salman Khan': ['Dabangg', 'K2H2'],
                   'Kajol':['K3G','K2H2', 'DDLJ'],
                   'Rajkumar': ['Newton']
                   }
        ratingsdb = {'Newton': ['100', '100'],'K3G': ['30', '90'], 'K2H2': ['90', '95'], 'Dabangg': ['5', '0']}
        #Check if correct result is returned
        self.assertEqual('Rajkumar', find_top_rated_actor(actordb, ratingsdb))

    def test_find_lowest_rated_actor(self):
        #Define dbs
        actordb = {'SRK':['K3G', 'K2H2', 'DDLJ'],
                   'Salman Khan': ['Dabangg', 'K2H2'],
                   'Kajol':['K3G','K2H2', 'DDLJ'],
                   'Rajkumar': ['Newton']
                   }
        ratingsdb = {'Newton': ['100', '100'],'K3G': ['30', '90'], 'K2H2': ['90', '95'], 'Dabangg': ['5', '0']}
        #Check if correct result is returned
        self.assertEqual('Salman Khan', find_lowest_rated_actor(actordb, ratingsdb))

    def test_avg_actor_ratings_db(self):
        #Define dbs
        actordb = {'SRK':['K3G', 'K2H2', 'DDLJ'],
                   'Salman Khan': ['Dabangg', 'K2H2'],
                   'Kajol':['K3G','K2H2', 'DDLJ'],
                   'Rajkumar': ['Newton']
                   }
        ratingsdb = {'Newton': ['100', '100'],'K3G': ['30', '90'], 'K2H2': ['90', '95'], 'Dabangg': ['5', '0']}
        #Check if correct result is returned
        self.assertEqual({'SRK': 76.25, 'Salman Khan': 47.5, 'Kajol': 76.25, 'Rajkumar': 100},
                         avg_actor_ratings_db(actordb, ratingsdb))
        #Ensure wrong answer is not returned
        self.assertFalse({'SRK': 51.25, 'Salman Khan': 2.5, 'Kajol': 76.25, 'Rajkumar': 100} == avg_actor_ratings_db(actordb, ratingsdb))
        

    def test_avg_movie_ratings_db(self):
        #Define dbs
        ratingsdb = {'Newton': ['100', '100'],'K3G': ['30', '90'], 'K2H2': ['90', '95'], 'Dabangg': ['5', '0']}
        #Check if correct result is returned
        self.assertEqual({'K3G': 60, 'K2H2': 92.5, 'Dabangg': 2.5, 'Newton': 100},
                         avg_movie_ratings_db(ratingsdb))
        #Ensure wrong answer is not returned
        self.assertFalse({'K3G': 60, 'K2H2': 92.5, 'Dabangg': 25, 'Newton': 100} == avg_movie_ratings_db(ratingsdb))

    def test_find_top_rated_movie(self):
        #Define dbs
        ratingsdb = {'Newton': ['100', '100'],'K3G': ['30', '90'], 'K2H2': ['90', '95'], 'Dabangg': ['5', '0']}
        #Check if correct result is returned
        self.assertEqual('Newton', find_top_rated_movie(ratingsdb))

    def test_find_lowest_rated_movie(self):
        #Define dbs
        ratingsdb = {'Newton': ['100', '100'],'K3G': ['30', '90'], 'K2H2': ['90', '95'], 'Dabangg': ['5', '0']}
        #Check if correct result is returned
        self.assertEqual('Dabangg', find_lowest_rated_movie(ratingsdb))
        
    
unittest.main()


