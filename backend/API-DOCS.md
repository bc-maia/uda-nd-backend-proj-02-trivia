# API Reference: Udacitrivia

## Project
- This project is result of Udacity second project: **Udacitrivia**. This project is composed by two apps: A Python Flask API and a ReactJS frontend consuming the Questions API. This document aims on explaining and documenting API routes.

## Getting Started
Assuming the project is properly configured, and started, it will be running at:
- http://localhost:5000

## Making requests
As developer you can try those API requests using any tool able to make HTML requests, like curl or postman. In this case, if you're using VSCode with the [REST Client](https://github.com/Huachao/vscode-restclient) plugin, that can be used with the [requests.rest](./requests.rest) file in this repository, which will make testing the API simpler.

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return Four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable 

___

## Endpoints 



## GET /categories

**Description**
 * Lists currently available categories

_Response_
```JSON
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    }
}
```

## GET /questions?page=3

**Description**
 * Get all questions paginated by current _QUESTIONS_PER_PAGE_ of 10 results per page limit.

_Response_
```JSON
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "totalQuestions": 10
}
```

## POST /questions

**Description**
 * Create a new question to the questions base.

* Body (JSON):
```JSON
{
    "question": "This is a question?",
    "answer": "YES",
    "category": "1",
    "difficulty": "1"
}
```

_Response_
```JSON
{
    "success": true
}
```

## DELETE /questions/{question_id}

**Description**
 * Removes a question by id from the questions base.

_Response_
```JSON
{
    "success": true
}
```

## POST /find

**Description**
 * Find questions based on search term and return all results found.

* Body (JSON):
```JSON
{
    "searchTerm": "question"
}
```

_Response_
```JSON
{
    "questions": [
        {
            "answer": "YES",
            "category": 1,
            "difficulty": 1,
            "id": 31,
            "question": "This is a question?"
        }
    ],
    "success": true,
    "totalQuestions": 1
}
```

## GET /categories/{category_id}/questions

**Description**
 * Get questions by category via id on URL and return all results found.

_Response_

```JSON
{
  "currentCategory": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "YES",
      "category": 1,
      "difficulty": 1,
      "id": 31,
      "question": "This is a question?"
    }
  ],
  "totalQuestions": 4
}
```

## POST /quizzes

**Description**
 * Get question for in game. Passing current category id (or category id = '0' for all categories), also, it could contain the previous question ids, to remove repeated questions.

* Body (JSON):
```JSON
{
    "previous_questions": [], 
    "quiz_category": {
        "type": "Science", "id": "1"
        }
}
```

_Response_
```JSON
{
    "currentCategory": "Science",
    "question": {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
    },
    "totalQuestions": 4
}
```