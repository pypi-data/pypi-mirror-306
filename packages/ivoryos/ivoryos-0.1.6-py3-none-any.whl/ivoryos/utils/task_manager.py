import threading
import queue
import time


# A task manager class to manage the queue and tasks
class TaskManager:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.current_task = None
        self.stop_event = threading.Event()

    def add_task(self, func, **kwargs):
        # Add the function and its kwargs to the task queue
        self.task_queue.put((func, kwargs))

    def run_tasks(self):
        # Run the tasks from the queue
        while not self.task_queue.empty():
            func, kwargs = self.task_queue.get()
            thread = threading.Thread(target=self.run_task, args=(func, kwargs))
            self.current_task = thread
            thread.start()
            thread.join()  # Wait for the task to finish

    def run_task(self, func, kwargs):
        # Run the task function with control to stop in the middle
        self.stop_event.clear()  # Reset the stop flag
        func(**kwargs)
        if self.stop_event.is_set():
            print("Current task was stopped.")

    def stop_current_task(self):
        # Stop the current task by setting the stop flag
        if self.current_task and self.current_task.is_alive():
            print("Stopping current task...")
            self.stop_event.set()  # Signal to stop the current task
            self.current_task.join()  # Wait for the task to stop


# Wrapping tasks to allow stopping between them
def function_to_call(stop_event, **kwargs):
    if stop_event.is_set():
        return
    task1(kwargs['arg1'])
    if stop_event.is_set():
        return
    task2(kwargs['arg2'])


# Dummy task functions as provided
def task1(arg1):
    for i in range(arg1):
        print(f"Task 1 running: {i}")
        time.sleep(1)


def task2(arg2):
    for i in range(arg2):
        print(f"Task 2 running: {i}")
        time.sleep(1)


if __name__ == "__main__":
    manager = TaskManager()

    # Add tasks to the manager
    manager.add_task(function_to_call, stop_event=manager.stop_event, arg1=3, arg2=5)
    manager.add_task(function_to_call, stop_event=manager.stop_event, arg1=2, arg2=4)

    # Run tasks in a separate thread
    manager_thread = threading.Thread(target=manager.run_tasks)
    manager_thread.start()

    # Example: Stop the current workflow while task1 is running
    time.sleep(2)  # Let task1 run for a bit
    manager.stop_current_task()

    # Wait for all tasks to finish
    manager_thread.join()
