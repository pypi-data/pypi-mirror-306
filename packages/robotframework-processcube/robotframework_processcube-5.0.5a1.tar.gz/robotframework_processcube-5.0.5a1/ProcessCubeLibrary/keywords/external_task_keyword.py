
import time
from typing import Dict, Any

from processcube_client.core.api import FetchAndLockRequestPayload
from processcube_client.core.api import FinishExternalTaskRequestPayload

from robot.api import logger

from ._retry_helper import retry_on_exception


class ExternalTaskKeyword:

    def __init__(self, client, **kwargs):
        self._client = client

    @retry_on_exception
    def get_external_task(self, topic: str, options: dict = {}, **kwargs):

        request = FetchAndLockRequestPayload(
            worker_id=self._worker_id,
            topic_name=topic,
            max_tasks=1
        )

        logger.info(f"get task with {request}")

        current_retry = 0
        current_delay = float(kwargs.get('delay', self._delay))
        backoff_factor = float(kwargs.get('backoff_factor', self._backoff_factor))
        max_retries = int(kwargs.get('max_retries', self._max_retries))

        while True:
            external_tasks = self._client.external_task_fetch_and_lock(request)

            logger.info(external_tasks)

            if len(external_tasks) == 1:
                external_task = external_tasks[0]
            else:
                external_task = {}

            if external_task:
                break
            else:
                time.sleep(current_delay)
                current_retry = current_retry + 1
                current_delay = current_delay * backoff_factor
                if current_retry > max_retries:
                    break
                logger.info(f" Retry count: {current_retry} of {max_retries}; delay: {current_delay} and backoff_factor: {backoff_factor}")

        return external_task

    @retry_on_exception
    def finish_external_task(self, external_task_id: str, result: Dict[str, Any], **kwargs):
        request = FinishExternalTaskRequestPayload(
            worker_id=self._worker_id,
            result=result
        )

        logger.info(f"finish task with {request}")

        self._client.external_task_finish(external_task_id, request)
