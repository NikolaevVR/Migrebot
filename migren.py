

import os
import sys
import smtplib
from ast import literal_eval

from kivy.app import App

from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex, get_hex_from_color
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty

from main import __version__
from libs.translation import Translation
from libs.uix.baseclass.startscreen import StartScreen
from libs.uix.lists import Lists
from libs.utils.showplugins import ShowPlugins

from kivymd.theming import ThemeManager
#from kivymd.uix.label import MDLabel
#from kivymd.label import MDLabel

from toast import toast
from dialogs import card

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label

import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import xlrd
import xlwt

from xlutils.copy import copy
from datetime import datetime




class Migren(App):
    title = 'Дневник головной боли'
    icon = 'icon.png'
    nav_drawer = ObjectProperty()
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Grey'
    lang = StringProperty('en')


    def __init__(self, **kvargs):
        super(Migren, self).__init__(**kvargs)
        Window.bind(on_keyboard=self.events_program)
        Window.soft_input_mode = 'below_target'

        self.list_previous_screens = ['base']
        self.window = Window
        self.plugin = ShowPlugins(self)
        self.config = ConfigParser()
        self.manager = None
        self.window_language = None
        self.exit_interval = False
        self.dict_language = literal_eval(
            open(
                os.path.join(self.directory, 'data', 'locales', 'locales.txt')).read()
        )
        self.translation = Translation(
            self.lang, 'Ttest', os.path.join(self.directory, 'data', 'locales')
        )

    def get_application_config(self):
        return super(Migren, self).get_application_config(
                        '{}/%(appname)s.ini'.format(self.directory))

    def build_config(self, config):

        config.adddefaultsection('General')
        config.setdefault('General', 'language', 'en')

    def set_value_from_config(self):
        self.config.read(os.path.join(self.directory, 'migren.ini'))
        self.lang = self.config.get('General', 'language')

    def build(self):
        self.set_value_from_config()
        self.load_all_kv_files(os.path.join(self.directory, 'libs', 'uix', 'kv'))
        self.screen = StartScreen()
        self.manager = self.screen.ids.manager
        self.nav_drawer = self.screen.ids.nav_drawer

        return self.screen

    def load_all_kv_files(self, directory_kv_files):
        for kv_file in os.listdir(directory_kv_files):
            kv_file = os.path.join(directory_kv_files, kv_file)
            if os.path.isfile(kv_file):
                with open(kv_file, encoding='utf-8') as kv:
                    Builder.load_string(kv.read())

    def events_program(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.nav_drawer.state == 'open':
                self.nav_drawer.toggle_nav_drawer()
            self.back_screen(event=keyboard)
        elif keyboard in (282, 319):
            pass

        return True

    def back_screen(self, event=None):
        if event in (1001, 27):
            if self.manager.current == 'base':
                self.dialog_exit()
                return
            try:
                self.manager.current = self.list_previous_screens.pop()
            except:
                self.manager.current = 'base'
            self.screen.ids.action_bar.title = self.title
            self.screen.ids.action_bar.left_action_items = \
                [['menu', lambda x: self.nav_drawer._toggle()]]


    def add_note(self, *args):
        #self.screen.ids.base.add_name_previous_screen()
        #self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'note'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen(27)]]

    def add_note2(self, *args):
        #self.screen.ids.base.add_name_previous_screen()
        #self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'note2'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen(27)]]

    def add_note3(self, *args):
        #self.screen.ids.base.add_name_previous_screen()
        #self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'note3'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen(27)]]



    def show_diary(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'diary'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen(27)]]

    def send_email(self, *args):
        addr_from = "MigreDiary@yandex.ru"  # Отправитель
        password = "VladNik98"  # Пароль

        msg = MIMEMultipart()  # Создаем сообщение
        msg['From'] = addr_from  # Адресат
        msg['To'] = self.screen.ids.diary.ids.mail_to.text  # Получатель
        msg['Subject'] = self.screen.ids.diary.ids.theme.text  # Тема сообщения
        users_name = self.screen.ids.diary.ids.user_name.text.replace(' ', '_')
        name = 'diary.xls'
        filepath = os.path.join(os.getcwd(), name)
        filename = os.path.basename(filepath)
        if os.path.isfile(filepath):
            rb = xlrd.open_workbook(filepath, formatting_info=True)
            wb = copy(rb)
            wb.save(users_name+'_diary.xls')
            os.remove(filepath)
        name = users_name+'_diary.xls'
        filepath = os.path.join(os.getcwd(), name)
        filename = os.path.basename(filepath)

        body = 'Дневник головной боли:\n\nПациент: '+ self.screen.ids.diary.ids.user_name.text + '\n'+\
                'Комментарий пациента: ' + self.screen.ids.diary.ids.comment.text + '\n\n' +\
            'Адресс для обратной связи: ' + self.screen.ids.diary.ids.add_mail.text  # Текст сообщения
        msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

        if os.path.isfile(filepath):  # Если файл существует
            ctype, encoding = mimetypes.guess_type(filepath)  # Определяем тип файла на основе его расширения
            if ctype is None or encoding is not None:  # Если тип файла не определяется
                ctype = 'application/octet-stream'  # Будем использовать общий тип
            maintype, subtype = ctype.split('/', 1)  # Получаем тип и подтип
            with open(filepath, 'rb') as fp:
                file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
                file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
                fp.close()
            encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
            file.add_header('Content-Disposition', 'attachment', filename=filename)  # Добавляем заголовки
            msg.attach(file)  # Присоединяем файл к сообщению

        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)  # Создаем объект SMTP
        server.login(addr_from, password)  # Получаем доступ
        server.send_message(msg)  # Отправляем сообщение
        server.quit()  # Выходим

        rb = xlrd.open_workbook(filepath, formatting_info=True)
        wb = copy(rb)
        wb.save(users_name+'_old_diary.xls')

        self.create_new_table(name)

        toast(self.translation._('Дневник отправлен'))
        self.screen.ids.diary.ids.mail_to.text = ''
        self.screen.ids.diary.ids.theme.text = ''
        self.screen.ids.diary.ids.comment.text = ''

    def create_new_table(self, name, *args):
        font0 = xlwt.Font()
        font0.name = 'Times New Roman'
        font0.bold = True
        style0 = xlwt.XFStyle()
        style0.font = font0
        style1 = xlwt.XFStyle()
        style1.num_format_str = 'D-MMM-YY'
        sheet = str(datetime.now())
        sheet = sheet[0:10]
        wb = xlwt.Workbook()
        ws = wb.add_sheet(sheet)
        Col = ws.col(0)
        Col.width = 256 * 21
        ws.write(0, 0, 'Дата и время', style0)
        Col = ws.col(1)
        Col.width = 256 * 41
        ws.write(0, 1, 'Тип боли', style0)
        Col = ws.col(2)
        Col.width = 256 * 41
        ws.write(0, 2, 'Локализация боли', style0)
        Col = ws.col(3)
        Col.width = 256 * 23
        ws.write(0, 3, 'Продолжительность боли', style0)
        Col = ws.col(4)
        Col.width = 256 * 65
        ws.write(0, 4, 'Комментарий пациента', style0)
        wb.save(name)



    def show_plugins(self, *args):
        self.plugin.show_plugins()

    def show_about(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.screen.ids.about.ids.label.text = \
            self.translation._(
                u'[size=20][b]PyConversations[/b][/size]\n\n'
                u'[b]Version:[/b] {version}\n'
                u'[b]License:[/b] MIT\n\n'
                u'[size=20][b]Developer[/b][/size]\n\n'
                u'[ref=SITE_PROJECT]'
                u'[color={link_color}]Pechka and Bomj[/color][/ref]\n\n'
                u'[b]Source code:[/b] '
                u'[ref=https://github.com/NikolaevVR/Migrebot]'
                u'[color={link_color}]GitHub[/color][/ref]').format(
                version=__version__,
                link_color=get_hex_from_color(self.theme_cls.primary_color)
            )
        self.manager.current = 'about'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen(27)]]

   # def show_license(self, *args):
   #     self.screen.ids.license.ids.text_license.text = \
   #         self.translation._('%s') % open(
   #             os.path.join(self.directory, 'LICENSE'), encoding='utf-8').read()
    #    self.nav_drawer._toggle()
    #    self.manager.current = 'license'
    #    self.screen.ids.action_bar.left_action_items = \
    #        [['chevron-left', lambda x: self.back_screen()]]
    #    self.screen.ids.action_bar.title = \
    #        self.translation._('MIT LICENSE')
    #    self.screen.ids.action_bar.left_action_items = \
    #        [['chevron-left', lambda x: self.back_screen(27)]]


    def select_locale(self, *args):

        def select_locale(name_locale):

            for locale in self.dict_language.keys():
                if name_locale == self.dict_language[locale]:
                    self.lang = locale
                    self.config.set('General', 'language', self.lang)
                    self.config.write()

        dict_info_locales = {}
        for locale in self.dict_language.keys():
            dict_info_locales[self.dict_language[locale]] = \
                ['locale', locale == self.lang]

        if not self.window_language:
            self.window_language = card(
                Lists(
                    dict_items=dict_info_locales,
                    events_callback=select_locale, flag='one_select_check'
                ),
                size=(.85, .55)
            )
        self.window_language.open()

    def dialog_exit(self):
        def check_interval_press(interval):
            self.exit_interval += interval
            if self.exit_interval > 5:
                self.exit_interval = False
                Clock.unschedule(check_interval_press)

        if self.exit_interval:
            sys.exit(0)
            
        Clock.schedule_interval(check_interval_press, 1)
        toast(self.translation._('Press Back to Exit'))
    def on_lang(self, instance, lang):
        self.translation.switch_lang(lang)
