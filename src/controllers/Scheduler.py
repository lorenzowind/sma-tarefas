from typing import List
from models.CustomEvent import CustomEvent
from models.CustomQueue import CustomQueue
from utils.linear_generator import generate_linear_numbers

class Scheduler:
  def __init__(self, event_names: List[str], numbers_to_generate: int):
    self.initialize_custom_events(event_names)
    self.__pseudo_random = generate_linear_numbers(numbers_to_generate)
    self.__current_time = 0.0

  def initialize_custom_events(self, event_names: List[str]):
    """ 
    Initialize the custom events dict with all event names passed as parameters.
    
    Args:
      event_names(List[str]): a list of strings
    """
    self.__custom_events = {}
    for event_name in event_names:
      self.__custom_events[event_name] = CustomEvent(event_name)

  def get_current_time(self) -> float:
    """ 
    Get the current_time attribute.
    
    Returns:
      a float
    """
    return self.__current_time

  def update_current_time(self, next_time: float):
    """ 
    Update the current_time attribute.
    
    Args:
      a float
    """
    self.__current_time = next_time

  def get_next_time_insertion(self, custom_queue: CustomQueue) -> float:
    """ 
    Get a next time value with a pseudo random number for an insertion event.
    
    Args:
      custom_queue(CustomQueue): an object of the queue
    
    Returns:
      a float
    """
    return custom_queue.generate_insertion(self.pop_pseudo_random()) + self.__current_time

  def get_next_time_exit(self, custom_queue: CustomQueue) -> float:
    """ 
    Get a next time value with a pseudo random number for an exit event.
    
    Args:
      custom_queue(CustomQueue): an object of the queue
    
    Returns:
      a float
    """
    return custom_queue.generate_exit(self.pop_pseudo_random()) + self.__current_time
  
  def get_pseudo_random(self) -> List[float]:
    """ 
    Get the pseudo_random attribute.
    
    Returns:
      a list of float number
    """
    return self.__pseudo_random
  
  def pop_pseudo_random(self) -> float:
    """ 
    Pop a pseudo_random number.
    
    Returns:
      a float
    """
    return self.__pseudo_random.pop(0)

  def evaluate_events(self) -> tuple[str, float]:
    """ 
    Evaluate the events to get the minor time value.
    
    Returns:
      a pair with the event name and the time value
    """
    evaluated_events = []
    for event_key in self.__custom_events.keys():
      event = self.__custom_events[event_key].get_event()
      if not event is None:
        evaluated_events.append((event_key, event))

    next_event = None
    for evaluated_event in evaluated_events:
      if next_event is None or evaluated_event[1] < next_event[1]:
        next_event = evaluated_event

    for evaluated_event in evaluated_events:
      if next_event is None or evaluated_event[0] != next_event[0]:
        self.__custom_events[evaluated_event[0]].add_event(evaluated_event[1])

    return next_event

  def schedule_event(self, event_tuple: tuple[str, float]):
    """ 
    Schedule the event.
    
    Args:
      event_tuple(tuple[str, float]): a tuple with the event name and the time value
    """
    if event_tuple[0] in self.__custom_events:
      self.__custom_events[event_tuple[0]].add_event(event_tuple[1])