from flask import Flask, request
from imbd_search import actordirect

app = Flask(__name__)

@app.route('/imdb', methods=["GET"])
def imbd_movie_search():
    if request.method == 'GET':
        print("IMDB movie search api is called")
        input_dict = request.get_json()
        question = input_dict['Question']
        response = actordirect(question) # movies list
        return {"html":response.replace("\n", "")}
        

if __name__ == '__main__':
    app.run(debug=True)