import time

ORDER = 0
REQ_TASK_RECEPT = 1
TASK_READY_RECEPT = 2
REQ_TASK_CLERK = 3
TASK_READY_CLERK = 4
REQ_TASK_COOKER = 5
TASK_READY_COOKER = 6
PICKUP = 7


def work(seconds):
    time.sleep(seconds)
