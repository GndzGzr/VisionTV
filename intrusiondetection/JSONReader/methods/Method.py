
class Method:
    def __init__(self, settings):
        self.settings = settings
        # display options
        self.email = settings["email_sent"]
        self.email_sent = False
        self.displayZone = settings["displayZone"]
        self.displayFPS = settings["displayFPS"]
