from imdb.Person import Person
import spacy
from spacy.tokenizer import Tokenizer
from imdb import IMDb
from collections import defaultdict
from datetime import date, datetime
from nltk import word_tokenize
import pandas as pd

# create an instance of the IMDb class
ia = IMDb()
nlp = spacy.load('en_core_web_sm')
all_stopwords = nlp.Defaults.stop_words
tokenizer = Tokenizer(nlp.vocab)

def parse_input_string(question):
    doc = nlp(question)
    entity_dict = defaultdict(list)
    for entity in doc.ents:
        entity_dict[entity.label_].append(entity.text)
    return entity_dict

def imdb_actor_search(person_dict, _year):
    try:
        movie_list = []
        for movie in person_dict['filmography']['actor']:
            temp_dict = {}
            if 'year' in movie.keys():
                temp_dict['move_title'] = movie['title']
                temp_dict['year'] = movie['year']
                movie_list.append(temp_dict)
        if _year!=[]:
            movie_year_list = []
            for movie in movie_list:
                if movie['year'] == int(_year[0]):
                    movie_year_list.append(movie)
            return movie_year_list
        else:
            return movie_list[:5]
    except:
        return []

        
def imdb_director_search(person_dict, _year):
    try:
        movie_list = []
        for movie in person_dict['filmography']['director']:
            temp_dict = {}
            if 'year' in movie.keys():
                temp_dict['move_title'] = movie['title']
                temp_dict['year'] = movie['year']
                movie_list.append(temp_dict)
        if _year!=[]:
            movie_year_list = []
            for movie in movie_list:
                if movie['year'] == int(_year[0]):
                    movie_year_list.append(movie)
            return movie_year_list
        else:
            return movie_list[:5]
    except:
        return []

def imdb_birth_year(person_dict):
    temp_dict = {}
    try:
        birth_date = person_dict['birth date']
        d = datetime.strptime(birth_date, '%Y-%m-%d')
        temp_dict['name'] = person_dict['name']
        temp_dict['date'] = d.strftime('%b %d,%Y')
        return [temp_dict]
    except:
        return []

def imdb_movie_search(question, movie_name):
    try:
        temp_dict = {}
        if "direct" in question:
            director = movie_name['directors'][0]['name']
            temp_dict['movie_title'] = movie_name['title']
            temp_dict['director'] = director
            return [temp_dict]
            
        elif "release" in question:
            year = movie_name['year']
            temp_dict['movie_title'] = movie_name['title']
            temp_dict['release year'] = year
            return [temp_dict]
            
        elif "good" in question:
            rating = movie_name['rating']
            temp_dict['movie_title'] = movie_name['title']
            if int(rating) >= 6:
                temp_dict['comments'] = "{} is a good movie and is rated {} on IMDB".format(movie_name['title'], movie_name['rating'])
            else:
                temp_dict['comments'] = "{} is not so good movie and is rated {} on IMDB".format(movie_name['title'], movie_name['rating'])
            return [temp_dict]
            
        elif "kind" in question or "genre" in question:
            genre = movie_name['genre']
            temp_dict['movie_title'] = movie_name['title']
            temp_dict['genre'] = "{} is a {} kind of movie".format(movie_name['title'], " ".join(movie_name['genre']))
            return [temp_dict]
            
        elif "plot" in question or "story" in question:
            plot = movie_name['plot outline']
            temp_dict['movie_title'] = movie_name['title']
            temp_dict['plot'] = "{} is a {} kind of movie".format(movie_name['title'], plot)
            return [temp_dict]
    except:
        return []

def movie_qa(question):
    movie_stop_words = ['genre','story','plot','kind','how','a','good','who', 'is', 'of', 'when', 'film', 'movie', 'directed', 'director', 'acted', 'year', 'the','?', 'was', 'released', 'release', 'In', 'which','did','what']
    entity_dict = parse_input_string(question)
    # for person in entity_dict['PERSON']:
    if entity_dict['PERSON'] != []: 
        if "film" not in question:
            person = entity_dict['PERSON'][0]
            person_ID = ia.search_person(person)[0].personID # only first person because closest search
            person_dict = ia.get_person(person_ID)
            _year = entity_dict['DATE']

            if "act" in question:
                temp_df = pd.DataFrame(imdb_actor_search(person_dict, _year))
                if not temp_df.empty:
                    return temp_df.to_html(index=False, justify='center').replace('\n', '')
            elif "direct" in question:
                temp_df = pd.DataFrame(imdb_director_search(person_dict, _year))
                if not temp_df.empty:
                    return temp_df.to_html(index=False, justify='center').replace('\n', '')
            elif "born" in question:
                temp_df = pd.DataFrame(imdb_birth_year(person_dict))
                if not temp_df.empty:
                    return temp_df.to_html(index=False, justify='center').replace('\n', '')
    else:
        text_tokens = word_tokenize(question)
        tokens_without_sw = [word for word in text_tokens if not word.lower() in movie_stop_words]
        movie_name = " ".join(tokens_without_sw)
        movie_ID = ia.search_movie(movie_name)[0].movieID
        movie_dict = ia.get_movie(str(movie_ID))
        temp_df = pd.DataFrame(imdb_movie_search(question, movie_dict))
        if not temp_df.empty:
            return temp_df.to_html(index=False, justify='center').replace('\n', '')