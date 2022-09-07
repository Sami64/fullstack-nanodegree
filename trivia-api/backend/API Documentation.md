# Udacity Trivia API Documentation

## API Reference

### Getting Started
- Base URL: Access API endpoints on the localhost - `http://127.0.0.1:5000`

### Error Response
All errors from api calls return a JSON object on the form below
```
{
"success": False,
"message": "resource not found",
"error":400
}
```

### Endpoints
#### GET /categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
##### Example Response
```
{
'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```

#### GET /questions?page={integer}
- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: page - `integer`
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
##### Example Response
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}

```

#### GET /categories/${id}/questions
- Fetch questions for a category specified by id request argument
- Request Arguments: id - `integer`
- Returns: An object with questions for the specified category, total questions, and current category string
##### Example Response
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```

#### DELETE /question/${id}
- Deletes a specified question using the id of the question
- Request Arguments: id - `integer`
- Returns: An object with fields success and id of deleted question
##### Example Response
```
{
 "success": True,
 "deleted": 1
}
```

#### POST /quizzes
- Post request in order to get next question
##### Example Request
```
{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
 }
```

##### Example Response
```
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}
```

#### POST /questions
- Sends a post request to create a new question
- Returns: Returns an object with field success and created question id field
##### Example Request
```
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
```

##### Example Response
```
{
'success': True,
'created': 1
}
```

#### POST /questions
- Sends a post request to search questions by search term
- Returns: Returns an object with field questions and another for totalQuestions and final for current category
##### Example Request
```
{
    'searchTerm': 'who is'
}
```

##### Example Response
```
{
"questions": results,
 "totalQuestions": len(results),
 "currentCategory": None
}
```
