# README #
This README normally documents whatever steps are necessary to get your application up and running.

### Technology Stack ###
* Python 3.9
* FastAPI
* faiss-cpu==1.7.4
* langchain==0.0.207
* pinecone-client
* pgvector

### Third Party Integrations ###
* SendGrid - Sending emails
* youtube-transcript-api - getting text youtube url
* docx2txt - getting text from docx file
* pypdf - getting text from pdf file
* selenium -getting text from url file
* other document loaders and data parsing librarires

### Project Setup ###
* install the dependencies in requirement files
  - pip install -r requirements.txt
* add openai and other api key in env file
* refer sample.env for variable names and use backend.env as actual env file 
* configure the constant variables in constant.py according to your use case

* Vector Database configuration:
    - configure the application according to your vector database

* further guidelines:
    - change how data is parsed according to fit your custom requirement
    - change the constant variables according to use cases
    - modify the boilerplate code for your project specific use cases

### features ###
* endpoints and utilites for generic functions
* create vector embeddings - from youtube video, html page,sitemaps,url, pdf, docx, json, text file, csv, or relational database
* question and answer based on custom data with exact sources
* token count and token exceeded error handling with tiktoken
* different vector db support for differnt endpoints


### future enhancement ###
* streaming the openai response real time to frontend 
* add some utilities function and improve functionality of existing ones.
* make code more modular and configurable

### IDE ###
* PyCharm
* VS Code
* Sublime Text

### Project Setup ###
* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Coding Conventions ###
* PEP8
* write modular and configurable code
* Do not put commented code or unused imports in the main code
* Absolute imports should be used instead of Relative imports
* Use of f-strings instead of .format() or %s
* Class names should be in CamelCase
* Function names and variable names should be in snake_case
* Use of type hints
* Use of docstrings
* Use of logging  


### Contribution guidelines ###
* Writing tests
* Code review
* Other guidelines




### REDIS INTEGATION ###
* Install redis : pip install redis aioredis
* freeze the requirements : pip freeze > requirements.txt
* Add REDIS_HOST_URL in .env file
* Redis instance is created in main.py file, in on_startup event

### Celery Integration ###
* Install celery : pip install celery
* freeze the requirements : pip freeze > requirements.txt
* Add CELERY_BROKER_URL in .env file
* Celery instance is created in core module, in celery_app
* Celery tasks are created in worker module in root directory
* Celery worker is started using command: celery -A app.worker worker -l info -c 1

### Celery Beat Integration ###
* Install celery : pip install celery
* freeze the requirements : pip freeze > requirements.txt
* Celery beat instance is created in worker module in root directory
* While adding new tasks, add them in worker module in root directory with scheduled time in seconds
* Celery beat is started using command: celery -A app.worker beat -l info

### Sentry Integration ###
* Install Sentry SDK : pip install sentry-sdk
* freeze the requirements : pip freeze > requirements.txt
* Sentry instance is created in main.py file