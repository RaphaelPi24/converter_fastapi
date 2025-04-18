import time

def progress_bar(duration: float):
    steps = int(duration / 0.2)
    if steps == 0:
        yield 100
        return

    for i in range(steps + 1):
        percent = int((i / steps) * 100)
        yield percent
        time.sleep(0.025)

