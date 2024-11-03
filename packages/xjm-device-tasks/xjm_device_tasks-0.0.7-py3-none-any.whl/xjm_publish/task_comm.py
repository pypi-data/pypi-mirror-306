import re

from .client import Stage, AndroidClient, ClientWaitTimeout


class SleepStage(Stage):
    def __init__(self, stage_serial: int, second: int):
        super().__init__(stage_serial)
        self.second = second

    def run(self, client: AndroidClient):
        client.device.sleep(self.second)


class PressTextStage(Stage):
    def __init__(self, stage_serial: int, text: str | re.Pattern, timeout=10, raise_not_found: bool = True):
        super().__init__(stage_serial)
        self.text = text
        self.timeout = timeout
        self.raise_not_found = raise_not_found

    def run(self, client: AndroidClient):
        try:
            client.wait_to_click({'text': self.text}, self.timeout)
        except ClientWaitTimeout as e:
            if self.raise_not_found:
                raise e


class WaitTextStage(Stage):
    def __init__(self, stage_serial: int, text: str | re.Pattern, timeout=10):
        super().__init__(stage_serial)
        self.text = text
        self.timeout = timeout

    def run(self, client: AndroidClient):
        client.wait_until_found({'text': self.text}, timeout=self.timeout)


class WaitXpathStage(Stage):
    def __init__(self, stage_serial: int, xpath: str, timeout=10):
        super().__init__(stage_serial)
        self.xpath = xpath
        self.timeout = timeout

    def run(self, client: AndroidClient):
        client.device.xpath(self.xpath).wait(self.timeout)


class PressRelativePositionStage(Stage):
    """
    relative position is [0, 0] to [1, 1]
    """

    def __init__(self, stage_serial: int, width_offset: float, height_offset: float):
        super().__init__(stage_serial)
        self.width_offset = width_offset
        self.height_offset = height_offset

    def run(self, client: AndroidClient):
        client.relative_click(self.width_offset, self.height_offset)


class WaitActivityStage(Stage):
    def __init__(self, stage_serial: int, activity: str, timeout=10):
        super().__init__(stage_serial)
        self.activity = activity
        self.timeout = timeout

    def run(self, client: AndroidClient):
        client.wait_until_activity(self.activity, self.timeout)


class PassStage(Stage):
    def __init__(self, stage_serial: int, *args, **kwargs):
        super().__init__(stage_serial)

    def run(self, client: AndroidClient):
        pass


class FailedToRunStage(Stage):
    def __init__(self, stage_serial: int, runStage: Stage, failStage: Stage):
        super().__init__(stage_serial)
        self.run_stage = runStage
        self.fail_stage = failStage

    def run(self, client: AndroidClient):
        try:
            self.run_stage.run(client)
        except Exception as e:
            self.fail_stage.run(client)


class SuccessToRunStage(Stage):
    def __init__(self, stage_serial: int, runStage: Stage, successStage: Stage):
        super().__init__(stage_serial)
        self.run_stage = runStage
        self.success_stage = successStage

    def run(self, client: AndroidClient):
        self.run_stage.run(client)
        self.success_stage.run(client)


class FinishToRunStage(Stage):
    def __init__(self, stage_serial: int, runStage: Stage, finishStage: Stage):
        super().__init__(stage_serial)
        self.run_stage = runStage
        self.finish_stage = finishStage

    def run(self, client: AndroidClient):
        try:
            self.run_stage.run(client)
        except Exception as e:
            pass
        self.finish_stage.run(client)


class RetryStage(Stage):
    def __init__(self, stage_serial: int, runStage: Stage, retry: int):
        super().__init__(stage_serial)
        self.run_stage = runStage
        self.retry = retry

    def run(self, client: AndroidClient):
        for i in range(self.retry):
            try:
                self.run_stage.run(client)
                break
            except Exception as e:
                pass
