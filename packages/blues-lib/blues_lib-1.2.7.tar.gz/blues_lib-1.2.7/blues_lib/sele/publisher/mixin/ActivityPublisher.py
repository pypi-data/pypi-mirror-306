import sys,os,re,time
from abc import ABC,abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BluesLoginChrome import BluesLoginChrome    
from sele.behavior.BehaviorChain import BehaviorChain
from sele.transformer.schema.SchemaSelectorReplacer import SchemaSelectorReplacer
from util.BluesConsole import BluesConsole

class ActivityPublisher(ABC):
  '''
  Use one some form data
  Publish multi times by choose a diff activities
  '''
  def publish_all_activities(self):
    if not self.material:
      BluesConsole.error('No available materials')
      return False

    self.login()
    self.release_all_activities()
    self.quit()
  
  def release_all_activities(self):
    options = self.get_activity_options()
    if not options:
      BluesConsole.error('No activity options')
      return 

    BluesConsole.info('Activity count: %s ' % len(options))
    max_idx = 50
    for i in range(len(options)-2):
      BluesConsole.info('release %s activity: %s' % ((i+1),options[i]))
      # start from 2
      self.set_activity_atom(i+2)
      self.release()
      if i>=max_idx:
        break

  def get_activity_options(self):
    if not self.schema.activity_atom:
      return None
    self.browser.open(self.url) 
    activity_map = self.schema.activity_atom.get_value()
    switch_atom = activity_map.get('switch')
    brief_atom = activity_map.get('brief')
    if switch_atom:
      handler = BehaviorChain(self.browser,switch_atom)
      handler.handle()
      # wait the options render
      time.sleep(3)

    handler = BehaviorChain(self.browser,brief_atom)
    outcome = handler.handle()
    if outcome.data:
      return outcome.data
    else:
      return None
    
  def set_activity_atom(self,idx):
    request = {
      'atom': self.schema.fill_atom,
      'value':{
        'activity_idx':idx
      }
    }
    handler = SchemaSelectorReplacer()
    handler.handle(request)

