import json
import main
from flask import Flask, request
from jinja2 import Environment, PackageLoader, select_autoescape


app = Flask(__name__)

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

@app.route('/<year>/<month>', methods=['GET'])
def summarize(year, month):
    
    summarized_data = main.summarize(year, month)
   
    template = env.get_template('index.html')
    return template.render(data=summarized_data)

@app.route("/count/<year>")
def count(year):
    return main.count(year)

@app.route("/")
def index():
    template = env.get_template('index.html')
    return template.render()
   
if __name__ == "__main__":
    app.run(debug=True)