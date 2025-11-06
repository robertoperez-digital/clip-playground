# Clip playground

# Setup

### Prerequisites
#### Local Postgresql database
```
Be sure your db has the 

pgvector extension

And activate it with following query statement

CREATE EXTENSION IF NOT EXISTS vector;

TODO: Add support for config file in order to setup db connection params, right now params are hardcoded on db.py file
```

## Conda local environment for development
### 1.- Create conda env using environment.yml file, env will be called cplayground, this will install all needed dependencies
```
$ conda env create -f environment.yml  # creates the env
$ conda activate cplayground            # activates the env
```
### 2.- Initialize service
```
$ fastapi dev main.py #it starts the service on default fastapi port 8000
```

## Docker image for deployement
### 1.- Call docker build to create an image from root folder
```
$ docker build --no-cache -t cplayground . 
```

### 2.- Start a container using the new image
```
$ docker run -d --name cplayground-cont -p 8000:8000 cplayground #it will start the service in cotainer on port 8000
```

## Usage

```
Use a rest client like postman or bruno or included interactive OpenApi tool available in

http://localhost:8000/docs

There you can test all endopoints
```
