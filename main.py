import time
from scheduler import *
from task1 import *
from task2 import *
from task3 import *

scheduler = Scheduler()
scheduler.SCH_Init()

task1 = Task1()
task3 = Task3()


scheduler.SCH_Add_Task(task3.Task3_Run, 3000,5000)

scheduler.SCH_Add_Task(task1.Task1_Run, 8000,5000)

while True:
    scheduler.SCH_Update()
    scheduler.SCH_Dispatch_Tasks()
    time.sleep(0.1)
