from os import environ


SESSION_CONFIGS = [
    dict(
        name="mainapp",
        app_sequence=["userform", "mainapp"],
        num_demo_participants=4,
        display_name="Povedek Experiment",
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)


PARTICIPANT_FIELDS = [
    "first_name",
    "second_name",
    "is_dropout",
    "is_leader",
    "question_num",
    "ans_0",
    "ans_1",
    "ans_2",
    "ans_3",
    "ans_4",
    "mail",
]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = "en"

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "USD"
USE_POINTS = True

ADMIN_USERNAME = "admin"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")
ADMIN_EMAIL = environ.get("ADMIN_EMAIL")
ADMIN_EMAIL_PASSWORD = environ.get("ADMIN_EMAIL_PASSWORD")

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = "5664654330323"
