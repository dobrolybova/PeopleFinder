# Service searches people from DB by first/last name, age, email, telephone number and city, extends it with some data and returns.

### API:
##### url: /find

##### body format (all fields are optional):
```
{
 "first_name": "first_name",
 "last_name": "last_name",
 "age": 11,
 "msisdn": "msisdn",
 "email": "email",
 "city": "city"
 }
 ```

##### Also metrics are available by url: /prometheus

The service consists of two apps: id generator and people finder.

Id generator provides API and extends people's data with uuid.
People finder fetches data from DB and provides it to id generator. 