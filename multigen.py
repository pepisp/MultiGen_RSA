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


    def selctedNewPoint(self):
        """
            Called when user has changed selection of point in spinner
        """
        self.ids.plotArea.text='Tu będzie wykres dla punktu '+self.ids.measurementPoint_spinner.text

class PlotArea(Label):
    pass


class MultigenApp(App):
    def build(self):
        with open('config\gui.kv',encoding='utf8') as kvfile:
            Builder.load_string(kvfile.read())

        multigen=Multigen()
        self.title="Multigen"
        self.settings_cls=SettingsWithSidebar

        #multigen.ids.Gen1Button.text=self.config.get("F1","F1Center")
        self.use_kivy_settings=False

        return multigen

    def build_config(self,config):
        config.read('config\multigen.ini')
        config.setdefaults('F1',{'f1enable':1,'f1center':169000000,'f1span':5000000,'f1rbw':100000,'f1reflevel':5000000,'f1tracelen':4096})
        config.setdefaults('F2',{'f2enable':1,'f2center':169000000,'f2span':5000000,'f2rbw':100000,'f2reflevel':5000000,'f2tracelen':4096})
        config.setdefaults('F3',{'f3enable':1,'f3center':169000000,'f3span':5000000,'f3rbw':100000,'f3reflevel':5000000,'f3tracelen':4096})
        config.setdefaults('F4',{'f4enable':1,'f4center':169000000,'f4span':5000000,'f4rbw':100000,'f4reflevel':5000000,'f4tracelen':4096})
        config.setdefaults('F5',{'f5enable':1,'f5center':169000000,'f5span':5000000,'f5rbw':100000,'f5reflevel':5000000,'f5tracelen':4096})
        config.setdefaults('F6',{'f6enable':1,'f6center':169000000,'f6span':5000000,'f6rbw':100000,'f6reflevel':5000000,'f6tracelen':4096})
        config.setdefaults('F7',{'f7enable':1,'f7center':169000000,'f7span':5000000,'f7rbw':100000,'f7reflevel':5000000,'f7tracelen':4096})
        config.setdefaults('F8',{'f8enable':1,'f8center':169000000,'f8span':5000000,'f8rbw':100000,'f8reflevel':5000000,'f8tracelen':4096})
        config.setdefaults('F9',{'f9enable':1,'f9center':169000000,'f9span':5000000,'f9rbw':100000,'f9reflevel':5000000,'f9tracelen':4096})

    def build_settings(self,settings):

        for gen_no in range(1,FREQ_RANGE_NUM):
            settings.add_json_panel(u"Zakres {}".format(str(gen_no)),self.config,data=settingsTemplate.format(str(gen_no),str(gen_no)))

if __name__=='__main__':
    MultigenApp().run()
