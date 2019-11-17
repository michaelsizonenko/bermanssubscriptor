import json


class Config:

    input_file = None
    error_file = None
    random_count = 25
    email_for_subscription = None
    page_load_timeout = 60  # seconds

    def __init__(self):
        with open("config.json") as f:
            config_data = json.loads(f.read())
            self.input_file = config_data.get("input_file")
            self.error_file = config_data.get("error_file")
            self.random_count = config_data.get("random_count")
            self.email_for_subscription = config_data.get("email_for_subscription")
            self.page_load_timeout = config_data.get("page_load_timeout")
        if not self.error_file:
            self.error_file = "errors.txt"


config = Config()