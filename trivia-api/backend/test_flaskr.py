import json
import os
import unittest

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        load_dotenv()
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(os.environ.get('DB_TEST_USER'),
                                                               os.environ.get('DB_TEST_PASSWORD'),
                                                               os.environ.get('DB_TEST_HOST'), self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {"question": "Question 1", "answer": "Answer 1", "difficulty": 1, "category": 1}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_404_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        if data['categories'] == 0:
            self.assertEqual(res.status_code, 404)

    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_404_get_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': 'What'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

    def test_422_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': ''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def test_retrieve_category_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

    def test_404_retrieve_category_questions(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_retrieve_quiz_questions(self):
        res = self.client().post('/quizzes',
                                 json={'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': 1}})
        data = json.loads(res.data)

        self.assertEqual(data['code'], 404)
        self.assertTrue(data['question'])

    def test_404_retrieve_quiz_questions(self):
        res = self.client().post('/quizzes',
                                 json={'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': 1000}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
