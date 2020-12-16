import spacy
from imdb import IMDb
from collections import defaultdict
import pandas as pd

# create an instance of the IMDb class
ia = IMDb()

nlp = spacy.load('en_core_web_sm')

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
        
def actordirect(question):
    entity_dict = parse_input_string(question)
    # for person in entity_dict['PERSON']:
    person = entity_dict['PERSON'][0]
    person_ID = ia.search_person(person)[0].personID # only first person because closest search
    person_dict = ia.get_person(person_ID)
    _year = entity_dict['DATE']
    
    if "act" in question:
        actor_dict = pd.DataFrame(imdb_actor_search(person_dict, _year))
        return actor_dict.to_html(index=False, justify='center')

    elif "direct" in question:
        director_dict = pd.DataFrame(imdb_director_search(person_dict, _year))
        return director_dict.to_html(index=False, justify='center')