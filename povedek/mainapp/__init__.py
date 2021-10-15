from os import stat
from otree.api import *
from random import randint
from email.mime.text import MIMEText
from email.header import Header

from settings import ADMIN_EMAIL, ADMIN_EMAIL_PASSWORD
import smtplib


doc = """
Your app description
"""


class Utility:

    # Function used to send email once opponent is done with experiment
    def send_email(to_addr, first_name, rwin):
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(ADMIN_EMAIL, ADMIN_EMAIL_PASSWORD)
            subject = "Эксперимент Поведек"
            body = f"Здравствуйте {first_name},\n\nНедавно Вы участвовали в нашем эксперименте, ваш соперник только что закончил игру:\nПоздравляем Вы выиграли {rwin} очков!!\nТакже напоминаем, что теперь у вас имеется шанс выиграть 700 рублей. Удачи!!\n\nНаша команда благодарит Вас за участие!"
            msg = MIMEText(body, "plain", "utf-8")
            msg["Subject"] = Header(subject, "utf-8")
            msg["From"] = ADMIN_EMAIL
            msg["To"] = to_addr
            smtp.sendmail(msg["From"], to_addr, msg.as_string())


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

    # Answers on questions:
    ans_0 = models.IntegerField(label="Введите ответ сюда:")
    ans_1 = models.IntegerField(label="Введите ответ сюда:")
    ans_2 = models.IntegerField(label="Введите ответ сюда:")
    ans_3 = models.IntegerField(label="Введите ответ сюда:")
    ans_4 = models.IntegerField(label="Введите ответ сюда:")
    initial_payoff = models.IntegerField(initial=0)
    initial_opponent_payoff = models.IntegerField(initial=0)
    final_payoff = models.IntegerField(initial=0)

    # Choice made by the leader of the game
    chosen_payoff = models.IntegerField(label="Выберите свой выигрыш: ", min=0, max=500)

    # General information on the participant
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
    # Variables used to get around @staticmethods
    current_answer = models.FloatField()
    question_num = models.IntegerField(initial=0)
    is_winner = models.BooleanField()


# PAGES
class StartPage(Page):
    pass


# Main template for question page
class QuestionPage(Page):
    timeout_seconds = 10
    form_model = "player"

    @staticmethod
    def vars_for_template(player):
        return {
            "round_number": player.question_num + 1,
            "current_question": Constants.questions[player.question_num],
        }

    @staticmethod
    def error_message(player, values):
        if values["ans_{}".format(player.question_num)] < 0:
            return "Расстояние должно быть положительным"

    @staticmethod
    def get_form_fields(player):
        return ["ans_{}".format(player.question_num)]

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.question_num += 1


class RecipientInfoPage(Page):
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

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

    @staticmethod
    def error_message(player, values):
        if values["age"] < 0:
            return "Возраст не может быть отрицательным"
        elif values["age"] > 80:
            return "Пожалуйста укажите свой настоящий возраст"


class WaitLeaderPage(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1


class WaitRecipientPage(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2


class DecisionPage(Page):
    form_model = "player"
    form_fields = ["chosen_payoff"]

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2


class CalcResultsPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        recipient, leader = group.get_players()
        leader_answers = [getattr(leader, f"ans_{i}") for i in range(5)]
        recipient_answers = [getattr(recipient, f"ans_{i}") for i in range(5)]
        for lans, rans, cor in zip(
            leader_answers, recipient_answers, Constants.answers
        ):
            if abs(cor - lans) < abs(cor - rans):
                leader.initial_payoff += 100
            elif abs(cor - lans) == abs(cor - rans):
                if randint(0, 1):
                    leader.initial_payoff += 100
                else:
                    recipient.initial_payoff += 100
            else:
                recipient.initial_payoff += 100

        leader.initial_opponent_payoff, recipient.initial_opponent_payoff = (
            recipient.initial_payoff,
            leader.initial_payoff,
        )


class CalcFinalResultsPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        recipient, leader = group.get_players()
        leader.final_payoff = leader.chosen_payoff
        recipient.final_payoff = 500 - leader.chosen_payoff
        # Once leader made a decision send email to the other player
        Utility.send_email(recipient.mail, recipient.first_name, recipient.final_payoff)


class FinalPage(Page):
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

    @staticmethod
    def error_message(player, values):
        if values["age"] < 0:
            return "Возраст не может быть отрицательным"
        elif values["age"] > 80:
            return "Пожалуйста укажите свой настоящий возраст"


page_sequence = [
    StartPage,
    QuestionPage,
    QuestionPage,
    QuestionPage,
    QuestionPage,
    QuestionPage,
    RecipientInfoPage,
    WaitRecipientPage,
    CalcResultsPage,
    DecisionPage,
    WaitLeaderPage,
    CalcFinalResultsPage,
    FinalPage,
]
