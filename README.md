# API USAGE

## http://127.0.0.1:12345/database/?id

### GET
- takes input 'id' from url
- returns the data saved for the corresponding person, based on id input, if no such
person exists in the database, the response will specify so

### PUT
- takes input 'id' from url
- takes name, age, and birthday in body form-data, if any are missing, response
will specify so
- updates person data corresponding with id input

### DELETE
- takes input 'id' from url
- deletes person corresponding with id

## http://127.0.0.1:12345/database

### POST
- takes name, age, and birthday in body form-data, if any are missing, response
will specify so
- creates new person with corresponding data

## http://127.0.0.1:12345/database/showall

### GET
- returns all database data
