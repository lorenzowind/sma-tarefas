from typing import List
from models.CustomQueue import CustomQueue
from models.QueueLink import QueueLink

def convert_dict_to_custom_queues(records: dict) -> List[CustomQueue]:
  """ 
  Convert a custom queues records dict to CustomQueue objects list.

  Args:
    records(dict): custom queues records dict

  Returns:
    a CustomQueue objects list
  """
  custom_queues = []

  for record_key in records.keys():
    custom_queue_record = { key : value for record in records[record_key] for key, value in record.items() }

    queue_id = int(record_key)

    capacity = int(custom_queue_record['Capacity']) if 'Capacity' in custom_queue_record else None
    servers = int(custom_queue_record['Servers']) if 'Servers' in custom_queue_record else None
    min_in = int(custom_queue_record['Min_in']) if 'Min_in' in custom_queue_record else None
    max_in = int(custom_queue_record['Max_in']) if 'Max_in' in custom_queue_record else None
    min_out = int(custom_queue_record['Min_out']) if 'Min_out' in custom_queue_record else None
    max_out = int(custom_queue_record['Max_out']) if 'Max_out' in custom_queue_record else None

    queue_links = convert_dict_to_queue_links(custom_queue_record['Queue_links']) if 'Queue_links' in custom_queue_record else None

    custom_queues.append(
      CustomQueue(
        queue_id,
        capacity,
        servers,
        min_in,
        max_in,
        min_out,
        max_out,
        queue_links,
      )
    )
  
  return custom_queues

def convert_dict_to_queue_links(records: List) -> List[QueueLink]:
  """ 
  Convert a queues links records list to QueueLink objects list.

  Args:
    records(dict): queues links records list

  Returns:
    a QueueLink objects list
  """
  queue_links = []

  custom_record = { key : value for record in records for key, value in record.items() }

  for record_key in custom_record.keys():
    queue_id = int(record_key)
    
    probability = float(custom_record[queue_id]) if queue_id in custom_record else None

    queue_links.append(
      QueueLink(
        queue_id,
        probability,
      )
    )
  
  return queue_links