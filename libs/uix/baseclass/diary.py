# -*- coding: utf-8 -*-
#
# This file created with KivyCreatorProject
# <https://github.com/HeaTTheatR/KivyCreatorProgect
#
# Copyright © 2017 Easy
#
# For suggestions and questions:
# <kivydevelopment@gmail.com>
# 
# LICENSE: MIT



from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class Diary(Screen):
    mail_to = ObjectProperty()
    theme = ObjectProperty()
    add_mail = ObjectProperty()
    user_name = ObjectProperty()
    comment = ObjectProperty()


