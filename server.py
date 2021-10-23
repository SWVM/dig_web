###########################
TEMP_IN = "/dig_web-master/temp/trace/{}.csv"
TEMP_OUT= "/dig_web-master/temp/out/{}.txt"
PYTHON  = "/root/miniconda3/bin/python"
PYTHON_FLAG = "-O"
DIG     = "/dig/src/dig.py"
DIG_FLAG= "-log"
DIG_NUM = "4"


###########################
import queue
import re
import subprocess
from uuid import uuid4
from flask import Flask, redirect, url_for, request, render_template
from flask.helpers import make_response, send_from_directory
import json

from time import sleep
from threading  import Thread
from queue import Queue


class Trace():
   def __init__(self, id, input):
      self.id = id
      self.done = False
      self.input_gen(input)
   def get_input_fp(self):
      return TEMP_IN.format(self.id)
   def get_output_fp(self):
      return TEMP_OUT.format(self.id)
   def input_gen(self, content):
      f = open( self.get_input_fp() , "w+")
      f.write(content)
      f.close()
   def retrive_result(self):
      result = "No result found"
      if self.done:
         f = open( self.get_output_fp() , "r")
         result = f.read()
         f.close()
      return result
   def run(self):
      command = [PYTHON, PYTHON_FLAG, DIG, self.get_input_fp(), DIG_FLAG, DIG_NUM, ">", self.get_output_fp()]
      subprocess.run( command )
      self.done = True 
      print("Done..."+self.id)

class Runner():
   def __init__(self):
      self.task_queue      = Queue()
      self.result_queue    = Queue()
      self.result_hash     = {}
      p = Thread(target=self.fire_thread)
      p.start()
      print("dig runner started...")

   def fire_thread(self):
      while True:
         task = self.task_queue.get() # blocked if queue is empty
         task.run()
         self.result_queue.put(task)
         self.result_hash[task.id] = task
   def add(self, tsk):
      self.task_queue.put(tsk)
   def get(self, id):
      return self.result_hash.get(id)

dig = Runner()


app = Flask(__name__)

@app.route('/dig', methods = ['POST', 'GET'])
def dig_main():
   if request.method == "GET":
      # return the form
      return render_template("index.html")
   elif request.method == "POST":
      id     = str(uuid4())
      str_in = request.data.decode("utf-8")
      task   = Trace(id, str_in)

      dig.add(task)

      return json.dumps(str(uuid4()))


@app.route('/dig/<id>')
def get_res(id):
   task = dig.get(id)
   return task.retrive_result()


if __name__ == '__main__':
   app.run(debug = True, port=80, host="0.0.0.0")
   