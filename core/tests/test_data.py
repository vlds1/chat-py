register_test_data = [
    (
        "xxx1@yandex.ru",
        "passw124ord",
        {"detail": "user has been registered"},
    ),
    (
        "vu",
        "asfasdqw",
        {"detail": "{'email': ['Not a valid email address.']}"},
    ),
]

login_test_data = [
    ("vu", "asfasdqw", "detail"),
    ("xxx1@yandex.ru", "passw124ord", "detail"),
]
