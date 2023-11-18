class EmailUnsubscribeSecret:
    def __init__(self, email:str, unsubscribe_secret:int):
        self.email = email
        self.unsubscribe_secret = unsubscribe_secret


    def print(self):
        print(f"email {self.email} unsubscribe_secret {self.unsubscribe_secret}")