import random
import os
import shutil
import json
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.popup import Popup

Window.clearcolor = (0.85, 0.95, 0.85, 1)  # Soft natural forest tone

SETTINGS_FILE = "thara_config.json"
VAULT_DIR = ".thara_vault"

if not os.path.exists(VAULT_DIR):
    os.makedirs(VAULT_DIR)

def load_settings():
    default_settings = {"pin": "1234", "sequence": ["lion", "panda", "doll"]}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except:
            return default_settings
    return default_settings

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f)

CURRENT_SETTINGS = load_settings()
SELECTED_TAP_SEQUENCE = []

class ImageButton(ButtonBehavior, Image):
    def __init__(self, cartoon_id, **kwargs):
        super().__init__(**kwargs)
        self.cartoon_id = cartoon_id

class PhotoButton(ButtonBehavior, Image):
    def __init__(self, photo_path, **kwargs):
        super().__init__(**kwargs)
        self.photo_path = photo_path

# Disguised Game / Home Screen (Looks like a live jungle game)
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        
        # Subtle title or can be removed completely for maximum stealth. Let's keep a friendly game header.
        self.header = Label(
            text='🌿 Jungle Animal Friends 🐾', 
            font_size='22sp', 
            bold=True, 
            color=(0.1, 0.4, 0.2, 0.8), 
            size_hint=(1, 0.1), 
            pos_hint={'x': 0, 'y': 0.9}
        )
        self.layout.add_widget(self.header)
        
        # Secret settings access trigger (Long press title or click corner discretely if needed, but tap sequence is primary)
        self.cartoons = ["lion", "panda", "doll", "cat", "dog", "ant", "rabbit", "teddy", "bird", "unicorn"]
        Clock.schedule_once(self.create_cartoons, 0.5)
        self.add_widget(self.layout)

    def create_cartoons(self, dt):
        for name in self.cartoons:
            pos_x = random.uniform(0.05, 0.70)
            pos_y = random.uniform(0.05, 0.80)
            img_path = f'{name}.png'
            if not os.path.exists(img_path):
                img_path = ''  # Fallback if image missing
            
            img_btn = ImageButton(
                cartoon_id=name, 
                source=img_path, 
                size_hint=(None, None), 
                size=(100, 100), 
                pos_hint={'x': pos_x, 'y': pos_y}
            )
            img_btn.bind(on_press=self.on_cartoon_tap)
            self.layout.add_widget(img_btn)
            self.animate_btn(img_btn)

    def animate_btn(self, btn):
        new_x = random.uniform(0.05, 0.75)
        new_y = random.uniform(0.05, 0.80)
        duration = random.uniform(6, 12)  # Smooth natural wandering speed
        anim = Animation(pos_hint={'x': new_x, 'y': new_y}, duration=duration, transition='in_out_sine')
        anim.bind(on_complete=lambda a, b: self.animate_btn(btn))
        anim.start(btn)

    def on_cartoon_tap(self, instance):
        global SELECTED_TAP_SEQUENCE
        SELECTED_TAP_SEQUENCE.append(instance.cartoon_id)
        if len(SELECTED_TAP_SEQUENCE) > len(CURRENT_SETTINGS["sequence"]):
            SELECTED_TAP_SEQUENCE.pop(0)
            
        if SELECTED_TAP_SEQUENCE == CURRENT_SETTINGS["sequence"]:
            SELECTED_TAP_SEQUENCE = []
            self.manager.current = 'lock'  # Prompt PIN or go straight to gallery

# Disguised Baby Doll Play Screen (Shows up if wrong password or normal interaction)
class BabyDollScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(Label(text='👶 Baby Doll Play Zone 🧸', font_size='28sp', bold=True, color=(0.8, 0.3, 0.5, 1), size_hint=(1, 0.15)))
        
        if os.path.exists('doll.png'):
            doll_img = Image(source='doll.png', size_hint=(1, 0.6))
            layout.add_widget(doll_img)
        
        layout.add_widget(Label(text='Tap the doll to hear a cute sound or play!', font_size='16sp', color=(0.4, 0.4, 0.4, 1), size_hint=(1, 0.1)))
        
        back_btn = Button(text='Back to Jungle', background_color=(0.3, 0.7, 0.4, 1), size_hint=(1, 0.15))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)

