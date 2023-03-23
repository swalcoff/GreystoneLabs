# Greystone Labs Coding Challenge
This is my submission for the Greystone labs code challenge. This API uses FastAPI, SQLModel, and SQLite for the DB.

#### To Run:

I've created a Makefile to make things simple. If running for the first time, first install dependencies:

```$ make install```

To run the api (this will create the DB if it doesn't already exist):

```$ make run```

To clear the DB:

```$ make clear```

#### How to test the API:

Since this app is using FastAPI, you will be able to access the documentation using http://127.0.0.1:8000/docs. Once here, you can run every command on the API. 

Note: if you exclude the ID number when creating a loan or user, the ID will be automatically calculated for you.

#### Functionality

All of the requested api calls are available. These include: 

- Create a user
- Create loan
- Fetch loan schedule
- Fetch loan summary for a specific month
- Fetch all loans for a user
- Share loan with another user

Please refer to docs to learn how each function is called. Enjoy :)
