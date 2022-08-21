import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle
import json
import pipeline_funcs

app = Flask("first_app", template_folder="template")

filename = "model_saved.pkl"
with open(filename, "rb") as file:
    Pickled_ML_Model = pickle.load(file)



@app.route("/prediction_var3")
def home():
    return render_template("prediction.html")


def prepr_input(values: list) -> pd.DataFrame:
    columns = ["ZN", "CHAS", "RM", "AGE", "TAX", "PTRATIO", "B"]
    n = len(columns)
    inputs = {columns[i]: [values[i]] for i in range(n)}
    inputs = pd.DataFrame.from_dict(inputs)
    return inputs


@app.route("/prediction_var3", methods=["POST"])
def make_prediction3():
    # obtain all form values and insert them into an array, convert into integers
    try:
        values = list(request.form.values())
        inputs = prepr_input(values)
        prediction = Pickled_ML_Model.predict(inputs)
        prediction = round(prediction[0], 2)
        prediction = "Predicted value is {}".format(prediction)
    except:
        prediction = "Incorrect input, please enter valid values"
    # predict the price given the values inputted by user
    # Round the output to 2 decimal places
    return render_template("prediction.html", prediction_text=prediction)


@app.route("/prediction_var2", methods=["POST"])
def make_prediction2():
    # get data
    data = request.get_json(force=True)
    try:
        data = {x: [float(y)] for x, y in data.items()}
        data = pd.DataFrame.from_dict(data)
        model_answer = Pickled_ML_Model.predict(data)
        json_dump = json.dumps({"answer": model_answer.tolist()[0]})
    except:
        json_dump = "Incorrect input"
    return json_dump


@app.route(
    "/prediction_var1/<zn>/<chas>/<rm>/<age>/<tax>/<ptratio>/<b>", methods=["GET"]
)
def make_prediction1(zn, chas, rm, age, tax, ptratio, b):
    try:
        values = [zn, chas, rm, age, tax, ptratio, b]
        inputs = prepr_input(values)
        model_answer = Pickled_ML_Model.predict(inputs)
        model_answer = model_answer[0]
        json_dump = json.dumps({"answer": model_answer})
    except:
        json_dump = "Incorrect input"
    return json_dump


@app.route("/", methods=["GET"])
def hello_world():
    return (
        " Let's suppose server running on http://192.168.0.101:8080. <br> "
        "In browser there are 2 methods to get prediction <br>  "
        "http://192.168.0.101:8080\prediction_var3 - will redirect you to the html form where you can fill all r <br>"
        "required fields and get answer <br> "
        "http://192.168.0.101:8080/prediction_var1/< ZN >/< CHAS >/< RM >/< AGE >/< TAX >/< PTRATIO >/< B >. <br>"
        "Here instead ZN, CHAS and so on you should input proper values <br>"
    )


if __name__ == "__main__":
    # app.run(debug=False)
    # we need set host ="0.0.0.0" to make our flask app visible  out of the docker container
    app.run(debug=False, host="0.0.0.0", port=8080)
