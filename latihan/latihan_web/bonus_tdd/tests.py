from django.test import TestCase, Client

class BonusTddTest(TestCase):

    def test_bonus_tdd_url_is_exist(self):

        response = Client().get('/bonus_tdd')

        self.assertEqual(response.status_code,200)

    def test_bonus_tdd_page_content(self):

        response = Client().get('/bonus_tdd')

        html_response = response.content.decode('utf8')

        self.assertIn('Try Unit Test!', html_response)