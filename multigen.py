# -*- coding: utf-8 -*-
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.settings import SettingsWithSidebar
from kivy.lang import Builder
from kivy.app import App



class Multigen(BoxLayout):
    # def __init__(self,**kwargs):
    #     super(Multigen,self).__init__(**kwargs)
    #     self.ids.Gen1Button.text=app.config.get("F1","F1Center")
    pass

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
        config.setdefaults('F1',{'f1enable':True,'f1center':169000000,'f1span':5000000,'f1rbw':100000,'f1reflevel':5000000,'f1tracelen':4096})

    def build_settings(self,settings):
        with open('config\settings.json',encoding='utf8') as settingsfile:
            settings.add_json_panel(u"Ustawienia dla generatora 1",self.config,data=settingsfile.read())


if __name__=='__main__':
    MultigenApp().run()
