from zedasignal_backend.core.termii.bulk_sms_client import TermiiBulkSmsClient


class TermiiBulkSmsSender:
    @property
    def bulk_client(self):
        return TermiiBulkSmsClient()

    def send_bulk_sms(self, to: list[str], message: str):
        response = self.bulk_client.post(to=to, message=message)
        return response
