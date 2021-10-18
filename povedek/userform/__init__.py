from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = "userform"
    players_per_group = None
    num_rounds = 1
    questions = [
        "Угадайте расстояние между Сан-Франциско и Иваново. Укажите ответ в километрах",
        "Угадайте расстояние между Костромой и Норильском",
        "Угадайте расстояние между Находкой и Владикавказом",
        "Угадайте расстояние между Чикаго и Якутском",
        "Угадайте расстояние между Осло и Астраханью",
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    first_name = models.StringField(label="Имя")
    second_name = models.StringField(label="Фамилия")
    age = models.IntegerField(label="Возраст")
    mail = models.StringField(label="Почта")
    gender = models.IntegerField(
        choices=[[0, "Мужской"], [1, "Женский"]],
        widget=widgets.RadioSelect,
        label="Выберите пол: ",
    )
    university = models.StringField(label="Название университета")
    major = models.StringField(label="Образовательная программа")
    year = models.IntegerField(label="Курс")

    ans_0 = models.IntegerField(label="Введите ответ:")
    ans_1 = models.IntegerField(label="Введите ответ:")
    ans_2 = models.IntegerField(label="Введите ответ:")
    ans_3 = models.IntegerField(label="Введите ответ:")
    ans_4 = models.IntegerField(label="Введите ответ:")


class RulePage(Page):
    pass


class FormPage(Page):
    timeout_seconds = 120

    form_model = "player"
    form_fields = [
        "first_name",
        "second_name",
        "age",
        "mail",
        "gender",
        "university",
        "major",
        "year",
    ]

    # if any of fields skipped player is not allowed to parttake
    @staticmethod
    def before_next_page(player, timeout_happened):
        if (
            player.first_name == ""
            or player.second_name == ""
            or player.age == 0
            or player.mail == ""
            or player.university == ""
            or player.major == ""
            or player.year == 0
        ):
            player.participant.is_dropout = True
        else:
            player.participant.is_dropout = False
            fields = getattr(FormPage, "form_fields")
            player_values = [getattr(player, field) for field in fields]
            for field, value in zip(fields, player_values):
                player.participant.vars[field] = value

        player.participant.question_num = 0

    @staticmethod
    def error_message(player, values):
        if values["age"] < 0:
            return "Возраст не может быть отрицательным"
        elif values["age"] > 80:
            return "Пожалуйста укажите свой настоящий возраст"
        elif "@" not in values["mail"]:
            return "Пожалуйста укажите свою настояющую почту"


class DisconnectedPage(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.is_dropout


class QuestionPage(Page):
    timeout_seconds = 10
    form_model = "player"

    @staticmethod
    def vars_for_template(player):
        return {
            "round_number": player.participant.question_num + 1,
            "current_question": Constants.questions[player.participant.question_num],
        }

    @staticmethod
    def error_message(player, values):
        if values["ans_{}".format(player.participant.question_num)] < 0:
            return "Расстояние должно быть положительным"

    @staticmethod
    def get_form_fields(player):
        return ["ans_{}".format(player.participant.question_num)]

    @staticmethod
    def before_next_page(player, timeout_happened):
        answer_key = f"ans_{player.participant.question_num}"
        player.participant.vars[answer_key] = getattr(player, answer_key)
        player.participant.question_num += 1
        player.participant.mail = player.mail


page_sequence = [
    RulePage,
    FormPage,
    DisconnectedPage,
    QuestionPage,
    QuestionPage,
    QuestionPage,
    QuestionPage,
    QuestionPage,
]
