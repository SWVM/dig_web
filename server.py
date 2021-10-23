import re
from flask import Flask, redirect, url_for, request, render_template
from flask.helpers import make_response, send_from_directory

app = Flask(__name__)

@app.route('/dig', methods = ['POST', 'GET'])
def instructor_join():
   if request.method == "GET":
      # return the form
      return render_template("index.html")
   elif request.method == "POST":
      f = open("./temp/trace.csv", "w+")
      f.write(request.data)
      f.close()
      return request.data


if __name__ == '__main__':
   app.run(debug = True, port=80, host="0.0.0.0")
   