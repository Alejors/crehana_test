from app.domain.interfaces import IMailingService


class TerminalMailingService(IMailingService):
    def sendmail(self, recipient: str):
        print(
            f"""
        --------------- Sending Invitation ----------------\n
        To: {recipient}\n
        Subject: Invitation to Participate in Task Manager\n
        Body:
            Hey! Someone invited you to participate in Task Manager App.
            You will be in charge of amazing Task and able to manage Lists.

            See you There!\n
        -------------- Invitaion Ended -------------------
        """
        )
