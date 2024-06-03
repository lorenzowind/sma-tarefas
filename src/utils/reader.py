from os.path import join, dirname
from yaml import safe_load
from utils.constants import QUEUE_CONFIG_PATH

def read_custom_queues_config_yml() -> dict:
  """ 
  Read the custom queues config from file.

  Returns:
    a list of strings lists
  """
  with open(
    join(dirname(__file__), '../../data/' + QUEUE_CONFIG_PATH), 
    'r',
    encoding="utf8"
  ) as f:
    records = safe_load(f)

  f.close()

  return records
