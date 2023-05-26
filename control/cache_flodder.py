import sys, os
import multiprocessing as mp

PERIOD = 10.0/1000.0 # milliseconds

def child(worker: int) -> None:
    import psutil
    import time

    p = psutil.Process()
    print(f"Child #{worker}: {p}, affinity {p.cpu_affinity()}", flush=True)
    # time.sleep(1)
    p.cpu_affinity([worker])
    print(f"Child #{worker}: Set my affinity to {worker}, affinity now {p.cpu_affinity()}", flush=True)
    # time.sleep(1 + 3 * worker)
    print(f"Child #{worker}: Starting CPU intensive task now on {p.cpu_affinity()}...", flush=True)
    # t_end = time.perf_counter() + 4
    while True:
        os.system("./cacheflodder")
        time.sleep(PERIOD)
    # print(f"Child #{worker}: Finished CPU intensive task on {p.cpu_affinity()}", flush=True)



def main() -> None:
    with mp.Pool() as pool:
        # noinspection PyProtectedMember
        workers: int = pool._processes
        print(f"Running pool with {workers} workers")

        for i in range(workers):
            pool.apply_async(child, (i,))

        # Wait for children to finnish
        pool.close()
        pool.join()

    pass


if __name__ == '__main__':
    main()