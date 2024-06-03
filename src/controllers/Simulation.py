from typing import List
from controllers.Persistance import Persistance
from controllers.Scheduler import Scheduler
from utils.constants import QUEUE_EVENT_SEPARATOR, QUEUE_EXIT_EVENT, QUEUE_INSERT_EVENT, QUEUE_MOVE_EVENT

class Simulation:
  def __init__(self, persistance: Persistance, scheduler: Scheduler):
    self.__persistance = persistance
    self.__scheduler = scheduler
    self.__status_table: List[List[int]] = []

  def update_status_table(self, next_time: float):
    """ 
    Update status table for all queues.
    
    Args:
      next_time(float): a float
    """
    delta_time = next_time - self.__scheduler.get_current_time()
    self.__scheduler.update_current_time(next_time)

    for index, custom_queue in enumerate(self.__persistance.get_custom_queues()):
      if len(self.__status_table[index]) == 0 or custom_queue.get_status() >= len(self.__status_table[index]):
        self.__status_table[index].append(delta_time)
      else:
        self.__status_table[index][custom_queue.get_status()] += delta_time

  def initialize_status_table(self):
    """ 
    Initialize the status table.
    """
    self.__status_table = [[] for _ in range(len(self.__persistance.get_custom_queues()))]

  def print_results(self):
    """ 
    Print results of the simulation.
    """
    for index, custom_queue in enumerate(self.__persistance.get_custom_queues()):
      print()
      print('Queue:', str(custom_queue))
      print('Total time:', self.__scheduler.get_current_time())
      print('Status:', self.__status_table[index])
      print('Probabilities:', [s / self.__scheduler.get_current_time() for s in self.__status_table[index]])
      print('Losses:', str(custom_queue.get_losses()))
    print()

  def handle_insert_event(self, queue_id: int, next_time: float):
    """ 
    Handle an insert event on the queue.
    
    Args:
      queue_id(int): an integer
      next_time(float): a float
    """
    self.update_status_table(next_time)

    custom_queue = self.__persistance.find_queue(queue_id)

    if custom_queue.get_capacity() is None or custom_queue.get_status() < custom_queue.get_capacity():
      custom_queue.event_insertion()

      if custom_queue.get_status() <= custom_queue.get_servers():
        sum = 0.0
        random_number = self.__scheduler.pop_pseudo_random()
        for queue_link in custom_queue.get_queue_links():
          sum = sum + queue_link.get_probability()

          custom_queue_link = self.__persistance.find_queue(queue_link.get_queue_id())

          if random_number < sum:
            if custom_queue_link is None and queue_link.get_queue_id() == -1:
              if len(self.__scheduler.get_pseudo_random()) > 0:
                self.__scheduler.schedule_event([QUEUE_EXIT_EVENT % (queue_id), self.__scheduler.get_next_time_exit(custom_queue)])
            else:
              if len(self.__scheduler.get_pseudo_random()) > 0:
                self.__scheduler.schedule_event([QUEUE_MOVE_EVENT % (queue_id, queue_link.get_queue_id()), self.__scheduler.get_next_time_exit(custom_queue)])
            break
    else:
      custom_queue.event_lose()

    if len(self.__scheduler.get_pseudo_random()) > 0:
      self.__scheduler.schedule_event([QUEUE_INSERT_EVENT % (queue_id), self.__scheduler.get_next_time_insertion(custom_queue)])
  
  def handle_exit_event(self, queue_id: int, next_time: float):
    """ 
    Handle an exit event on the queue.
    
    Args:
      queue_id(int): an integer
      next_time(float): a float
    """
    self.update_status_table(next_time)

    custom_queue = self.__persistance.find_queue(queue_id)

    custom_queue.event_exit()

    if custom_queue.get_status() >= custom_queue.get_servers():
      sum = 0.0
      random_number = self.__scheduler.pop_pseudo_random()
      for queue_link in custom_queue.get_queue_links():
        sum = sum + queue_link.get_probability()

        custom_queue_link = self.__persistance.find_queue(queue_link.get_queue_id())

        if random_number < sum:
          if custom_queue_link is None and queue_link.get_queue_id() == -1:
            if len(self.__scheduler.get_pseudo_random()) > 0:
              self.__scheduler.schedule_event([QUEUE_EXIT_EVENT % (queue_id), self.__scheduler.get_next_time_exit(custom_queue)])
          else:
            if len(self.__scheduler.get_pseudo_random()) > 0:
              self.__scheduler.schedule_event([QUEUE_MOVE_EVENT % (queue_id, queue_link.get_queue_id()), self.__scheduler.get_next_time_exit(custom_queue)])
          break

  def handle_move_event(self, from_queue_id: int, to_queue_id: int, next_time: float):
    """ 
    Handle an event to move to another queue.
    
    Args:
      from_queue_id(int): an integer
      to_queue_id(int): an integer
      next_time(float): a float
    """
    self.update_status_table(next_time)

    from_custom_queue = self.__persistance.find_queue(from_queue_id)

    from_custom_queue.event_exit()

    if from_custom_queue.get_status() >= from_custom_queue.get_servers():
      sum = 0.0
      random_number = self.__scheduler.pop_pseudo_random()
      for queue_link in from_custom_queue.get_queue_links():
        sum = sum + queue_link.get_probability()

        custom_queue_link = self.__persistance.find_queue(queue_link.get_queue_id())

        if random_number < sum:
          if custom_queue_link is None and queue_link.get_queue_id() == -1:
            if len(self.__scheduler.get_pseudo_random()) > 0:
              self.__scheduler.schedule_event([QUEUE_EXIT_EVENT % (from_queue_id), self.__scheduler.get_next_time_exit(from_custom_queue)])
          else:
            if len(self.__scheduler.get_pseudo_random()) > 0:
              self.__scheduler.schedule_event([QUEUE_MOVE_EVENT % (from_queue_id, queue_link.get_queue_id()), self.__scheduler.get_next_time_exit(from_custom_queue)])
          break

    to_custom_queue = self.__persistance.find_queue(to_queue_id)

    if to_custom_queue.get_capacity() is None or to_custom_queue.get_status() < to_custom_queue.get_capacity():
      to_custom_queue.event_insertion()

      if to_custom_queue.get_status() <= to_custom_queue.get_servers() and len(self.__scheduler.get_pseudo_random()) > 0:
        sum = 0.0
        random_number = self.__scheduler.pop_pseudo_random()
        for queue_link in to_custom_queue.get_queue_links():
          sum = sum + queue_link.get_probability()

          custom_queue_link = self.__persistance.find_queue(queue_link.get_queue_id())

          if random_number < sum:
            if custom_queue_link is None and queue_link.get_queue_id() == -1:
              if len(self.__scheduler.get_pseudo_random()) > 0:
                self.__scheduler.schedule_event([QUEUE_EXIT_EVENT % (to_queue_id), self.__scheduler.get_next_time_exit(to_custom_queue)])
            else:
              if len(self.__scheduler.get_pseudo_random()) > 0:
                self.__scheduler.schedule_event([QUEUE_MOVE_EVENT % (to_queue_id, queue_link.get_queue_id()), self.__scheduler.get_next_time_exit(to_custom_queue)])
            break
    else:
      to_custom_queue.event_lose()

  def simulate_model(self):
    """ 
    Start simulation.
    """
    self.initialize_status_table()

    first_event = [QUEUE_INSERT_EVENT % (self.__persistance.get_custom_queues()[0].get_queue_id()), 2.0]
    self.__scheduler.schedule_event(first_event)

    while len(self.__scheduler.get_pseudo_random()) > 0:
      current_event = self.__scheduler.evaluate_events()

      event_info = current_event[0].split(QUEUE_EVENT_SEPARATOR)

      if QUEUE_INSERT_EVENT.startswith(event_info[0]):
        self.handle_insert_event(int(event_info[1]), float(current_event[1]))
      elif QUEUE_EXIT_EVENT.startswith(event_info[0]):
        self.handle_exit_event(int(event_info[1]), float(current_event[1]))
      elif QUEUE_MOVE_EVENT.startswith(event_info[0]):
        self.handle_move_event(int(event_info[2]), int(event_info[4]), float(current_event[1]))

    self.print_results()
