from flask import Flask, request
from imbd_search import movie_qa

app = Flask(__name__)


# IMDB search api
@app.route('/imdb', methods=["GET"])
def imbd_movie_search():
    if request.method == 'GET':
        print("IMDB movie search api is called")
        input_dict = request.get_json()
        question = input_dict['Question']
        response = movie_qa(question) # movies list
        # return {"answer": response}
        return {
                "status": 200,
                "message": "Fetched information successfully.",
                "code": 200,
                "data": response
            }
        
        

if __name__ == '__main__':
    app.run(debug=True)