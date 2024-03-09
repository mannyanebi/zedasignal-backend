from zedasignal_backend.core.termii.client import TermiiClient


class Termii:
    @property
    def client(self):
        return TermiiClient()

    def send_sms(self, to: str, message: str):
        response = self.client.post(to=to, message=message)
        return response
