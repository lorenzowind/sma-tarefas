from typing import List
from utils.constants import GLIB_LINEAR_A, GLIB_LINEAR_C, GLIB_LINEAR_M

def generate_linear_numbers(numbers: int) -> List[float]:
  """ 
  Generate pseudo random numbers.

  Returns:
    a list of float numbers
  """
  pseudo_numbers = []

  x0 = 12345
  for _ in range(numbers):
    xi = ((GLIB_LINEAR_A * x0) + GLIB_LINEAR_C) % GLIB_LINEAR_M
    x0 = xi
    pseudo_numbers.append(xi / GLIB_LINEAR_M)

  return pseudo_numbers
