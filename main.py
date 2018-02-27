from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.vector import Vector


class Player(Widget):
    def move(self, vector):
        self.pos = Vector(*vector) + self.pos


class ShooterGame(Widget):
    player = ObjectProperty(None)
    
    
    def on_touch_down(self, touch):
        global x0, y0
        if touch.x < self.width//2:
            x0 = touch.x
            y0 = touch.y
        else:
            pass    #for shooting
    
    
    def on_touch_move(self, touch):
        x = touch.x
        y = touch.y
        vector = (x - x0, y - y0)
        self.player.move(vector)
    pass


class ShooterApp(App):
    def build(self):
        game = ShooterGame()
        return game


if __name__ == '__main__':
    ShooterApp().run()