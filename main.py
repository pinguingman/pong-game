from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def update(self, dt):
        self.ball.move()
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        if self.ball.x < 0:
            self.ball.velocity_x *= -1
            self.player2.score += 1
            self.ball.set_velocity(start=135, end=225)
            self.ball.set_center(self.center)
        if self.ball.right > self.width:
            self.ball.velocity_x += -1
            self.player1.score += 1
            self.ball.set_velocity(start=-45, end=45)
            self.ball.set_center(self.center)

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            speedup = 1.1
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * speedup
            ball.velocity = vel.x, vel.y + offset


class PongApp(App):
    def build(self):
        game = PongGame()
        game.ball.set_velocity()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def set_velocity(self, start=0, end=360):
        self.center = self.center
        self.velocity = Vector(4, 0).rotate(randint(start, end))

    def set_center(self, new_center):
        self.center = new_center


if __name__ == '__main__':
    PongApp().run()
