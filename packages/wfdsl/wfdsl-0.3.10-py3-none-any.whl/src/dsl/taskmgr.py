from concurrent.futures.thread import ThreadPoolExecutor

class TaskManager():
    def __init__(self, max_count = 5):
        self.pool = ThreadPoolExecutor(max_count)
        self.futures = []
        
    def submit_func(self, func, *args):
        self.cleanup_pool()
        future = self.pool.submit(func, *args)
        self.futures.append(future)
    
    def submit(self, argv):
        self.cleanup_pool()
        future = self.pool.submit(check_output, ' '.join(argv), shell=True)
        self.futures.append(future)
        return future.result()
        
    def cleanup_pool(self):
        self.futures = list(filter(lambda f : f and not f.done(), self.futures))
    
    def wait(self):
        for future in self.futures:
            future.result() # blocks and forward exceptions
            
    def idle(self):
        '''
        True if no task is running
        '''
        for future in self.futures:
            if not future.done():
                return False
        return True