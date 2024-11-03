from abc import ABC,abstractmethod

class ReaderSchemaFactory():
  @abstractmethod
  def create_news(self):
    pass

  @abstractmethod
  def create_gallery(self):
    pass
