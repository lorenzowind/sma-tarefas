from typing import List
from models.QueueLink import QueueLink

class CustomQueue:
  def __init__(
    self,
    queue_id: int = None, 
    capacity: int = None, 
    servers: int = None, 
    min_in: int = None, 
    max_in: int = None, 
    min_out: int = None, 
    max_out: int = None,
    queue_links: List[QueueLink] = None,
  ):
    self.__queue_id = queue_id
    self.__capacity = capacity
    self.__servers = servers
    self.__min_in = min_in
    self.__max_in = max_in
    self.__min_out = min_out
    self.__max_out = max_out
    self.__queue_links = queue_links
    self.__status = 0
    self.__losses = 0

  def get_queue_id(self) -> int:
    """ 
    Get the queue_id attribute.
    
    Returns:
      an integer
    """
    return self.__queue_id

  def get_capacity(self) -> int:
    """ 
    Get the capacity attribute.
    
    Returns:
      an integer
    """
    return self.__capacity

  def get_servers(self) -> int:
    """ 
    Get the servers attribute.
    
    Returns:
      an integer
    """
    return self.__servers

  def get_min_in(self) -> int:
    """ 
    Get the min_in attribute.
    
    Returns:
      an integer
    """
    return self.__min_in

  def get_max_in(self) -> int:
    """ 
    Get the max_in attribute.
    
    Returns:
      an integer
    """
    return self.__max_in

  def get_min_out(self) -> int:
    """ 
    Get the min_out attribute.
    
    Returns:
      an integer
    """
    return self.__min_out

  def get_max_out(self) -> int:
    """ 
    Get the max_out attribute.
    
    Returns:
      an integer
    """
    return self.__max_out

  def get_queue_links(self) -> List[QueueLink]:
    """ 
    Get the queue_links attribute.
    
    Returns:
      a QueueLink objects list
    """
    return self.__queue_links
  
  def get_status(self) -> int:
    """ 
    Get the status attribute.
    
    Returns:
      an integer
    """
    return self.__status
  
  def get_losses(self) -> int:
    """ 
    Get the losses attribute.
    
    Returns:
      an integer
    """
    return self.__losses

  def event_insertion(self):
    """ 
    Increase the status of the queue.
    """
    self.__status += 1

  def event_exit(self):
    """ 
    Decrease the status of the queue.
    """
    self.__status -= 1

  def event_lose(self):
    """ 
    Increase the number of losses of the queue.
    """
    self.__losses += 1

  def generate_insertion(self, pseudo_random: float) -> float:
    """ 
    Calculate the generation number for an event of queue insertion.
    
    Args:
      pseudo_random(float): a pseudo random number

    Returns:
      a float
    """
    return pseudo_random * (self.__max_in - self.__min_in) + self.__min_in

  def generate_exit(self, pseudo_random: float) -> float:
    """ 
    Calculate the generation number for an event of queue exit.
    
    Args:
      pseudo_random(float): a pseudo random number
    
    Returns:
      a float
    """
    return pseudo_random * (self.__max_out - self.__min_out) + self.__min_out
  
  def __str__(self):
    result = '{'

    if not self.get_queue_id() is None:
      result = result + ' Queue_id=' + str(self.get_queue_id())

    if not self.get_capacity() is None:
      result = result + ' : Capacity=' + str(self.get_capacity())

    if not self.get_servers() is None:
      result = result + ' : Servers=' + str(self.get_servers())

    if not self.get_min_in() is None:
      result = result + ' : Min_in=' + str(self.get_min_in())

    if not self.get_max_in() is None:
      result = result + ' : Max_in=' + str(self.get_max_in())

    if not self.get_min_out() is None:
      result = result + ' : Min_out=' + str(self.get_min_out())

    if not self.get_max_out() is None:
      result = result + ' : Max_out=' + str(self.get_max_out())

    if not self.get_queue_links() is None:
      queue_links = []
      for queue_link in self.get_queue_links():
        queue_links.append(str(queue_link))
      result = result + ' : Queue_links=' + str(queue_links)
    
    result = result + ' }'

    return result
