import os
import pygame
import json


class ControlsManager:
    def __init__(self):
        self.controls_file_name = 'controls.json'
        self.controls = self.load_controls()

    def load_controls(self):
        try:
            # Controls are loaded
            controls = self.load_existing_controls()
        except FileNotFoundError:
            # No controls file, so create one
            controls = self.create_controls()
            self.write_controls(controls)
        return controls

    def load_existing_controls(self):
        #with open(os.path.join(self.controls_file_name), 'r+') as file:
        with open(self.controls_file_name, 'r+') as file:
            controls = json.load(file)
        return controls

    def create_controls(self):
        new_controls = {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT}
        return new_controls

    def write_controls(self, data):
        #with open(os.path.join(os.getcwd(), self.controls_file_name), 'w') as file:
        with open(self.controls_file_name, 'w') as file:
            json.dump(data, file)