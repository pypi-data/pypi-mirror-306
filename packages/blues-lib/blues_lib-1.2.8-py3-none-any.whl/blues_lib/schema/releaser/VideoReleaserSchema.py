import sys,os,re
from abc import ABC,abstractmethod
from .ReleaserSchema import ReleaserSchema
sys.path.append(re.sub('test.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.schema.SchemaValueReplacer import SchemaValueReplacer     
from util.BluesFiler import BluesFiler
from util.BluesURL import BluesURL
from util.BluesConsole import BluesConsole

class VideoReleaserSchema(ReleaserSchema,ABC):

  CHANNEL = 'video'

  def __init__(self):
    self.limit = {
      'title_max_length':28,
      'video_max_size':'1GB'
    }
    super().__init__()

  def fill_fields(self):
    '''
    Cover the parent's method
    '''
    if not self.fill_atom:
      return

    video_dir = 'D:\short-video'
    files = BluesFiler.readfiles(video_dir)
    file_path = files[0]
    file_name = BluesURL.get_file_name(file_path,False)

    BluesConsole.info(files,'videos')

    material = {
      'material_title':file_name,
      'material_video':file_path,
    }

    request = SchemaValueReplacer().handle({
      'atom':self.fill_atom,
      'value':material, # fetch material by handler
    })

    if request:
      self.material = request['value']
    
