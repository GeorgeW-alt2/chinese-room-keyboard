import pygame
import os
from PIL import Image
import textwrap

class SymbolKeyboard:
    def __init__(self):
        pygame.init()
        
        # Window settings
        self.WINDOW_WIDTH = 1200
        self.WINDOW_HEIGHT = 800
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Symbol Keyboard")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.LIGHT_BLUE = (200, 220, 255)
        
        # Keyboard layout settings
        self.KEY_SIZE = 60
        self.KEY_SPACING = 10
        self.SPACE_BAR_WIDTH = 300  # Width for space bar
        self.KEY_ROWS = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM",
            " "  # Space bar row
        ]
        
        # Text input area
        self.text_input = ""
        self.font = pygame.font.Font(None, 36)
        
        # Load symbols
        self.symbols = self._load_symbols()
        self.key_to_symbol = self._create_key_mapping()
        
        # Pressed keys tracking
        self.pressed_keys = set()
        
    def _load_symbols(self):
        """Load all symbol images from the generated_symbols folder."""
        symbols = {}
        symbol_dir = "generated_symbols"
        if not os.path.exists(symbol_dir):
            raise FileNotFoundError("Generated symbols folder not found!")
            
        for filename in sorted(os.listdir(symbol_dir)):
            if filename.endswith(".png"):
                number = int(filename.split("_")[1].split(".")[0])
                image_path = os.path.join(symbol_dir, filename)
                
                # Load with PIL first to ensure consistent format
                pil_image = Image.open(image_path)
                pil_image = pil_image.resize((self.KEY_SIZE - 10, self.KEY_SIZE - 10))
                # Convert PIL image to Pygame surface
                mode = pil_image.mode
                size = pil_image.size
                data = pil_image.tobytes()
                py_image = pygame.image.fromstring(data, size, mode)
                
                symbols[number] = py_image
        return symbols
        
    def _create_key_mapping(self):
        """Create mapping between keyboard keys and symbols."""
        mapping = {}
        symbol_index = 1
        for row in self.KEY_ROWS[:-1]:  # Exclude space bar row from symbol mapping
            for key in row:
                mapping[key] = symbol_index
                symbol_index += 1
        return mapping
        
    def draw_keyboard(self):
        """Draw the keyboard with symbols."""
        start_y = 400  # Starting Y position for the keyboard
        
        for row_index, row in enumerate(self.KEY_ROWS):
            if row == " ":  # Space bar row
                # Center the space bar
                x = (self.WINDOW_WIDTH - self.SPACE_BAR_WIDTH) // 2
                y = start_y + row_index * (self.KEY_SIZE + self.KEY_SPACING)
                
                # Draw space bar
                space_rect = pygame.Rect(x, y, self.SPACE_BAR_WIDTH, self.KEY_SIZE)
                is_pressed = " " in self.pressed_keys
                color = self.LIGHT_BLUE if is_pressed else self.WHITE
                pygame.draw.rect(self.screen, color, space_rect)
                pygame.draw.rect(self.screen, self.BLACK, space_rect, 2)
                
                # Draw "SPACE" text
                space_text = self.font.render("SPACE", True, self.BLACK)
                text_x = x + (self.SPACE_BAR_WIDTH - space_text.get_width()) // 2
                text_y = y + (self.KEY_SIZE - space_text.get_height()) // 2
                self.screen.blit(space_text, (text_x, text_y))
            else:
                # Regular key row
                row_width = len(row) * (self.KEY_SIZE + self.KEY_SPACING)
                start_x = (self.WINDOW_WIDTH - row_width) // 2
                
                for col_index, key in enumerate(row):
                    x = start_x + col_index * (self.KEY_SIZE + self.KEY_SPACING)
                    y = start_y + row_index * (self.KEY_SIZE + self.KEY_SPACING)
                    
                    # Draw key background
                    key_rect = pygame.Rect(x, y, self.KEY_SIZE, self.KEY_SIZE)
                    is_pressed = key in self.pressed_keys
                    color = self.LIGHT_BLUE if is_pressed else self.WHITE
                    pygame.draw.rect(self.screen, color, key_rect)
                    pygame.draw.rect(self.screen, self.BLACK, key_rect, 2)
                    
                    # Draw symbol
                    symbol_index = self.key_to_symbol.get(key)
                    if symbol_index in self.symbols:
                        symbol_surf = self.symbols[symbol_index]
                        symbol_x = x + (self.KEY_SIZE - symbol_surf.get_width()) // 2
                        symbol_y = y + (self.KEY_SIZE - symbol_surf.get_height()) // 2
                        self.screen.blit(symbol_surf, (symbol_x, symbol_y))
                    
                    # Draw key letter
                    letter_surf = self.font.render(key, True, self.BLACK)
                    letter_x = x + (self.KEY_SIZE - letter_surf.get_width()) // 2
                    letter_y = y + self.KEY_SIZE - 20
                    self.screen.blit(letter_surf, (letter_x, letter_y))
                
    def draw_text_input(self):
        """Draw the text input area with the typed symbols."""
        # Draw input box
        input_rect = pygame.Rect(50, 50, self.WINDOW_WIDTH - 100, 300)
        pygame.draw.rect(self.screen, self.WHITE, input_rect)
        pygame.draw.rect(self.screen, self.BLACK, input_rect, 2)
        
        # Draw symbols in text input
        x, y = 60, 60
        line_height = self.KEY_SIZE
        max_width = self.WINDOW_WIDTH - 120
        
        # Wrap text into lines
        wrapped_text = textwrap.wrap(self.text_input, width=50)
        
        for line in wrapped_text:
            x = 60  # Reset x position for each line
            for char in line:
                if char == " ":  # Handle space
                    x += self.KEY_SIZE // 2
                elif char.upper() in self.key_to_symbol:
                    symbol_index = self.key_to_symbol[char.upper()]
                    if symbol_index in self.symbols:
                        symbol_surf = self.symbols[symbol_index]
                        if x + symbol_surf.get_width() > max_width:
                            x = 60
                            y += line_height
                        self.screen.blit(symbol_surf, (x, y))
                        x += symbol_surf.get_width() + 5
            y += line_height
            
    def run(self):
        """Main loop for the keyboard interface."""
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.text_input += " "
                        self.pressed_keys.add(" ")
                    elif event.unicode.upper() in self.key_to_symbol:
                        self.text_input += event.unicode
                        self.pressed_keys.add(event.unicode.upper())
                    elif event.key == pygame.K_BACKSPACE:
                        self.text_input = self.text_input[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.pressed_keys.remove(" ")
                    elif event.unicode.upper() in self.key_to_symbol:
                        self.pressed_keys.remove(event.unicode.upper())
            
            # Draw everything
            self.screen.fill(self.GRAY)
            self.draw_text_input()
            self.draw_keyboard()
            pygame.display.flip()
            
            clock.tick(60)
            
        pygame.quit()

if __name__ == "__main__":
    keyboard = SymbolKeyboard()
    keyboard.run()