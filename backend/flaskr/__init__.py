import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from random import choice

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/categories")
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            if categories:
                response = {"categories": {c.id: c.type for c in categories}}
                return jsonify(response)
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application you should see
    questions and categories generated, ten questions per page and
    pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/questions")
    def get_questions():
        try:
            page = request.args.get("page", 1, type=int)
            if page:
                questions = Question.query.order_by(Question.category).paginate(
                    page, QUESTIONS_PER_PAGE, True
                )
                if questions:
                    items = questions.items
                    if items:
                        response = {
                            "questions": [question.format() for question in items],
                            "totalQuestions": len(items),
                            "categories": {c.id: c.type for c in Category.query.all()},
                            "success": True,
                        }
                        return jsonify(response)
                else:
                    abort(404)
        except:
            abort(400)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def get_question_by_id(question_id):
        try:
            question = Question.query.get(question_id)
            if question:
                question.delete()
                return jsonify({"success": True})
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question
    will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route("/questions", methods=["POST"])
    def create_question():
        try:
            payload = request.get_json()
            if payload:
                new_question = Question(
                    question=payload["question"],
                    answer=payload["answer"],
                    category=payload["category"],
                    difficulty=payload["difficulty"],
                )
                new_question.insert()
                return jsonify({"success": True})
        except:
            abort(400)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/find", methods=["POST"])
    def search_question():
        try:
            search_term = request.get_json()["searchTerm"]
            if search_term:
                questions = (
                    Question.query.order_by(Question.id)
                    .filter(Question.question.ilike(f"%{search_term}%"))
                    .all()
                )
                if questions:
                    response = {
                        "success": True,
                        "questions": [q.format() for q in questions],
                        "totalQuestions": len(questions),
                    }
                    return jsonify(response)
                abort(404)
            abort(400)
        except:
            abort(400)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_question_by_category(category_id):
        try:
            questions = Question.query.filter_by(category=category_id).all()
            if questions:
                response = {
                    "questions": [q.format() for q in questions],
                    "totalQuestions": len(questions),
                    "currentCategory": Category.query.get(category_id).type,
                }
                return jsonify(response)
            else:
                abort(404)
        except:
            abort(400)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/quizzes", methods=["POST"])
    def get_random_by_category():
        try:
            category = request.get_json()["quiz_category"]
            cid = category["id"]
            current_category = category["type"] if cid != 0 else "All"

            previous_questions = request.get_json()["previous_questions"]

            if category["id"] != 0:
                questions = [
                    q
                    for q in Question.query.filter_by(category=cid).all()
                    if q.id not in previous_questions
                ]
            else:
                questions = [
                    q for q in Question.query.all() if q.id not in previous_questions
                ]

            if questions or previous_questions:
                if questions:
                    question = choice(questions)
                    response = {
                        "question": question.format(),
                        "totalQuestions": len(questions),
                        "currentCategory": current_category,
                    }
                else:
                    response = {"success": True}
                return jsonify(response)
            else:
                abort(404)
        except:
            abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    return app
