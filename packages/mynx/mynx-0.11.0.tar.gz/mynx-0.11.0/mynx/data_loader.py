from abc import ABC, abstractmethod
import multiprocessing as mp
from time import sleep
import warnings

from mynx.callbacks import Callback
from mynx.logs import Logs
from mynx.src import Cycle

class DataLoader(Callback, ABC):
    def __init__(self, use_multiprocesing:bool = True, num_workers:int = None, max_queued_batches: int = 8, warmup_queue:bool = True, disable_warnings:bool = False):
        if not num_workers:
            num_workers = mp.cpu_count()
        self.use_multiprocesing = use_multiprocesing
        self.num_workers = num_workers
        self.max_queued_batches = max_queued_batches
        self.warmup_queue = warmup_queue
        self.disable_warnings = disable_warnings

        self.get_batch_idx = Cycle(range(len(self)))

        if use_multiprocesing:
            self._batch_queue = mp.Queue(self.max_queued_batches)
            self._task_queues = [mp.Queue() for _ in range(num_workers)]

            self._workers = [mp.Process(target=self._worker, args=(queue,), daemon=True) for queue in self._task_queues]

            for worker in self._workers:
                worker.start()

    def start(self):
        if not self.use_multiprocesing:
            return
        for _ in range(self.max_queued_batches):
            batch_idx = next(self.get_batch_idx)
            self._task_queues[batch_idx % self.num_workers].put(batch_idx)

        while self.warmup_queue and not self._batch_queue.full():
            sleep(0.1)

    @abstractmethod
    def __len__(self):
        ...

    @abstractmethod
    def get_batch(self, idx:int):
        ...

    def _worker(self, queue:mp.Queue):
        while True:
            batch_idx = queue.get()
            batch = self.get_batch(batch_idx)
            self._batch_queue.put(batch)

    def on_step_start(self, step:int, logs:Logs):
        logs.batch = next(self)

    def __next__(self):
        if not self.use_multiprocesing:
            return self.get_batch(next(self.get_batch_idx))
        
        if not self.disable_warnings and self._batch_queue.qsize() == 0:
            warnings.warn(f"Batches are not preparing fast enought. Consider optimizing `{self.__class__.__name__}.{self.get_batch.__name__}` method")
        
        batch = self._batch_queue.get()
        batch_idx = next(self.get_batch_idx)
        self._task_queues[batch_idx % self.num_workers].put(batch_idx)
        return batch
    
    def terminate(self):
        if not self.use_multiprocesing:
            return
        
        for worker in self._workers:
            worker.terminate()
            worker.join()