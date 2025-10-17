from abc import ABC, abstractmethod


class IEmailNotifierService(ABC):
    
    @abstractmethod
    def prepared_email(self, title: str, content: str, to: list, cc: list = []):
        raise NotImplementedError

    @abstractmethod
    def send_email(self, template: str, title: str, to: list, content: dict, send: bool = True, cc: list = []):
        raise NotImplementedError
