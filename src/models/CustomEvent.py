from typing import List
from heapq import heappop, heappush

class CustomEvent:
  def __init__(self, event_name: str):
    self.__event_name = event_name
    self.__event_list: List[float] = []

  def get_event_name(self) -> int:
    """ 
    Get the event_name attribute.
    
    Returns:
      a string
    """
    return self.__event_name

  def get_event_list(self) -> List[float]:
    """ 
    Get the event_list attribute.
    
    Returns:
      a list of float numbers
    """
    return self.__event_list

  def add_event(self, event_value):
    """ 
    Add an event value to the list using a heap algorithm.
    
    Args:
      event_value(float): a float value
    """
    heappush(self.__event_list, event_value)

  def get_event(self) -> float:
    """ 
    Get an event value from the list using a heap algorithm.
    
    Returns:
      a float
    """
    return heappop(self.__event_list) if len(self.__event_list) > 0 else None
