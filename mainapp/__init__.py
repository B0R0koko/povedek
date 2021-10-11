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

    num_1 = models.FloatField()
    num_2 = models.FloatField()
    num_3 = models.FloatField()
    num_4 = models.FloatField()
    num_5 = models.FloatField()
    total_payoff = models.FloatField(initial=0)


# PAGES
class StartPage(Page):
    pass


class WaitOtherPlayersPage(WaitPage):
    pass


class FirstQuestion(Page):

    timeout_seconds = 10
    form_model = "player"
    form_fields = ["num_1"]

    @staticmethod
    def before_next_page(player, timeout_happened):
        correct_answer = 9362
        error = abs(player.num_1 - correct_answer)
        punish = correct_answer / 100
        player.total_payoff += max(100 - error / punish, 0)

    @staticmethod
    def error_message(player, values):
        if values["num_1"] < 0:
            return "Расстояние не может быть отрицательным"


class SecondQuestion(Page):

    timeout_seconds = 10
    form_model = "player"
    form_fields = ["num_2"]

    @staticmethod
    def before_next_page(player, timeout_happened):
        corrent_answer = 2579
        error = abs(player.num_2 - corrent_answer)
        punish = corrent_answer / 100
        player.total_payoff += max(100 - error / punish, 0)

    @staticmethod
    def error_message(player, values):
        if values["num_2"] < 0:
            return "Расстояние не может быть отрицательным"


class ThirdQuestion(Page):

    timeout_seconds = 10
    form_model = "player"
    form_fields = ["num_3"]

    @staticmethod
    def before_next_page(player, timeout_happened):
        corrent_answer = 6814
        error = abs(player.num_3 - corrent_answer)
        punish = corrent_answer / 100
        player.total_payoff += max(100 - error / punish, 0)

    @staticmethod
    def error_message(player, values):
        if values["num_3"] < 0:
            return "Расстояние не может быть отрицательным"


class FourthQuestion(Page):

    timeout_seconds = 10
    form_model = "player"
    form_fields = ["num_4"]

    @staticmethod
    def before_next_page(player, timeout_happened):
        corrent_answer = 7984
        error = abs(player.num_4 - corrent_answer)
        punish = corrent_answer / 100
        player.total_payoff += max(100 - error / punish, 0)

    @staticmethod
    def error_message(player, values):
        if values["num_4"] < 0:
            return "Расстояние не может быть отрицательным"


class FifthQuestion(Page):

    timeout_seconds = 10
    form_model = "player"
    form_fields = ["num_5"]

    @staticmethod
    def before_next_page(player, timeout_happened):
        correct_answer = 2852
        error = abs(player.num_5 - correct_answer)
        punish = correct_answer / 100
        player.total_payoff += max(100 - error / punish, 0)
        player.total_payoff = round(player.total_payoff)

    @staticmethod
    def error_message(player, values):
        if values["num_5"] < 0:
            return "Расстояние не может быть отрицательным"


class Results(Page):
    pass


class CombinedResults(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player):
        return {"total_payoff": player.total_payoff}


page_sequence = [
    StartPage,
    WaitOtherPlayersPage,
    FirstQuestion,
    SecondQuestion,
    ThirdQuestion,
    FourthQuestion,
    FifthQuestion,
    Results,
    CombinedResults,
]
