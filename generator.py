import time

def progress_bar(duration: float):
    steps = int(duration / 0.1)
    if steps == 0:
        yield 100
        return

    for i in range(steps + 1):
        percent = int((i / steps) * 100)
        yield percent
        time.sleep(0.1)


for i in progress_bar(5.7):
    print(f'прогресс {i}%')