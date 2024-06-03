from typing import List
from models.CustomQueue import CustomQueue
from utils import converter, reader
from utils.constants import QUEUE_EXIT_EVENT, QUEUE_INSERT_EVENT, QUEUE_MOVE_EVENT

class Persistance:
  def __init__(self):
    self.initialize_custom_queues()

  def initialize_custom_queues(self):
    """ 
    Initialize the custom queues list.
    """
    self.__custom_queues = converter.convert_dict_to_custom_queues(
      reader.read_custom_queues_config_yml()
    )

  def get_custom_queues(self) -> dict[CustomQueue]:
    """
    Get the custom_queues attribute.
    
    Returns:
      a CustomQueue objects list
    """
    return self.__custom_queues
  
  def find_queue(self, queue_id: int) -> CustomQueue:
    """
    Find the queue by the queue_id attribute.
    
    Args:
      queue_id(int): an integer

    Returns:
      a CustomQueue objects list
    """
    for custom_queue in self.__custom_queues:
      if queue_id == custom_queue.get_queue_id():
        return custom_queue
      
    return None

  def get_event_names(self) -> List[str]:
    """ 
    Map all the event names possible.
    
    Returns:
      a list of strings
    """
    event_names = []
    for custom_queue in self.__custom_queues:
      event_names.append(QUEUE_INSERT_EVENT % (custom_queue.get_queue_id()))
      
      for queue_link in custom_queue.get_queue_links():
        if queue_link.get_queue_id() == -1:
          event_names.append(QUEUE_EXIT_EVENT % (custom_queue.get_queue_id()))
        else:
          event_names.append(QUEUE_MOVE_EVENT % (custom_queue.get_queue_id(), queue_link.get_queue_id()))

    return event_names
