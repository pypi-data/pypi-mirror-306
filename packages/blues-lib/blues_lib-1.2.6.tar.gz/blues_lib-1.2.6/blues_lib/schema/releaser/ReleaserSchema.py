import sys,os,re
from abc import ABC,abstractmethod
sys.path.append(re.sub('test.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.schema.SchemaTransformerChain import SchemaTransformerChain     
from atom.AtomFactory import AtomFactory     
from atom.Atom import Atom
from pool.BluesMaterialIO import BluesMaterialIO

class ReleaserSchema(ABC):
  
  DEFAULT_LIMIT = {
    'title_max_length':28,
    'content_max_length':2000,
    'image_max_length':9
  }

  CHANNEL = 'events'

  def __init__(self):

    self.atom_factory = AtomFactory()

    # { dict } standard material data entiry
    self.material = None
    
    # declare atom fields
    # { URLAtom } the form page
    self.url_atom = None
    # { ArrayAtom } the form controller atom list
    self.fill_atom = None
    # { ArrayAtom } the preview atom list
    self.preview_atom = None
    # { ArrayAtom } the submit atom list
    self.submit_atom = None
    # { ArrayAtom } the modal atom list, should be closed
    self.popup_atom = None
    # { ArrayAtom } the activity atom
    self.activity_atom = None
    
    # create atoms fields
    self.create_fields()

    # fillin the material value ,must after fields created
    self.fill_fields()
  
  def create_fields(self):
    self.create_url_atom()
    self.create_fill_atom()
    self.create_preview_atom()
    self.create_submit_atom()
    self.create_popup_atom()
    self.create_activity_atom()

  def fill_fields(self):
    '''
    Replace the placeholder in the schema by the materail entity data
    '''
    if not self.fill_atom:
      return

    if hasattr(self,'limit') and self.limit:
      limit = {**self.DEFAULT_LIMIT,**self.limit}
    else:
      limit = self.DEFAULT_LIMIT

    request = SchemaTransformerChain().handle({
      'atom':self.fill_atom,
      'value':None, # fetch material by handler
      'limit':limit
    })

    if request:
      self.material = request['value']
  
  @abstractmethod
  def create_url_atom(self):
    pass

  @abstractmethod
  def create_fill_atom(self):
    pass

  @abstractmethod
  def create_preview_atom(self):
    pass

  @abstractmethod
  def create_submit_atom(self):
    pass

  @abstractmethod
  def create_popup_atom(self):
    pass

  @abstractmethod
  def create_activity_atom(self):
    pass

