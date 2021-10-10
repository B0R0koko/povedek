from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = "mainapp"
    players_per_group = 2
    num_rounds = 1
    payment = cu(1)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    number_passed = models.FloatField()


# PAGES
class StartPage(Page):
    pass


class WaitOtherPlayersPage(WaitPage):
    pass


class FirstQuestion(Page):

    timeout_seconds = 10
    form_model = "player"
    form_fields = ["number_passed"]

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            number_passed = None


class Results(Page):
    pass


page_sequence = [StartPage, WaitOtherPlayersPage, FirstQuestion, Results]
