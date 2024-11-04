class Sourcing():
    def __init__(self, id, options, registration) -> None:
        self.id = id
        self.options = options
        self.registration = registration

    def init(self):
        print("No special behaviour for init step implemented in sourcing module: " + self.id)

    def get(self):
        print("No special behaviour for get step implemented in sourcing module: " + self.id)

    def end(self):
        print("No special behaviour for end step implemented in sourcing module: " + self.id)