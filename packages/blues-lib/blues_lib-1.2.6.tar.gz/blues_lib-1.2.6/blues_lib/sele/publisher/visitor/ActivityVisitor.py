import sys,os,re,time
from .Visitor import Visitor
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BluesLoginChrome import BluesLoginChrome    
from sele.behavior.BehaviorChain import BehaviorChain
from sele.transformer.schema.SchemaSelectorReplacer import SchemaSelectorReplacer
from util.BluesDateTime import BluesDateTime
from util.BluesConsole import BluesConsole

class ActivityVisitor(Visitor):
  '''
  Publish one material several times by select a different activity
  The form has a selection or checkbox field
  '''
  def visit_standard(self,publisher) -> None:
    self.publisher = publisher
    self.publish()

  def visit_once_login(self,publisher) -> None:
    self.publisher = publisher
    self.publish()

  def visit_test(self,publisher,callback) -> None:
    self.publisher = publisher
    rows = []
    for i in range(3):
      self.set_activity_atom(i+1)
      callback(self.publisher.schema)

  # concreate calculate
  def publish(self):
    if not self.publisher.material:
      BluesConsole.error('No available materials')
      return False

    self.publisher.login()
    self.release()
    self.publisher.quit()
  
  def release(self):
    options = self.get_activity_options()
    if not options:
      BluesConsole.error('No activity options')
      return 

    BluesConsole.info('There are currently %s activities: ' % (len(options),options))
    
    range_value = len(options) - self.starting_index
    for i in range(range_value):
      nth = i+1
      BluesConsole.info('release %sth activity: %s' % (nth,options[i]))

      # replace the activity element selector dynamically
      self.set_activity_atom(nth)

      # releae the material
      self.publisher.release()

      if nth>=self.maximum:
        BluesConsole.info('Reach the maximum: %s' % self.maximum)
        break

  def get_activity_options(self):
    # { ValueAtom } : the value is a dict {'switch': Atom, 'brief': Atom}
    if not self.publisher.schema.activity_atom:
      return None
    
    activity_atom_dict = self.publisher.schema.activity_atom.get_value()
    if not activity_atom_dict:
      return None

    self.publisher.browser.open(self.publisher.url) 

    switch_atom = activity_atom_dict.get('switch')
    brief_atom = activity_atom_dict.get('brief')

    if switch_atom:
      # switch to show the activity selection
      handler = BehaviorChain(self.browser,switch_atom)
      handler.handle()
      # wait the options render
      BluesDateTime.count_down({'duration':3,'title':'Wait for the activity options to render'})

    handler = BehaviorChain(self.browser,brief_atom)
    outcome = handler.handle()
    if outcome.data:
      return outcome.data
    else:
      return None
    
  def set_activity_atom(self,nth):
    '''
    Set the activity option
    Parameter:
      nth {int} : the option's index, start from 1 xx:nth-of-type(nth)
    '''
    request = {
      'atom': self.publisher.schema.fill_atom,
      'value':{
        'activity_nth':nth
      }
    }
    handler = SchemaSelectorReplacer()
    handler.handle(request)

