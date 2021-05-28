#Required Libraries
import sqlite3
import time
import os
from transformers.pipelines import pipeline
from flask import Flask
from flask import request
from flask import jsonify


#Creating the App using Flask
app = Flask(__name__)

#Connecting to the database
db = sqlite3.connect('database.db')
c = db.cursor()
db.execute('DROP TABLE IF EXISTS models')
#Creating Table and inserting details
db.execute("CREATE TABLE models(name TEXT, tokenizer TEXT, model TEXT)")


c.execute("INSERT INTO models VALUES ('distilled-bert','distilbert-base-uncased-distilled-squad','distilbert-base-uncased-distilled-squad')")
c.execute("INSERT INTO models VALUES ('deepset-roberta','deepset/roberta-base-squad2','deepset/roberta-base-squad2')")
db.commit()

#Creating Table for storing Timestamp
c.execute("CREATE TABLE IF NOT EXISTS qa_log(question TEXT, context TEXT, answer TEXT, model TEXT,timestamp REAL)")

#Models

@app.route('/models', methods=['GET','PUT','DELETE'])
def methods_for_models():
   
    if  request.method =='GET':
        db  =  sqlite3.connect('database.db')
        cursor  =  db.cursor()
        cursor.execute('''SELECT name,tokenizer,model  FROM models''')
        myresult = cursor.fetchall()
        li_model=[]
        for i in range(0,len(myresult)):
            record = {"name": myresult[i][0] ,"tokenizer":myresult[i][1]  ,"model": myresult[i][2] }
            li_model.append(record)
        return jsonify(li_model)

    elif request.method == 'PUT':
        db = sqlite3.connect('database.db')
        c = db.cursor()
       

        data = request.json
        name = data['name']
        tokenizer = data['tokenizer']
        model = data['model']
       
#Adding new row into the model
        c.execute("INSERT INTO models (name, tokenizer, model) VALUES (?, ?, ?)", (name, tokenizer, model))
        db.commit()
#Retrieving models from database
        c.execute("SELECT name,tokenizer,model FROM models")
        #Storing Results of the query in a list
        myresult = c.fetchall()
        li_model = []
#Storing the Result in JSON
        for i in range(0,len(myresult)):
            record = {"name": myresult[i][0] ,"tokenizer":myresult[i][1]  ,"model": myresult[i][2]}
            li_model.append(record)
        return jsonify(li_model)
   
    elif request.method == 'DELETE':
        db = sqlite3.connect("database.db")
        c = db.cursor()
#Getting details of the model to be deleted in the Table
        modelname = request.args.get('model',None)
        #Deleting row
        c.execute("DELETE FROM models WHERE name = ?", (modelname,))
        db.commit()
#Query to retrieve models from database
        c.execute("SELECT name,tokenizer,model FROM models")
        myresult = c.fetchall()
#Storing the Result in JSON
        li_model = []
        for i in range(0,len(myresult)):
            record = {"name": myresult[i][0] ,"tokenizer":myresult[i][1]  ,"model": myresult[i][2]}
            li_model.append(record)
        return jsonify(li_model)

#Answers

@app.route("/answer", methods = ['GET','POST'])
def methods_for_answers():
   
    if  request.method =='POST':
        model_name = request.args.get('model', None)
        data = request.json
#Default model when no model is specified
        if not model_name:
            model_name='distilled-bert'    
        db = sqlite3.connect('database.db')
        c = db.cursor()
#Query to retireve information of that particular model
        c.execute("SELECT DISTINCT name,tokenizer,model FROM models WHERE name=?",(model_name,))
        myresult = c.fetchall()
       
        row= myresult[0]
        name = row[0]
        tokenizer = row[1]
        model = row[2]
   
#Implementing Model
        hg_comp = pipeline('question-answering', model=model, tokenizer=tokenizer)

# Answering the Question
        answer = hg_comp({'question': data['question'], 'context': data['context']})['answer']

#Generating Timestamp
        ts = time.time()

#Inserting entry into qa_log table
        c.execute("CREATE TABLE IF NOT EXISTS qa_log(question TEXT, context TEXT, answer TEXT, model TEXT,timestamp REAL)")
        c.execute("INSERT INTO qa_log VALUES(?,?,?,?,?)", (data['question'], data['context'],answer, model_name,ts))
        db.commit()


        c.close()
        db.close()

#JSON to return Output
        output = {
        "timestamp": ts,
        "model": model_name,
        "answer": answer,
        "question": data['question'],
        "context": data['context']}  
        return jsonify(output)

    if request.method == 'GET':
        name= request.args.get('model')
        start= request.args.get('start')
        end= request.args.get('end')
        db = sqlite3.connect('database.db')
        c = db.cursor()
        if name:
            c.execute('SELECT * FROM qa_log WHERE model=? AND timestamp >=? AND timestamp <=?',(name,start,end))
            model = c.fetchall()
            output=[]
            for row in model:
              record = {"timestamp": row[4],
                        "model":row[3],
                        "answer": row[2],
                        "question": row[0],
                        "context": row[1]}
              output.append(record)
            return jsonify(output)
        else:
            c.execute('SELECT * FROM qa_log WHERE timestamp >=? AND timestamp <=?',(start,end))
            model = c.fetchall()
            output=[]
            for row in model:
              record = {"timestamp": row[4],
                        "model":row[3],
                        "answer": row[2],
                        "question": row[0],
                        "context": row[1]}
              output.append(record)
            return jsonify(output)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), threaded=True)
    
