# -*- coding: utf-8 -*-
from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '600')

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.settings import SettingsWithSidebar
from kivy.properties import DictProperty,ListProperty
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.app import App
from config.settings_panel_config import settingsTemplate

from datetime import datetime
from rsa_spectrum import RSA_DEVICE




FREQ_RANGE_NUM=10




class MeasurementPoint():
    """
    Class of measurment point containning all data according to single measurement point
    """
    def __init__(self,pointName,pointDesc,**kwargs):
        super(MeasurementPoint,self).__init__(**kwargs)
        self.name=pointName
        self.description=pointDesc
        self.id=int(datetime.now().timestamp())
    def __str__(self):
        return self.name

class WarnnigPopup(Popup):
    pass


class NewPointPopup(Popup):
    """
        Class of popup dialiog for creating new measurement point
    """
    def __init__(self,parent_widget,**kwargs):
        super(NewPointPopup,self).__init__(**kwargs)
        self.parent_widget=parent_widget

    def dismiss_add(self):


        if (self.pointName.text!=''):
            for point in self.parent_widget.measurementPointsDict:      #Check if point of that name already exists and prevent adding new one
                if self.parent_widget.measurementPointsDict[point].name==self.pointName.text:
                    popup = WarnnigPopup()
                    popup.open()
                    return True
            newPoint=MeasurementPoint(self.pointName.text,self.pointDesc.text)
            self.parent_widget.measurementPointsDict[newPoint.id]=newPoint
            #print(self.parent_widget.measurementPointsDict.keys())
            self.dismiss()

class Multigen(BoxLayout):
    """
        Main class containning root widget
    """

    measurementPointsDict=DictProperty()
    def __init__(self,**kwargs):
        self.device=RSA_DEVICE()
        super(Multigen,self).__init__(**kwargs)


    def add_measurePoint(self):
        newpoint=NewPointPopup(self)
        newpoint.open()

    def on_measurementPointsDict(self,instance,newPoints):
        """
            Binding for measurementPoints dict change. It updatest spinner list of points.
        """

        #print('Zmiana slownika... Podmeiniam listę')
        self.ids.measurementPoint_spinner.values=[]
        #print(newPoints.keys())
        for point in sorted(newPoints,reverse=True):
            self.ids.measurementPoint_spinner.values.append(newPoints[point].name)
        self.ids.measurementPoint_spinner.text=self.ids.measurementPoint_spinner.values[-1]
        self.selctedNewPoint()


    def selectedNewPoint(self):
        """
            Called when user has changed selection of point in spinner
        """
        self.ids.plotArea.text='Tu będzie wykres dla punktu '+self.ids.measurementPoint_spinner.text

    def rsaConnection(self):
        if self.device.deviceID==1024:
            self.device.search()
            self.device.connect()
        else:
            if self.device.connectionStatus:
                self.device.disconnect()
            else:
                self.device.connect()
        if self.device.connectionStatus:
            self.ids.connection_button_image.source='img/connected.png'
        else:
            self.ids.connection_button_image.source='img/disconnected.png'
        print(self.device.connectionStatus)

class PlotArea(Label):
    pass


class MultigenApp(App):
    def build(self):
        with open('config\gui.kv',encoding='utf8') as kvfile:
            Builder.load_string(kvfile.read())

        multigen=Multigen()
        self.title="Multigen"
        self.settings_cls=SettingsWithSidebar

        #multigen.ids.Gen1Button.text=self.config.get("F1","centerFreq")
        self.use_kivy_settings=False

        return multigen

    def build_config(self,config):
        config.read('config\multigen.ini')
        config.setdefaults('Range1',{'enable':1,'centerFreq':169000000,'span':5000000,'rbw':100000,'reflevel':5000000,'tracelen':4096})
        config.setdefaults('Range2',{'enable':1,'centerFreq':169000000,'span':5000000,'rbw':100000,'reflevel':5000000,'tracelen':4096})
        config.setdefaults('Range3',{'enable':1,'centerFreq':169000000,'span':5000000,'rbw':100000,'reflevel':5000000,'tracelen':4096})
        config.setdefaults('Range4',{'enable':1,'centerFreq':169000000,'span':5000000,'rbw':100000,'reflevel':5000000,'tracelen':4096})
        config.setdefaults('Range5',{'enable':1,'centerFreq':169000000,'span':5000000,'rbw':100000,'reflevel':5000000,'tracelen':4096})
        config.setdefaults('Range6',{'enable':1,'centerFreq':169000000,'span':5000000,'rbw':100000,'reflevel':5000000,'tracelen':4096})
        config.setdefaults('Range7',{'enable':1,'centerFreq':169000000,'span':5000000,'rbw':100000,'reflevel':5000000,'tracelen':4096})
        config.setdefaults('Range8',{'enable':1,'centerFreq':169000000,'span':5000000,'rbw':100000,'reflevel':5000000,'tracelen':4096})
        config.setdefaults('Range9',{'enable':1,'centerFreq':169000000,'span':5000000,'rbw':100000,'reflevel':5000000,'tracelen':4096})

    def build_settings(self,settings):

        for gen_no in range(1,FREQ_RANGE_NUM):
            settings.add_json_panel(u"Zakres {}".format(str(gen_no)),self.config,data=settingsTemplate.format(str(gen_no),str(gen_no)))

    def on_config_change(self, config, section, key, value):
        """
            Function changing button labels on config change.
        """
        if section.startswith("Range"):
            if key=="centerFreq":
                self.root.ids[section+'Button'].text=str(int(self.config.get(section,"centerFreq"))/(1000000)) +" MHz"
            if key=="enable":
                self.root.ids[section+'Button'].disabled=not bool(int(value))
                if self.root.ids[section+'Button'].disabled and self.root.ids[section+'Button'].state=='down':
                    self.root.ids[section+'Button'].state='normal'
                    for rangeButton in reversed(self.root.ids.rangeSelector.children):
                        if rangeButton.disabled==False:
                            rangeButton.state='down'
                            break


if __name__=='__main__':
    MultigenApp().run()
