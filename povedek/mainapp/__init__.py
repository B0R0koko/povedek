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
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(ADMIN_EMAIL, ADMIN_EMAIL_PASSWORD)
                subject = "Эксперимент Поведек"
                body = f"Здравствуйте {first_name},\n\nНедавно Вы участвовали в нашем эксперименте, ваш соперник только что закончил игру:\nПоздравляем Вы выиграли {rwin} очков!!\nТакже напоминаем, что теперь вы участвуете в розыгрыше 1000 рублей. Удачи!!\n\nНаша команда благодарит Вас за участие!"
                msg = MIMEText(body, "plain", "utf-8")
                msg["Subject"] = Header(subject, "utf-8")
                msg["From"] = ADMIN_EMAIL
                msg["To"] = to_addr
                smtp.sendmail(msg["From"], to_addr, msg.as_string())
        except:
            pass


class Constants(BaseConstants):
    name_in_url = "mainapp"
    players_per_group = 2
    num_rounds = 1
    payment = cu(1)
    answers = [9362, 2579, 6814, 7984, 2852]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    initial_payoff = models.IntegerField(initial=0)
    initial_opponent_payoff = models.IntegerField(initial=0)
    chosen_payoff = models.IntegerField(label="Ваш выигрыш:", min=0, max=500)
    final_payoff = models.IntegerField()


class WaitOtherPlayers(WaitPage):
    title_text = "Пожалуйста, не закрывайте вкладку, пока Вам на почту не придет уведомление о результате игры. Вы можете переходить на другие вкладки. Оставьте браузер в фоновый режиме!!"
    body_text = "Мы назначили вашего соперника диктатором. Он определит итоговое количество очков обоих игроков. Информация об очках, полученных в процессе игры, будет известна только диктатору. Вы узнаете только то количество очков, которое назначил диктатор. Мы пришлём вам количество очков на электронный адрес, который вы указали в форме."
    group_by_arrival_time = True


def group_by_arrival_time_method(subsession, waiting_players):
    valid_players = [p for p in waiting_players if not p.participant.is_dropout]
    if len(valid_players) >= 2:
        return valid_players


# Main template for question page
class CalcResultsPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        recipient, leader = group.get_players()
        leader_answers = [leader.participant.vars[f"ans_{i}"] for i in range(5)]
        recipient_answers = [recipient.participant.vars[f"ans_{i}"] for i in range(5)]
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


class DecisionPage(Page):
    form_model = "player"
    form_fields = ["chosen_payoff"]

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2

    @staticmethod
    def error_message(player, values):
        if values["chosen_payoff"] < 0:
            return "Ваш выигрыш не может быть отрицательным"
        if values["chosen_payoff"] > 500:
            return "Вам выигрыш не может превышать 500"


class CalcFinalResultsPage(WaitPage):

    title_text = "Теперь Вы можете закрыть страницу"
    body_text = "Ожидаем, когда оппонент закончит игру.\nТакже Вы можете закрыть страницу, на указанную почту позже Вам придет письмо с результатами игры."

    @staticmethod
    def after_all_players_arrive(group):
        recipient, leader = group.get_players()
        leader.final_payoff = leader.chosen_payoff
        recipient.final_payoff = 500 - leader.chosen_payoff
        # Once leader made a decision send email to the other player
        Utility.send_email(
            recipient.participant.mail,
            recipient.participant.first_name,
            recipient.final_payoff,
        )


class FinalPage(Page):
    form_model = "player"

    @staticmethod
    def error_message(player, values):
        if values["age"] < 0:
            return "Возраст не может быть отрицательным"
        elif values["age"] > 80:
            return "Пожалуйста укажите свой настоящий возраст"


page_sequence = [
    WaitOtherPlayers,
    CalcResultsPage,  # Page where both players are awaited to calculate their results
    DecisionPage,  # Page where leader decides his final payoff
    CalcFinalResultsPage,
    FinalPage,
]
