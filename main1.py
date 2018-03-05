from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Rectangle, Rotate, Ellipse, Color, Line
from kivy.core.audio import SoundLoader
from kivy.graphics.context_instructions import PopMatrix, PushMatrix
from math import atan, degrees


class Player(Widget):
    def move(self, angle):
        self.pos = Vector(2,0).rotate(90) + self.pos
    
    
    def rotate(self, angle):
        global start_angle
        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate() 
            self.rot.angle = angle - start_angle
            self.rot.origin = self.center
            self.rot.axis = (0, 0, 1)
            start_angle = angle
            
        with self.canvas.after:
            PopMatrix()
           


class ShooterGame(Widget):
    player = ObjectProperty(None)
    
    def on_touch_down(self, touch):
        global x0, y0
        if touch.x < self.width//2:
            x0 = touch.x
            y0 = touch.y
            with self.canvas:
                Color(0, 1, 0)
                self.joystick = Line(circle = (x0, y0 , self.width//12), width = 2)
                Color(0, 1, 0)
                self.line = Line(points = (x0, y0), width = 2)
        else:
            pass    #for shooting
    
    
    def on_touch_move(self, touch):
        global x, y, angle
        if touch.x < self.width//1.5:
            x = touch.x
            y = touch.y
            self.line.points = [x0, y0, x, y]
            if x > x0:
                angle = degrees(atan((y - y0)/(x - x0)))           #rotation angle
            elif x < x0:
                angle = 180 + degrees(atan((y - y0)/(x - x0)))           #rotation angle
            elif y > y0:
                angle = 90
            else:
                angle = -90
            self.player.rotate(angle)
        else:
            pass
        
        
    def update(self, dt):
        global angle, x, y, x0 ,y0
        if x != x0 or y != y0:
            self.player.move(angle)

    
    
    def on_touch_up(self, touch):
        global x0, y0, y, x
        self.canvas.remove(self.joystick)
        self.canvas.remove(self.line)
        x = x0
        y = y0


class ShooterApp(App):
    def build(self):
        #self.load_sounds()
        #self.play_sound()
        game = ShooterGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game
    
    
    def load_sounds(self):
        name = 'papercut.wav'
        self.sound = SoundLoader.load(name)
        
        
    def play_sound(self):
        self.sound.volume = 0.2
        self.sound.play()

angle = 0
x = 0
x0 = 0
y = 0
y0 = 0
start_angle = 90
if __name__ == '__main__':
    ShooterApp().run()