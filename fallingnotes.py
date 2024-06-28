import pygame
import sys

#CONSTANTS
beatsPerMin = 60


#COLORS
blue = (0,0,255)
orange = (255,165,0)

class FallingNote:
    def __init__(self, note, x, y, noteWidth, noteHeight, screen, hand="right_hand"):
        self.note = note
        self.x = x
        self.y = y
        self.hand = hand
        self.noteWidth = noteWidth
        self.noteHeight = noteHeight
        self.screen = screen

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
    

def calculateHeight(holdTime, noteSpeed):
    return holdTime * (beatsPerMin / 60) * noteSpeed
