from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

Window.size = (800, 480)

# Global değişkenler
score = 0
sound = SoundLoader.load("music.mp3")
if sound:
    sound.loop = True
    sound.play()

# Ana Menü Ekranı
class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        layout = FloatLayout()
        self.bg = Image(source="background.jpg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.bg)

        title = Label(text="🎮 Tıklama Oyunu 🎮", font_size=40, pos_hint={"center_x":0.5,"center_y":0.8})
        layout.add_widget(title)

        play_button = Button(text="Başla", size_hint=(.3, .2), pos_hint={"center_x":0.5, "center_y":0.5})
        play_button.bind(on_press=self.start_game)
        layout.add_widget(play_button)

        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = "game"

# Oyun Ekranı
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.bg = Image(source="background.jpg", allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.bg)

        self.score_label = Label(text="Skor: 0", font_size=30, pos_hint={"center_x":0.5,"top":1})
        self.layout.add_widget(self.score_label)

        self.click_button = Button(text="Tıkla!", size_hint=(.3, .2), pos_hint={"center_x":0.5, "center_y":0.5})
        self.click_button.bind(on_press=self.increase_score)
        self.layout.add_widget(self.click_button)

        self.timer_label = Label(text="Zaman: 15", font_size=24, pos_hint={"center_x":0.5,"center_y":0.9})
        self.layout.add_widget(self.timer_label)

        self.add_widget(self.layout)

        self.time_left = 15

    def on_enter(self):
        global score
        score = 0
        self.time_left = 15
        self.score_label.text = "Skor: 0"
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def increase_score(self, instance):
        global score
        score += 1
        self.score_label.text = f"Skor: {score}"

    def update_timer(self, dt):
        self.time_left -= 1
        self.timer_label.text = f"Zaman: {self.time_left}"
        if self.time_left <= 0:
            Clock.unschedule(self.timer_event)
            self.manager.current = "gameover"

# Oyun Sonu Ekranı
class GameOverScreen(Screen):
    def __init__(self, **kwargs):
        super(GameOverScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        self.bg = Image(source="background.jpg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.bg)

        self.result_label = Label(text="", font_size=30, pos_hint={"center_x":0.5,"center_y":0.7})
        layout.add_widget(self.result_label)

        restart_button = Button(text="Tekrar Oyna", size_hint=(.3, .2), pos_hint={"center_x":0.5, "center_y":0.4})
        restart_button.bind(on_press=self.restart_game)
        layout.add_widget(restart_button)

        self.add_widget(layout)

    def on_enter(self):
        global score
        self.result_label.text = f"Skorun: {score}"

    def restart_game(self, instance):
        self.manager.current = "menu"

# Ana App
class ClickGameApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainMenu(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(GameOverScreen(name="gameover"))
        return sm

if __name__ == "__main__":
    ClickGameApp().run()