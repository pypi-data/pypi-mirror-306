import sys,os,re

from .NAPS import NAPS
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.releaser.baijia.BaiJiaSchemaFactory import BaiJiaSchemaFactory
from sele.loginer.baijia.BaiJiaLoginerFactory import BaiJiaLoginerFactory   
from sele.publisher.StandardPublisher import StandardPublisher

class BaiJiaEventsNAPS(NAPS):
  '''
  1. Crawl a materail
  2. Login the publish page
  3. Publish
  4. Set published log
  '''

  def publish(self):
    loginer_factory = BaiJiaLoginerFactory()
    loginer = loginer_factory.create_account()

    factory = BaiJiaSchemaFactory()
    schema = factory.create_events()

    publisher = StandardPublisher(schema,loginer)
    publisher.publish()


