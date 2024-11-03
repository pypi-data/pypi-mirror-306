import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.releaser.VideoReleaserSchema import VideoReleaserSchema

class ChannelsVideoSchema(VideoReleaserSchema):

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('Video page','https://channels.weixin.qq.com/platform/post/create')

  def create_fill_atom(self):
    atoms = [
      # select activity
      self.atom_factory.createClickable('show activity dialog','.activity-display-wrap'),
      self.atom_factory.createInput('activity title','.activity-filter-wrap input','material_title'),
      self.atom_factory.createClickable('select a activity','','.activity-filter-wrap .option-item:nth-of-type(${activity_nth})'),
      # upload video
      self.atom_factory.createFile('video','.ant-upload input','material_video'),
    ]

    self.fill_atom = self.atom_factory.createArray('fields',atoms)

  def update_selector(self,field,template_dict):
    '''
    Don't change the atom's value ,update the selector by template
    Paramters:
      member { str } : current class's member
      template_dict {dict} : the replacement dict
        - key : the plachoder in selector
        - value : the real value
    '''
    pass


  def create_preview_atom(self):
    return None

  def create_submit_atom(self):
    atoms = [
      self.atom_factory.createClickable('submit','.form-btns .weui-desktop-btn_primary'),
    ]
    self.submit_atom = self.atom_factory.createArray('submit',atoms)

  def create_popup_atom(self):
    return None

  def create_activity_atom(self):
    unit_selector = '.activity-filter-wrap .option-item'
    field_atoms = [
      self.atom_factory.createText('title','.activity-item-info'),
    ]
    array_atom = self.atom_factory.createArray('fields',field_atoms) 
    brief_atom = self.atom_factory.createBrief('briefs',unit_selector,array_atom) 

    switch_atoms = [
      self.atom_factory.createClickable('show activity dialog','.activity-display-wrap'),
      self.atom_factory.createInput('activity title','.activity-filter-wrap input','妈妈我想你'),
    ]
    switch_atom = self.atom_factory.createArray('switch',switch_atoms) 
    atom_map = {
      'switch':switch_atom,
      'brief':brief_atom,
    }

    self.activity_atom = self.atom_factory.createData('activity map',atom_map)
