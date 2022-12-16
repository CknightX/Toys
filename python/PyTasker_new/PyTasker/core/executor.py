from concurrent.futures import ThreadPoolExecutor

POOL_SIZE = 100

class TaskExecutor:
    pool = ThreadPoolExecutor(max_workers=POOL_SIZE)
    
    @classmethod
    def run(cls,fn):
        cls.pool.submit(fn)
    
    @classmethod
    def stop(cls,fn):
        cls.tpool.shutdown(wait=False,cancel_futures=True)