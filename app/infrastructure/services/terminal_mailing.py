from app.domain.interfaces import IMailingService


class TerminalMailingService(IMailingService):
    def sendmail(self, recipient: str):
        print(f"""
        --------------- Sending Invitation ----------------\n
        To: {recipient}\n
        Subject: Invitation to Participate in Task Manager\n
        Body:
            Hey! Someone invited you to participate in Task Manager App.
            There you will be in charge of some amazing Task and you will be able to manage Lists.
        
            See you There!\n
        -------------- Invitaion Ended -------------------
        """)