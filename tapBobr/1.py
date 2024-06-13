from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivymd.app import MDApp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.uix.label import Label
from kivymd.uix.progressbar import MDProgressBar
from kivy.clock import Clock
from kivy.core.window import Window

kv = '''
BoxLayout:
    orientation: 'vertical'
    padding: dp(20)

    AnchorLayout:
        ImageButton:
            id: img_btn
            source:'BOBR.jpg'
            size_hint: None, None
            size: dp(200), dp(200)

    AnchorLayout:
        Label:
            text: "Зруйнуй дамбу і  послухай пісню!!!"
            font_size: '18sp'
            color: (1, 0.6, 0, 1)
            bold: True

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(40)
        padding: dp(20)

        MDProgressBar:
            id: progress_bar
            value: 100
            color: (1, 0.6, 0, 1)
            max: 100
            min: 0
            size_hint_x: 0.8

        Label:
            id: progress_label
            text: "100%"
            size_hint_x: 0.2
            halign: 'center'
            color: (1, 0.6, 0, 1)

    Label:
        id: timer_label
        text: "Time: 25s"
        size_hint_y: None
        height: dp(40)
        halign: 'center'
        color: (1, 0.6, 0, 1)

    BoxLayout:
        size_hint_y: None
        height: dp(60)
        padding: dp(10)

        Button:
            text: "Ще раз"
            on_press: app.reset_game()
            size_hint_x: 0.5
            color: (1, 0.6, 0, 1)

        Button:
            text: "Вихід "
            on_press: app.exit_app()
            size_hint_x: 0.5
            color: (1, 0.6, 0, 1)
'''

class ImageButton(Image):
    initial_width = NumericProperty(0)
    initial_height = NumericProperty(0)
    timer_started = False
    time_left = NumericProperty(25)  # Початкове значення 25 секунд

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = SoundLoader.load('tap.mp3')
        self.victory_sound = SoundLoader.load('kurwa-bobr.mp3')  # Додайте ваш файл переможного звуку
        self.victory = False

    def on_kv_post(self, base_widget):
        self.initial_width = self.width
        self.initial_height = self.height

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if not self.timer_started and not self.victory:
                self.start_timer()
                self.timer_started = True

            if self.sound and not self.victory:
                self.sound.play()
            if not self.victory:
                self.animate_button()
                self.update_progress()
            return True
        return super().on_touch_down(touch)

    def animate_button(self):
        # Повернення до початкового розміру перед запуском нової анімації
        self.size = (self.initial_width, self.initial_height)
        anim = Animation(size=(self.initial_width * 0.9, self.initial_height * 0.9), duration=0.1) + Animation(size=(self.initial_width, self.initial_height), duration=0.1)
        anim.start(self)

    def update_progress(self):
        # Зменшуємо значення шкали на 1% при кожному натисканні
        progress_bar = self.parent.parent.ids.progress_bar
        progress_label = self.parent.parent.ids.progress_label

        if progress_bar.value > 0:
            progress_bar.value -= 1
            progress_label.text = f"{int(progress_bar.value)}%"
            if progress_bar.value == 0:
                self.timer_started = False
                self.victory = True
                Clock.unschedule(self.update_timer)
                self.parent.parent.ids.timer_label.text = "Дамбу знищено, ти справжній  бобр!"
                if self.victory_sound:
                    self.victory_sound.play()  # Програвання звуку перемоги
                # Не викликаємо reset_game при перемозі

    def start_timer(self):
        Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        if self.time_left > 0:
            self.time_left -= 1
            self.parent.parent.ids.timer_label.text = f"Time: {self.time_left}s"
        else:
            self.timer_started = False
            Clock.unschedule(self.update_timer)
            self.parent.parent.ids.timer_label.text = "Time's up! Mission failed."
            self.reset_game()

    def reset_game(self):
        # Встановлюємо шкалу на 100%, скидаємо лічильник часу та повідомлення
        progress_bar = self.parent.parent.ids.progress_bar
        progress_label = self.parent.parent.ids.progress_label
        timer_label = self.parent.parent.ids.timer_label
        progress_bar.value = 100
        progress_label.text = "100%"
        self.time_left = 25  # Скидаємо лічильник на 25 секунд
        timer_label.text = "Time: 25s"
        self.timer_started = False
        self.victory = False

class BODIA_I_boberApp(MDApp):
    def build(self):
        self.icon = 'BOBR.jpg' # Вказуємо шлях до іконки
        return Builder.load_string(kv)

    def reset_game(self):
        img_btn = self.root.ids.img_btn
        img_btn.reset_game()

    def exit_app(self):
        Window.close()

if __name__ =='__main__': 
   BODIA_I_boberApp().run()

