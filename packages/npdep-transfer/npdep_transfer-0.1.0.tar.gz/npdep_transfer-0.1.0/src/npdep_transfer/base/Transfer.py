class Transfer():
    def __init__(self, id, options, registration) -> None:
        self.id = id
        self.options = options
        self.registration = registration

    def init(self):
        print("No special behaviour for init step implemented in transfer module: " + self.id)

    def send(self):
        print("No special behaviour for send step implemented in transfer module: " + self.id)

    def end(self):
        print("No special behaviour for end step implemented in transfer module: " + self.id)