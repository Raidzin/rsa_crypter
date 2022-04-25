import time

SEC_FORMAT = 'Осталось {} сек'
MIN_FORMAT = 'Осталось {0} мин, {1} сек'


def format_time(time_in_seconds):
    if time_in_seconds < 60:
        return SEC_FORMAT.format(
            round(time_in_seconds)
        )
    else:
        return MIN_FORMAT.format(
            round(time_in_seconds / 60),
            round(time_in_seconds % 60),
        )


class Timer:
    def __init__(self, total_chunks_count):
        self._start_time = 0
        self.total_chunks_count = total_chunks_count

    @property
    def spent_time(self):
        return time.time() - self._start_time

    def start(self):
        self._start_time = time.time()

    def get_waiting_time(self, current_chunk_number):
        return format_time(self.spent_time / current_chunk_number *
                           (self.total_chunks_count - current_chunk_number))


if __name__ == '__main__':
    total = 2000
    timer = Timer(total)
    timer.start()
    for i in range(1, total + 1):
        print(timer.get_waiting_time(i))
        time.sleep(0.1)
