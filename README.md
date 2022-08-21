# Sklearn-based ML model with flask built into docker.

This project provides an example how to develop and
deploy ML model with Flask and Docker.

Here ML-model - Linear Regression. I used toy-dataset Boston to
fit it and make predictions. You may look into
**ML_model_development.ipyng** file to see how it the model was developed.
Saved ML-model's filename on disk - *model_saved.pkl*. 
You may also take a look at file **API_requests_example.ipynb**
to see how model may be uploaded and used. 

In *main.py* there is the code combining flask and the ml-model.

In *requirements.txt* there are all necessary libraries for this project.

## Docker-image creation.

In your OS (for example Ubuntu) with a previously installed docker go to project's folder 
and write:

**docker build -t test_flask .**   (comma is also necessary)

Here **test_flask** - docker-image's name. Actually it is up to you how to name it

There is a docker-file in the project's folder where all required commands for 
creation of a docker-image are specified.

## Docker-container creation.

After you finished with the creation of a docker-image you need to
launch docker-container. Here is an example how to do it:

**docker run  --rm -p 8080:8080 test_flask**
This command forwards docker's port 8080 to your computer's port 8080 so hereby
any requests to your computer's port 8080 would be forwarded to docker's port 8080 and back.


## Interaction with the ml-model

In this project there are 3 implemented methods of client-server interaction.

One of them has been described in **API_requests_example.ipynb**. It requests library 
and get, post methods.

Let's assume that docker-container is running. You will see something like this in your terminal:

 * Serving Flask app 'first_app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. 
Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://172.17.0.2:8080

Press CTRL+C to quit

Thus we can send requests to a docker-container with the address http://172.17.0.2:8080.

After launching container you can use of these three methods to interact wit it.

1) http://172.17.0.2/prediction_var3 - you will be redirected to a
web form where you will be offered to input values required to make a predictin.
2) First of all you have to make a json-request: 
data = {'ZN': 0, 'CHAS': 1, 'RM': 2, 'AGE': 3, 'TAX': 4, 'PTRATIO': 5, 'B': 6} . 
Then you have to put this json into post request and send 
to address http://172.17.0.2/prediction_var2 and get and answer.
For example, you may do it with requests library. More full description 
you may find in file **API_requests_example.ipynb**
3) In your browser go to 
http://192.168.0.101:8080/prediction_var1/< ZN >/< CHAS >/< RM >/< AGE >/< TAX >/< PTRATIO >/< B >, 
enter valid values instead ZN, CHAS, ... and get an output.



