import sys,os,re

from .NAPS import NAPS
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.releaser.channels.ChannelsSchemaFactory import ChannelsSchemaFactory
from sele.loginer.channels.ChannelsLoginerFactory import ChannelsLoginerFactory   
from sele.publisher.OnceLoginPublisher import OnceLoginPublisher

# don't need spide
class ChannelsVideoNAPS():
  '''
  1. Login the publish page
  2. Upload the video and fill the from
  3. Submit
  '''

  def publish(self):
    loginer = ChannelsLoginerFactory().create_qrcode()
    schema = ChannelsSchemaFactory().create_video()

    publisher = OnceLoginPublisher(schema,loginer)
    publisher.publish()


