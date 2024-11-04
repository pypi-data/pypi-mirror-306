import socket
import time
import traceback
import requests
from typing import Union
import logging

logger = logging


class Alerts:
    def __init__(self, **kwargs):
        self.exception = kwargs.get("exception")
        self.alert_header = kwargs.get("alert_header")
        self.alert_message = kwargs.get("alert_message")
        self.module_name = kwargs.get("module_name")
        self.slack_alerts_webhook = kwargs.get('slack_alerts_webhook')

        self._validate_initialization()


    def _validate_initialization(self):
        if self.slack_alerts_webhook is None:
            raise ValueError("The field - 'slack_alerts_webhook' is required and cannot be empty.")
        if self.module_name is None:
            raise ValueError("The field - 'module_name' is required and cannot be empty.")
    def get_alert_header(self) -> str:
        return f"[CRASH] - MODULE {self.module_name} MACHINE {socket.gethostname()}"

    def get_alert_message(self, trace=None) -> str:
        return f"{str(self.exception)} \n{'-' * 50} \n {trace if trace else traceback.format_exc()}"

    def __send_alert(self, url: str, payload: dict, max_retries: Union[int, None] = None) -> bool:
        attempt = 0
        retry_interval = 30

        if max_retries:
            retry_condition = attempt < max_retries
        else:
            retry_condition = True

        logger.info(payload)

        while retry_condition:
            try:
                response = requests.post(url, json=payload, timeout=30)
                status_code_class = response.status_code / 100
            except requests.Timeout as err:
                logger.error(err)
            except requests.ConnectionError as err:
                logger.error(err)
            else:
                if status_code_class == 2:
                    return True
                if status_code_class == 4:
                    logger.info(
                        f"Got RESPONSE: {response.text} STATUS CODE: {response.status_code} for URL: {response.request.url} BODY: {response.request.body}")
                    raise Exception(response.text)
                elif status_code_class == 5:
                    logger.error(f"Alerts endpoint responded with status code: {response.status_code}")
                    logger.info(response.text)

            logger.info(f"Will retry after {retry_interval} seconds")
            time.sleep(retry_interval)
            attempt += 1

            if max_retries:
                retry_condition = attempt < max_retries
            else:
                retry_condition = True

        return False

    def create_slack_payload(self) -> dict:
        return {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": self.alert_header,
                    },
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"{self.alert_message}"},
                },
            ]
        }

    def slack_alert(self) -> bool:
        logger.info("Sending slack alert")
        payload = self.create_slack_payload()
        return self.__send_alert(url=self.slack_alerts_webhook, payload=payload, max_retries=5)

    def alert(self, header="", message="") -> bool:
        try:
            self.alert_header = header if header else self.get_alert_header()
            self.alert_message = message if message else self.get_alert_message()
            success = self.slack_alert()
            return True
        except Exception as err:
            logger.error(err)
            exit(1)

    def handle_uncaught_exception(self, exc_type, exc_value, exc_traceback):
        exception = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger.error(exception)
        self.alert(message=exception)

    def handle_uncaught_thread_exception(self, args):
        exception = ''.join(traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback))
        thread_info = f"Thread Name: {args.thread.name if args.thread else 'Main Thread'}\n"
        logger.error(f"Exception in Thread:\n {thread_info} \n Exception: {exception}")
        self.alert(message=f"Exception in Thread:\n {thread_info} \n Exception: {exception}")

    def send_exception_alert(self, e):
        self.alert(message=''.join(traceback.format_exception(type(e), e, e.__traceback__)))
        logger.error(''.join(traceback.format_exception(type(e), e, e.__traceback__)))

