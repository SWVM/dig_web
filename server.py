import re
from uuid import uuid4
from flask import Flask, redirect, url_for, request, render_template
from flask.helpers import make_response, send_from_directory

app = Flask(__name__)

@app.route('/dig', methods = ['POST', 'GET'])
def dig_main():
   if request.method == "GET":
      # return the form
      return render_template("index.html")
   elif request.method == "POST":
      f = open("/dig_web-master/temp/trace.csv", "w+")
      f.write(request.data.decode("utf-8"))
      f.close()

      return str(uuid4())


if __name__ == '__main__':
   app.run(debug = True, port=80, host="0.0.0.0")
   