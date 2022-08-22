from django.test import TestCase
from .models import Player

# Create your tests here.
class PlayerTestCase(TestCase):
    def setUp(self) -> None:
        Player.objects.create(game_id="111111111", nick="TestPlayer")

    def test_player_is_searchable_by_id(self):
        found = Player.objects.filter(game_id="111111111").first()

        self.assertEqual(found.nick, "TestPlayer")