# Secure PIN Lock Screen for the Vault
class LockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        layout.add_widget(Label(text='🔒 Secret Verification', font_size='28sp', bold=True, color=(0.2, 0.2, 0.2, 1)))
        layout.add_widget(Label(text='Enter PIN Code:', font_size='16sp', color=(0.4, 0.4, 0.4, 1)))
        
        self.pin_input = TextInput(password=True, multiline=False, size_hint=(1, 0.15), font_size='24sp', halign='center')
        layout.add_widget(self.pin_input)
        
        btn_box = BoxLayout(size_hint=(1, 0.2), spacing=10)
        unlock_btn = Button(text='Access Vault', background_color=(0.2, 0.6, 0.3, 1), color=(1, 1, 1, 1))
        unlock_btn.bind(on_press=self.verify_pin)
        
        cancel_btn = Button(text='Cancel', background_color=(0.7, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        cancel_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        
        btn_box.add_widget(unlock_btn)
        btn_box.add_widget(cancel_btn)
        layout.add_widget(btn_box)
        
        self.msg = Label(text='', color=(0.8, 0, 0, 1))
        layout.add_widget(self.msg)
        self.add_widget(layout)

    def verify_pin(self, instance):
        if self.pin_input.text == CURRENT_SETTINGS["pin"]: 
            self.pin_input.text = ""
            self.msg.text = ""
            self.manager.current = 'secret_gallery'
        else:
            self.pin_input.text = ""
            # Clever disguise: If someone types the wrong PIN, redirect them seamlessly to the Baby Doll screen so they think it's just a kids game!
            self.manager.current = 'baby_doll'

# Hidden Secret Gallery Screen
class SecretGalleryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text='📁 Thara Secure Vault', font_size='24sp', bold=True, color=(0.1, 0.3, 0.5, 1), size_hint=(1, 0.1)))
        
        self.grid = GridLayout(cols=2, spacing=15, size_hint=(1, 0.7))
        layout.add_widget(self.grid)
        
        btn_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)
        
        settings_btn = Button(text='Settings', background_color=(0.2, 0.5, 0.7, 1))
        settings_btn.bind(on_press=self.open_settings)
        btn_layout.add_widget(settings_btn)
        
        back_btn = Button(text='Lock & Exit', background_color=(0.8, 0.3, 0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        btn_layout.add_widget(back_btn)
        
        layout.add_widget(btn_layout)
        self.add_widget(layout)
        
    def on_enter(self):
        self.load_photos()

    def load_photos(self):
        self.grid.clear_widgets()
        found_photos = False
        cartoons_list = ["lion.png", "panda.png", "doll.png", "cat.png", "dog.png", "ant.png", "rabbit.png", "teddy.png", "bird.png", "unicorn.png"]
        
        # Auto sweep any loose photos into vault
        for file in os.listdir('.'):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) and file not in cartoons_list and file != 'thara_config.json':
                try:
                    shutil.move(file, os.path.join(VAULT_DIR, file))
                except:
                    pass

        if os.path.exists(VAULT_DIR):
            for file in os.listdir(VAULT_DIR):
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    found_photos = True
                    full_path = os.path.join(VAULT_DIR, file)
                    img_btn = PhotoButton(photo_path=full_path, source=full_path, size_hint=(None, None), size=(150, 150))
                    img_btn.bind(on_press=self.open_full_view)
                    self.grid.add_widget(img_btn)
                    
        if not found_photos:
            self.grid.add_widget(Label(text='No private photos in vault.', font_size='16sp', color=(0.4, 0.4, 0.4, 1)))

    def open_full_view(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        full_img = Image(source=instance.photo_path, size_hint=(1, 0.8))
        content.add_widget(full_img)
        
        btn_box = BoxLayout(size_hint=(1, 0.2), spacing=10)
        restore_btn = Button(text='Restore', background_color=(0.2, 0.7, 0.3, 1))
        delete_btn = Button(text='Delete', background_color=(0.9, 0.2, 0.2, 1))
        close_btn = Button(text='Close', background_color=(0.5, 0.5, 0.5, 1))
        
        btn_box.add_widget(restore_btn)
        btn_box.add_widget(delete_btn)
        btn_box.add_widget(close_btn)
        content.add_widget(btn_box)
        
        popup = Popup(title='View Photo', content=content, size_hint=(0.9, 0.85))
        
        def restore_photo(btn):
            file_name = os.path.basename(instance.photo_path)
            try:
                shutil.move(instance.photo_path, file_name)
            except:
                pass
            popup.dismiss()
            self.load_photos()

        def delete_photo(btn):
            try:
                os.remove(instance.photo_path)
            except:
                pass
            popup.dismiss()
            self.load_photos()

        restore_btn.bind(on_press=restore_photo)
        delete_btn.bind(on_press=delete_photo)
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def open_settings(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='New 4-Digit PIN:'))
        pin_in = TextInput(text=CURRENT_SETTINGS["pin"], multiline=False)
        content.add_widget(pin_in)
        
        content.add_widget(Label(text='New Tap Sequence (comma separated):'))
        seq_in = TextInput(text=",".join(CURRENT_SETTINGS["sequence"]), multiline=False)
        content.add_widget(seq_in)
        
        save_btn = Button(text='Save Settings', background_color=(0.2, 0.6, 0.3, 1))
        content.add_widget(save_btn)
        
        popup = Popup(title='Vault Settings', content=content, size_hint=(0.85, 0.6))
        
        def save(b):
            global CURRENT_SETTINGS
            CURRENT_SETTINGS["pin"] = pin_in.text.strip()
            CURRENT_SETTINGS["sequence"] = [x.strip() for x in seq_in.text.split(",") if x.strip()]
            save_settings(CURRENT_SETTINGS)
            popup.dismiss()
            
        save_btn.bind(on_press=save)
        popup.open()

class TharaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(BabyDollScreen(name='baby_doll'))
        sm.add_widget(LockScreen(name='lock'))
        sm.add_widget(SecretGalleryScreen(name='secret_gallery'))
        return sm

if __name__ == '__main__':
    TharaApp().run()