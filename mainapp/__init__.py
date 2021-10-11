from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = "mainapp"
    players_per_group = 2
    num_rounds = 1
    payment = cu(1)
    questions = [
        "Угадайте расстояние между Сан-Франциско и Иваново. Укажите ответ в километрах",
        "Угадайте расстояние между Костромой и Норильском",
        "Угадайте расстояние между Находкой и Владикавказом",
        "Угадайте расстояние между Чикаго и Якутском",
        "Угадайте расстояние между Осло и Астраханью",
    ]
    answers = [9362, 2579, 6814, 7984, 2852]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    num_1 = models.FloatField(label="Введите ответ сюда:")
    num_2 = models.FloatField(label="Введите ответ сюда:")
    num_3 = models.FloatField(label="Введите ответ сюда:")
    num_4 = models.FloatField(label="Введите ответ сюда:")
    num_5 = models.FloatField(label="Введите ответ сюда:")
    total_payoff = models.FloatField(initial=0)
    options = models.IntegerField(
        choices=[
            [0, "0 очков мне и 500 очков сопернику"],
            [1, "100 очков мне и 400 очков сопернику."],
            [2, "200 очков мне и 300 очков сопернику."],
            [3, "300 очков мне и 200 очков сопернику"],
            [4, "400 очков мне и 100 очков сопернику"],
            [5, "500 очков мне и 0 очков сопернику."],
        ],
        widget=widgets.RadioSelect,
        label="Варианты:",
    )

    # Variables used to get around @staticmethods
    current_question = models.IntegerField(initial=1)
    current_answer = models.FloatField()


# PAGES
class StartPage(Page):
    pass


class WaitOtherPlayersPage(WaitPage):
    pass


# Main template for question page
class QuestionPage(Page):
    timeout_seconds = 10
    form_model = "player"

    @staticmethod
    def vars_for_template(player):
        return {
            "round_number": player.current_question,
            "current_question": Constants.questions[player.current_question - 1],
        }

    @staticmethod
    def error_message(player, values):
        if values["num_{}".format(player.current_question)] < 0:
            return "Расстояние должно быть положительным"

    @staticmethod
    def get_form_fields(player):
        return ["num_{}".format(player.current_question)]

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.current_question += 1


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        first, second = group.get_players()

        def compare_errors(first_a, second_a, round_num):
            correct = Constants.answers[round_num - 1]
            error_1, error_2 = (abs(correct - first_a), abs(correct - second_a))
            if error_1 > error_2:
                first.total_payoff += 100
            elif error_1 == error_2:
                first.total_payoff += 50
                second.total_payoff += 50
            else:
                second.total_payoff += 100

        # For some reason u cant just access all player fields at once
        # so you have to go the long way
        compare_errors(first.num_1, second.num_1, 1)
        compare_errors(first.num_2, second.num_2, 2)
        compare_errors(first.num_3, second.num_3, 3)
        compare_errors(first.num_4, second.num_4, 4)
        compare_errors(first.num_5, second.num_5, 5)


class DecisionPage(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player):
        if player.id_in_group == 1:
            return {"second_player_payoff": str(500 - player.total_payoff)}

    @staticmethod
    def get_form_fields(player):
        if player.id_in_group == 1:
            return ["options"]

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1


class WaitLeaderPage(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2


class FinalPage(Page):
    @staticmethod
    def vars_for_template(player):
        winnings_mapping = {0: 0, 1: 100, 2: 200, 3: 300, 4: 400, 5: 500}
        if player.id_in_group == 1:
            return {"winnings": winnings_mapping[player.options]}
        else:
            leader = player.get_others_in_group()
            return {"winnings": 500 - winnings_mapping[leader[0].options]}


page_sequence = [
    StartPage,
    WaitOtherPlayersPage,
    QuestionPage,
    QuestionPage,
    QuestionPage,
    QuestionPage,
    QuestionPage,
    ResultsWaitPage,
    DecisionPage,
    WaitLeaderPage,
    FinalPage,
]
