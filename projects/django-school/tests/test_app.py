from django.test import SimpleTestCase,Client
from main import STUDENTS

class DirectoryTests(SimpleTestCase):
    def test_students(self):
        response=Client().get("/api/students/")
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()["students"]),2)
    def test_post_rejected(self):
        self.assertEqual(Client().post("/api/students/").status_code,405)
