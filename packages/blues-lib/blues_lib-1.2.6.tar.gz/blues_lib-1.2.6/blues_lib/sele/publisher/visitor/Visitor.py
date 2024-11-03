from __future__ import annotations
from abc import ABC, abstractmethod

class Visitor(ABC):
  """
  The Visitor Interface declares a set of visiting methods that correspond to
  component classes. The signature of a visiting method allows the visitor to
  identify the exact class of the component that it's dealing with.
  """
  def __init__(self,starting_index=0,maximum=50):
    # { Publisher }
    self.publisher = None
    # { int } the start option index , sometime the first option is the placehoder, start from 0
    self.starting_index = starting_index
    # { int } the max activity count
    self.maximum = maximum

  @abstractmethod
  def visit_standard(self, publisher: StandardPublisher) -> None:
    pass

  @abstractmethod
  def visit_once_login(self, publisher: OnceLoginPublisher) -> None:
    pass
