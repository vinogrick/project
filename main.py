from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


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
        global x, y
        if touch.x < self.width//2:
            x = touch.x
            y = touch.y
        else:
            pass
        
        
    def update(self, dt):
        try:
            global x, y, x0, y0
            if x0 != x or y0 != y:
                r = 2
                R = ((x - x0)**2 + (y - y0)**2)**0.5
                try:
                    x_itog = (x - x0) * r/R
                    y_itog = (y - y0) * r/R
                    vector = (x_itog, y_itog)
                    self.player.move(vector)
                except Exception:
                    None
        except Exception:
            None
    
    
    def on_touch_up(self, touch):
        global x0, y0, y, x
        x = x0
        y = y0


class ShooterApp(App):
    def build(self):
        game = ShooterGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    ShooterApp().run()