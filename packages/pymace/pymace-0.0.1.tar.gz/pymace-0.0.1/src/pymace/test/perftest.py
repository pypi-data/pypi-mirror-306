import cProfile
import logging
import pstats
import time


def performance_time(repetitions: int, func: callable, *args, output: str = None, **kwargs):
    start = time.perf_counter()
    for _ in range(repetitions):
        func(*args, **kwargs)
    end = time.perf_counter()
    if output == "toConsole":
        took = end - start
        logging.debug(f"took {took:.3f} s, ", end="")
        logging.debug(f"{repetitions/took:.3f} it/s, ", end="")
        logging.debug(f"{took/repetitions*1e3:.3f} ms/it")
        return
    return (end - start) / repetitions


def performance_report(func, *args, **kwargs):
    with cProfile.Profile() as pr:
        func(*args, **kwargs)
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename="need_profiling.prof")
