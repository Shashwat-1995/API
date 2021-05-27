# API
This project aims to form a question Answering API with multiple extra facilitation. 


## Available routes
There are 5 different routes which are facilitating in their own way. They are providing multiple functionalities.They are:

## General Information about API
### The general idea behind the API
A Question Answering API which basically tries to answer the question after reading the provided context. It also provides option to choose the model of choice to get answer for the question. Other functions include knowing the present models and the answers provided by them with timestamp.

The main pain point that this API addresses is to provide answer for a question after reading the context provided with question as input. So it uses pre trained models which take a question and a context as an input then based on that context, models try to find answer for the question.

Apart from this, API provides few other functionaloities to facilitate the question answering process. there are different handlers for these processes. The routes for these are mentioned above under the section important routes.  First route is to get the name of all the available models at present. Second routes is used to enter a new model in the available lists of model. Once API receives PUT request to this handler, the name of model is extracted from request and that particular model is made available to use in future. Third route is to delete a model from API. It extracts the name of model from DELETE request and deletes that particular model. Fourth route is the most important route. It answers the question on basis of context. It takes a post request and extract the Question and context from the body of request. An option is also there to choose the model. In this case API will use the same model to answer the question. If no model name is given then API uses the default model and predict the answer. Once the answer is predicte and returned to client, the question, context, answer , name of the model used and time stamp is noted to maintain the record of past data. Fifth funtionality is to provide the history of Questions answered . It provides an option to select a specific model and know the details of its activity. In this case the name of model is extracted and activity of that model is returned. That is the question , context and answer along with time stamp of answering is returned. There is also option to select time frame . the start and the end time frame if selected, the API returns the records between that provided window. If there is no start and end time , API returns the records of all the instance wher a model was used to answetr a qyestion.In same way if the model name is not provided in request, the record for all models are returned.

### Where the API can be located (the base URL)

## How to build and run the API locally via Docker or Flask
The most important step in building an API is to build an optimum robest code. The code consist of two basic parts. One is related to launching the API. Second is to identify functionalities and build the respective handlers.

### Launching the API
Launching part can easily be done by Flask. We have to import flask then there is code which is mentioned with comments in our code. One very crucial thing that happens during launching is to decide the address of host. We can also host the API in our own local machine. We can also use multiole online service to host.

### Making the Handlers
Actually Handlers are the part which facilitates in achieving the goals in API. Every handler has a route or path where request comes and thus handler gets invoke. the second part of Handler is fuction that starts executing once handler gets invoked. So we use a decorator to assign a route to handler. Then we write code to form the fuction wwhich will start once handler receives any request. Here is an illustration:
