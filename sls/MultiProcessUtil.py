# General imports
import sys, warnings
import multiprocessing
warnings.filterwarnings('ignore')

from multiprocessing import Queue, Process, Manager

def worker(tasks, ress, func):
    while True:
        try:
            param = tasks.get(timeout=1)
        except Exception as e:
            break
        res = func(param)
        ress.put(res)    

def manager(params, func, process_num=16):
    tasks = Manager().Queue()
    ress  = Manager().Queue()
    proceses = []
    results  = []

    print('creating params')
    for i, p in enumerate(params):
        print('\r {}'.format(i),end="")
        tasks.put(p)
    
    task_num = tasks.qsize()
    
    print('starting process')
    for i in range(process_num):
        p = Process(
            target = worker,
            args   = (tasks, ress, func)
        )
        proceses.append(p)
        p.start()
        
    print('wait response')
    
    for i in range(task_num):
        res = ress.get()
        results.append(res)
        if i % 10 == 0:
            sys.stdout.write("\r fin task: {}/{}".format(i, task_num))
            sys.stdout.flush() 

    print('wait process')
    for p in proceses:
        p.join()       
    return results
