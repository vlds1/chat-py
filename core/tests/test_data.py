register_test_data = [
    (
        "xxx@yandex.ru",
        "passw124ord",
        {"detail": "user has been registered"},
    ),
    (
        "vu",
        "asfasdqw",
        {
            "detail": [
                {
                    "loc": ["email"],
                    "msg": "value is not a valid email address",
                    "type": "value_error.email",
                }
            ]
        },
    ),
]

login_test_data = [
    ("vu", "asfasdqw", "detail"),
    ("xxx@yandex.ru", "passw124ord", "data"),
]
