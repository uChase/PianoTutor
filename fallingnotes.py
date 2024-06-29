import pygame
import sys
import math
import random

#


#COLORS
blue = (0,0,255)
orange = (255,165,0)
green = (0,255,0)
red = (255,0,0)


class Particle:
    def __init__(self, x, y, angle, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.speed = random.uniform(2, 50)
        self.angle = math.radians(angle)
        self.life = 0.7  # seconds
        self.alpha = 255  # Full opacity

    def move(self, delta_time):
        self.x += self.speed * math.cos(self.angle) * delta_time
        self.y += self.speed * math.sin(self.angle) * delta_time
        self.life -= delta_time
        self.alpha = max(0, int(255 * (self.life / 0.7)))

    def draw(self, screen):
        if self.life > 0:
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, self.alpha), (self.size, self.size), self.size)
            screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))


class FallingNote:
    def __init__(self, note, x, y, noteWidth, noteHeight, screen, hand="right_hand"):
        self.note = note
        self.x = x
        self.y = y
        self.hand = hand
        self.noteWidth = noteWidth
        self.noteHeight = noteHeight
        self.screen = screen
        self.isHitCorrect = False
        self.isReleasedCorrect = True
        self.released = False
        self.particles = []
        self.spawning_particles = False


    def fall(self, deltaTime, noteSpeed):
        self.y += noteSpeed * deltaTime

    def draw(self):
        radius = min(self.noteWidth, self.noteHeight) // 4  # Radius for the rounded corners
        color = blue if self.hand == "right_hand" else orange

        # Draw the rounded rectangle
        pygame.draw.rect(self.screen, color, (self.x + radius, self.y, self.noteWidth - 2 * radius, self.noteHeight))  # Center rectangle
        pygame.draw.rect(self.screen, color, (self.x, self.y + radius, self.noteWidth, self.noteHeight - 2 * radius))  # Side rectangles

        # Draw the corners
        pygame.draw.circle(self.screen, color, (self.x + radius, self.y + radius), radius)  # Top-left corner
        pygame.draw.circle(self.screen, color, (self.x + self.noteWidth - radius, self.y + radius), radius)  # Top-right corner
        pygame.draw.circle(self.screen, color, (self.x + radius, self.y + self.noteHeight - radius), radius)  # Bottom-left corner
        pygame.draw.circle(self.screen, color, (self.x + self.noteWidth - radius, self.y + self.noteHeight - radius), radius)  # Bottom-right corner

    def decrease_and_delete(self, keyboard_location):
        if self.y + self.noteHeight > keyboard_location:
            self.noteHeight -= self.y + self.noteHeight - keyboard_location
        if self.noteHeight <= 0:
            return True
        return False
    
    def setIsHitCorrect(self):
        self.isHitCorrect = True
    
    def setIsReleasedIncorrect(self):
        self.isReleasedCorrect = False
    
    def correctEffect(self):
        self.spawning_particles = True
    
    def stopCorrectEffect(self):
        self.spawning_particles = False

        color = red

        for _ in range(5):  # Number of particles per frame
            angle = random.uniform(-20, 20)
            particle_right = Particle(self.x + self.noteWidth, self.y + self.noteHeight, angle, color)
            particle_left = Particle(self.x, self.y + self.noteHeight, angle + 180, color)
            self.particles.append(particle_right)
            self.particles.append(particle_left)

    def stopCorrectEffectGood(self):
        self.spawning_particles = False
        color = green            
            # Create particles at the bottom left and right of the note
        for _ in range(5):  # Number of particles per frame
            angle = random.uniform(-20, 20)
            particle_right = Particle(self.x + self.noteWidth, self.y + self.noteHeight, angle, color)
            particle_left = Particle(self.x, self.y + self.noteHeight, angle + 180, color)
            self.particles.append(particle_right)
            self.particles.append(particle_left)

    def update_particles(self, delta_time):
        if self.hand == "right_hand":
            color = blue
        else:
            color = orange
        if self.spawning_particles:
            
            # Create particles at the bottom left and right of the note
            for _ in range(5):  # Number of particles per frame
                angle = random.uniform(-20, 20)
                particle_right = Particle(self.x + self.noteWidth, self.y + self.noteHeight, angle, color)
                particle_left = Particle(self.x, self.y + self.noteHeight, angle + 180, color)
                self.particles.append(particle_right)
                self.particles.append(particle_left)

        for particle in self.particles:
            particle.move(delta_time)
            particle.draw(self.screen)
        # Remove dead particles
        self.particles = [particle for particle in self.particles if particle.life > 0]

        


    

def calculateHeight(holdTime, noteSpeed, bpm):
    return holdTime * (60 / bpm) * noteSpeed




