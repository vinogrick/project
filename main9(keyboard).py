from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Rectangle, Rotate, Ellipse, Color, Line
from kivy.core.audio import SoundLoader
from kivy.graphics.context_instructions import PopMatrix, PushMatrix
from kivy.core.window import Window
from math import atan, degrees, sin, cos, radians
from random import randint
from kivy.lang import Builder

angle = 0
x = 0
x0 = 0
y = 0
y0 = 0
start_angle = 90
interval = 1

def start_game():
    global angle, x, x0, y, y0, start_angle, interval
    
    def proverka(x_reck, y_reck, x_bul, y_bul, angle):
        if x_reck < x_bul + 15*cos(radians(angle)) < x_reck + 50 and y_reck < y_bul + 15*sin(radians(angle)) < y_reck + 50:
            return True
        else:
            return False
        
        
    def proverka2(x_pl, y_pl, x_en, y_en):
        if ((x_pl-x_en)**2+(y_pl-y_en)**2)**0.5 < 50:
            return True
        else:
            return False
        
    
    # player widget (at the time - a tank) that reacts to moves of joystick and button "fire" press
    class Player(Widget):
        
        def move_enemies(self, dt):
            for i in self.parent.enemies:
                y = self.parent.player.center_coords[1]
                x = self.parent.player.center_coords[0]
                x0 = i[0]
                y0 = i[1]            
                if x > x0:
                    angle = degrees(atan((y - y0)/(x - x0)))           #rotation angle
                elif x < x0:
                    angle = 180 + degrees(atan((y - y0)/(x - x0)))           #rotation angle
                elif y > y0:
                    angle = 90
                else:
                    angle = -90            
                i[0] = i[0] + Vector(2, 0).rotate(angle)[0]
                i[1] = i[1] + Vector(2, 0).rotate(angle)[1]
                i[2].pos = (i[0], i[1])
            
        
        # moving bullet
        def fly_bullet(self, dt):
            
            if self.bullets == []:
                Clock.unschedule(self.fire_clock)
            else:
                to_delete = []
                for i in self.bullets:
                    if not((i[0] > self.parent.width + 50) or (i[0] < -50) or (i[1] < -50) or (i[1] > self.parent.height + 50)):
                        i[0] = i[0] + Vector(5, 0).rotate(i[3])[0]
                        i[1] = i[1] + Vector(5, 0).rotate(i[3])[1]
                        i[2].points = [i[0], i[1], i[0] + 15*cos(radians(i[3])), i[1] + 15*sin(radians(i[3]))]
                    else:
                        self.parent.canvas.remove(i[2])
                        to_delete.append(i)
                for i in to_delete:
                    self.bullets.remove(i)
                
                    
        
        
        # one bullet
        def fire(self):
            global start_angle
            with self.parent.canvas:
                Color(1, 0, 1)
                
                # coordinates of barrel
                self.coord_fire = [self.center_coords[0] + Vector(self.size[1]//2 - 0, 0).rotate(start_angle)[0], 
                                   self.center_coords[1] + Vector(self.size[1]//2 - 30, 0).rotate(start_angle)[1]]
                
                # creating a list with 4 parameters: start positions of bullets, bullet as a Line object and the angle of bullet
                
                if self.bullets == []:
                    self.fire_clock = Clock.schedule_interval(self.fly_bullet, 1.0 / 60.0)
                else:
                    Clock.unschedule(self.fire_clock)
                    self.fire_clock = Clock.schedule_interval(self.fly_bullet, 1.0 / 60.0)
                    
                self.bullets.append([self.coord_fire[0], self.coord_fire[1], Line(points = self.coord_fire + [self.coord_fire[0] + 15*cos(radians(start_angle)), 
                                                                                self.coord_fire[1] + 15*sin(radians(start_angle))], width = 1.5), start_angle])            
                    
            
        # moves player according to joystick posision
        def move(self, angle):
            global start_angle
            self.pos = Vector(0, 2) + self.pos
            self.center_coords[0] += Vector(2, 0).rotate(start_angle)[0]
            self.center_coords[1] += Vector(2, 0).rotate(start_angle)[1]
        
        
        # rotates player according to joystick posision
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
                
               
    # the main widget like canvas in tkinter
    class ShooterGame(Widget):     
        def __init__(self, **kwargs):
            super(ShooterGame, self).__init__(**kwargs)
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
        def _keyboard_closed(self):
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None
        
        def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
            if keycode[1] == 'spacebar':
                self.player.fire()
            return True           
        
        player = ObjectProperty(None)
        

        # activates when the finger touches the screen
        def on_touch_down(self, touch):
            global x0, y0
            if touch.x < self.width//1.5:
                self.if_joy = 1     # for escaping error when deleting joystick            
                x0 = touch.x
                y0 = touch.y
                with self.canvas:
                    Color(0, 1, 0)
                    self.joystick = Line(circle = (x0, y0 , self.width//12), width = 2)
                    Color(0, 1, 0)
                    self.line = Line(points = (x0, y0), width = 2)
            else:
                self.player.fire()
        
        
        # activates when the finger moves on screen
        def on_touch_move(self, touch):
            global x, y, angle
            if touch.x < self.width//1.5 and self.if_joy:
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
                
            
        
        # updates the screen 60 times per second
        def update(self, dt):
            global angle, x, y, x0 ,y0
            if x != x0 or y != y0:
                self.player.move(angle)
            if self.player.bullets != [] and self.enemies != []:
                to_delete = []
                for i in self.player.bullets:
                    for j in self.enemies:
                        if proverka(j[0], j[1], i[0], i[1], i[3]):
                            self.canvas.remove(i[2])
                            self.canvas.remove(j[2])
                            to_delete.append([i, j])
                for i in to_delete:
                    self.player.score+=1
                    try:
                        self.player.bullets.remove(i[0])
                        self.enemies.remove(i[1])
                    except Exception:
                        None
                        
                  
            if self.enemies != []:
                to_delete1=[]
                for j in self.enemies:  
                    if proverka2(self.player.center_coords[0],self.player.center_coords[1], j[0]+25,j[1]+25):
                        self.canvas.remove(j[2])
                        to_delete1.append(j)    
                        
                for i in to_delete1:
                    self.player.lifes-=1
                    if self.player.lifes == 0:    
                        run.sound.stop()
                        run.stop()
                        menu()
                    else:
                        try:
                            self.enemies.remove(i)
                        except Exception:
                            None
                        
            
        
        
        # activates when the finger is released
        def on_touch_up(self, touch):
            if self.if_joy:
                global x0, y0, y, x
                self.canvas.remove(self.joystick)
                self.canvas.remove(self.line)
                x = x0
                y = y0
                self.if_joy = 0
                
                
        # spawn enemies
        def spawn_enemies(self, dt):
            x1,y1=randint(0,self.width),0
            x2,y2=randint(0,self.width),self.height
            x3,y3=0,randint(0,self.height)
            x4,y4=self.width,randint(0,self.height) 
            l=[[x1,y1], [x2, y2], [x3, y3], [x4,y4]]
            x, y = l[randint(0, 3)]
            with self.canvas:
                Color(1, 1, 1)
                self.enemies.append([x, y, Rectangle(source = 'alien.png', pos = (x, y), size = (50, 50))])
                
            
            
    
    # the game itself as an app
    class ShooterApp(App):
        def build(self):
            self.load_sounds()
            self.play_sound()
            game = ShooterGame()
            Clock.schedule_interval(game.spawn_enemies, interval)
            Clock.schedule_interval(game.player.move_enemies, 1.0 / 40.0)
            Clock.schedule_interval(game.update, 1.0 / 60.0)
            return game
        
        
        # loads the sounds of game
        def load_sounds(self):
            name = 'gachi.mp3'
            self.sound = SoundLoader.load(name)
            
        
        # plays all sounds
        def play_sound(self):
            self.sound.volume = 0.2
            self.sound.loop = True
            self.sound.play()
    
    
    Builder.load_file('shoter.kv')
    run = ShooterApp()
    run.run()
        

def menu():
    global angle, x, x0, y, y0, start_angle, interval
    angle = 0
    x = 0
    x0 = 0
    y = 0
    y0 = 0
    start_angle = 90
    
    
    class ShooterMenu(Widget):
        def start(self):
            run.stop()
            start_game()
    
    
        def level(self, num):
            global interval
            interval = num    
            
    class Menu(App):
        def build(self):
            menu = ShooterMenu()
            return menu
       
        
    Builder.load_file('menu.kv')
    run = Menu()
    run.run()
        
menu()