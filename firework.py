import arcade
import random
import math


class FireworkParticle:
    def __init__(self, x, y, color, angle):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 8)
        self.vel_x = math.cos(angle) * random.uniform(0.5, 2)  # Adjust speed
        self.vel_y = math.sin(angle) * random.uniform(0.5, 2)  # Adjust speed
        self.alpha = random.randint(200, 255)

    def update(self, delta_time):
        self.x += self.vel_x * delta_time
        self.y += self.vel_y * delta_time
        self.alpha -= random.randint(3, 8) * delta_time

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.size, self.color + (self.alpha,))


class Firework:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = 5
        self.alpha = 255
        self.is_exploded = False
        self.explode_timer = 0
        self.particles = []
        self.explosion_speed = 25

    def update(self, delta_time):
        if not self.is_exploded:
            self.size += self.explosion_speed * delta_time
            if self.size >= random.randint(50, 100):
                self.is_exploded = True
                self.explode_timer = 0

                # Explode into particles
                for _ in range(random.randint(30, 50)):
                    angle = random.uniform(math.pi / 4, math.pi / 2)
                    particle = FireworkParticle(self.x, self.y, self.color, angle)
                    self.particles.append(particle)

        elif self.explode_timer < 1.5:  # Control explosion duration
            for particle in self.particles:
                particle.update(delta_time)
            self.explode_timer += delta_time

    def draw(self):
        if not self.is_exploded:
            arcade.draw_circle_filled(self.x, self.y, self.size, self.color + (self.alpha,))
        else:
            for particle in self.particles:
                particle.draw()
