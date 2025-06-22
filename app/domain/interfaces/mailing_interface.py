from abc import ABC, abstractmethod


class IMailingService(ABC):
    @abstractmethod
    def sendmail(self, recipient: str):
        raise NotImplementedError("Method Not Implemented")
