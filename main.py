import flask
import csv
import os.path

from flask.json import jsonify
import mysql.connector
from datetime import datetime
#Hardcoded data
data = {"workers": [{"worker_id": 1, "worker_name": "1", "cpu_usage": 3, "ram_usage": "1%", "vmem_usage": "0%", "gpu": "GeForce RTX 2070", "gpu_used": "used"}, {"worker_id": 2, "worker_name": "2", "cpu_usage": 3, "ram_usage": "3%", "vmem_usage": "43%", "gpu": "GeForce RTX 2080 TI", "gpu_used": "not used"}, {"worker_id": 3, "worker_name": "3", "cpu_usage": 16, "ram_usage": "13%", "vmem_usage": "10%", "gpu": "GeForce GTX 1080", "gpu_used": "not used"}]}

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#Insert record function, takes a success and error parameter with defaults to success and 0 errors
def insertRecord(success="success", errors=0):
  now = datetime.now()
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="nebula_exam"
  )
  mycursor = mydb.cursor()

  mycursor.execute("SELECT * FROM `api_requests`")
  mycursor.fetchall()
  rc = mycursor.rowcount
  
  sql = "INSERT INTO api_requests (admin_id, call_date, call_time, result, error_counts) VALUES (%s, %s, %s, %s, %s)"
  values = ("admin_" + str(rc + 1), now.strftime("%Y-%m-%d"), now.time(), success , errors)
  #insert the values into the database
  mycursor.execute(sql, values)

  mydb.commit()
  print(mycursor.rowcount, "record inserted.")

  mycursor.close()
  mydb.close()


#Create a CSV function
def createCSV(request):
  
  file_exists = os.path.isfile("requests.csv")
  with open("requests.csv", mode ="a") as file:
    fieldnames = ["payload data", "source ip"]
    writer = csv.DictWriter(file, delimiter=",", lineterminator='\n', fieldnames=fieldnames)
    if not file_exists:
      writer.writeheader()
    
    writer.writerow({'payload data': request.data.decode('UTF-8'), "source ip": request.remote_addr})



#API routes
@app.route('/api/workers/all', methods=['GET'])
def api_all():
    
    insertRecord()
    createCSV(flask.request)
    return jsonify(data)


@app.route('/api/workers', methods=['GET'])
#if querying with an ID, check if it's there, if not error out and insert a failed record
def api_id():
    if 'id' in flask.request.args:
        id = int(flask.request.args['id'])
        insertRecord()
    else:
        insertRecord("failed", 1)
        return "Error: No id field provided. Please specify an id."

    results = []

    for worker in data["workers"]:
        if worker['worker_id'] == id:
            results.append(worker)
    #call createCSV function
    createCSV(flask.request)
    return jsonify(results)

@app.route('/api/gpu', methods=['GET'])
def api_gpu():
    if 'used' in flask.request.args:
        used = flask.request.args['used']
        insertRecord()
    else:
        insertRecord("failed", 1)
        return "Error: No used field provided. Please specify true or false."

    results = []

    gpu_used = "used" if used == "true" else "not used"

    for worker in data["workers"]:
        if worker['gpu_used'] == gpu_used:
            results.append(worker)
    
    createCSV(flask.request)
    return jsonify(results)

app.run()
