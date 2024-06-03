class QueueLink:
  def __init__(self, queue_id: int, probability: float):
    self.__queue_id = queue_id
    self.__probability = probability

  def get_queue_id(self) -> int:
    """ 
    Get the queue_id attribute.
    
    Returns:
      an integer
    """
    return self.__queue_id

  def get_probability(self) -> float:
    """ 
    Get the probability attribute.
    
    Returns:
      a float number
    """
    return self.__probability
  
  def __str__(self):
    result = '{'
    result = result + ' Queue_id=' + str(self.get_queue_id())
    result = result + ' : Probability=' + str(self.get_probability())
    result = result + ' }'

    return result
