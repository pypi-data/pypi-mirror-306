import sys,os,re,json
from .ChannelsVideoSchema import ChannelsVideoSchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.releaser.ReleaserSchemaFactory import ReleaserSchemaFactory

class ChannelsSchemaFactory(ReleaserSchemaFactory):

  def create_video(self):
    return ChannelsVideoSchema()
