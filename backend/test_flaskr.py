import os
import unittest
import json
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # binds the app to the current context
        self.app = create_app()
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # GET /categories
    def test_get_categories_count(self):
        response = self.client().get("/categories")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["categories"]), 6)

    def test_error_category_not_allowed(self):
        response = self.client().put("/categories")
        self.assertEqual(response.status_code, 405)

    # GET /questions?page=
    def test_get_questions(self):
        response = self.client().get("/questions?page=1")
        total_questions = json.loads(response.data)["totalQuestions"]
        pagination_size = 10
        self.assertEqual(response.status_code, 200)
        self.assertEqual(total_questions, pagination_size)

    def test_error_questions_page_not_found(self):
        response = self.client().get("/questions?page=99")
        self.assertEqual(response.status_code, 404)

    # POST /questions
    def test_create_question(self):
        payload = {
            "question": "This is a question?",
            "answer": "YES",
            "category": "1",
            "difficulty": "1",
        }
        response = self.client().post("/questions", json=payload)
        self.assertEqual(response.status_code, 200)

    def test_error_create_question_bad_request(self):
        payload = {"question": "This is a question?", "answer": "YES"}
        response = self.client().post("/questions", json=payload)
        self.assertEqual(response.status_code, 400)

    # POST /find
    def test_find_question(self):
        payload = {"searchTerm": "Penicillin"}
        response = self.client().post("/find", json=payload)
        questions = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(questions["totalQuestions"], 1)
        q = questions["questions"][0]
        self.assertDictEqual(
            q,
            {
                "answer": "Alexander Fleming",
                "category": 1,
                "difficulty": 3,
                "id": 21,
                "question": "Who discovered penicillin?",
            },
        )

    def test_error_question_not_found(self):
        payload = {"searchTerm": "sharknado"}
        response = self.client().post("/find", json=payload)
        self.assertEqual(response.status_code, 404)

    # DELETE /questions/{question_id}
    def test_question_delete(self):
        # Previously added question into database
        question = Question.query.filter_by(question="This is a question?").first()
        response = self.client().delete(f"/questions/{question.id}")
        self.assertEqual(response.status_code, 200)

    def test_error_delete_question_wrong_id(self):
        response = self.client().delete("/questions/999")
        self.assertEqual(response.status_code, 404)

    # /categories/{category_id}/questions
    def test_get_questions_by_category(self):
        category_id = 5
        response = self.client().get(f"/categories/{category_id}/questions")
        total_questions = json.loads(response.data)["totalQuestions"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(total_questions, 3)

    def test_error_get_questions_by_unknown_category(self):
        category_id = 999
        response = self.client().get(f"/categories/{category_id}/questions")
        self.assertEqual(response.status_code, 400)

    # POST /quizzes
    def test_get_quiz_question(self):
        payload = {
            "previous_questions": [],
            "quiz_category": {"type": "History", "id": "4"},
        }
        response = self.client().post("/quizzes", json=payload)
        question = json.loads(response.data)
        self.assertEqual(question["currentCategory"], "History")
        self.assertEqual(question["totalQuestions"], 4)

    def test_error_get_quiz_question_bad_request(self):
        payload = {
            "quiz_category": {"type": "History", "id": "4"},
        }
        response = self.client().post("/quizzes", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_error_get_quiz_question_method_not_allowed(self):
        payload = {
            "previous_questions": [],
            "quiz_category": {"type": "History", "id": "4"},
        }
        response = self.client().get("/quizzes", json=payload)
        self.assertEqual(response.status_code, 405)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
