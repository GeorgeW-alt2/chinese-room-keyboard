import random
import math
from typing import List, Tuple
import os
from PIL import Image, ImageDraw
import hashlib
import numpy as np

class SymbolGenerator:
    def __init__(self, size: int = 500):
        self.size = size
        self.margin = size // 10
        self.effective_size = size - 2 * self.margin
        self.center = size // 2
        self.generated_hashes = set()
        
    def _get_symbol_hash(self, image: Image.Image) -> str:
        img_array = np.array(image)
        img_small = Image.fromarray(img_array).resize((50, 50))
        return hashlib.md5(np.array(img_small).tobytes()).hexdigest()

    def _is_unique(self, image: Image.Image) -> bool:
        symbol_hash = self._get_symbol_hash(image)
        if symbol_hash in self.generated_hashes:
            return False
        self.generated_hashes.add(symbol_hash)
        return True

    def _generate_base_shape(self) -> List[Tuple[float, float]]:
        shape_type = random.choice([
            self._generate_calligraphic_stroke,
            self._generate_radical,
            self._generate_flowing_curve,
            self._generate_glyph_structure,
            self._generate_logographic,
            self._generate_pictographic
        ])
        return shape_type()
    
    def _generate_calligraphic_stroke(self) -> List[Tuple[float, float]]:
        """Generate a stroke that looks like calligraphy."""
        points = []
        start_x = self.center - self.effective_size * random.uniform(0.2, 0.3)
        start_y = self.center + self.effective_size * random.uniform(0.2, 0.3)
        
        # Create main stroke
        control_points = [
            (start_x, start_y),
            (start_x + random.uniform(50, 100), start_y - random.uniform(50, 100)),
            (start_x + random.uniform(150, 200), start_y - random.uniform(150, 200)),
            (start_x + random.uniform(250, 300), start_y - random.uniform(50, 100))
        ]
        
        # Generate smooth curve through control points
        for t in range(0, 101, 5):
            t = t / 100
            x = sum(p[0] * self._bezier_coeff(i, 3, t) for i, p in enumerate(control_points))
            y = sum(p[1] * self._bezier_coeff(i, 3, t) for i, p in enumerate(control_points))
            points.append((x, y))
            
        return points
    
    def _bezier_coeff(self, i: int, n: int, t: float) -> float:
        return math.comb(n, i) * (1 - t)**(n - i) * t**i
    
    def _generate_radical(self) -> List[Tuple[float, float]]:
        """Generate a shape reminiscent of radicals in logographic writing systems."""
        points = []
        num_strokes = random.randint(2, 4)
        base_x = self.center - self.effective_size * 0.25
        base_y = self.center + self.effective_size * 0.25
        
        for _ in range(num_strokes):
            stroke_length = random.uniform(0.3, 0.5) * self.effective_size
            angle = random.uniform(-math.pi/4, math.pi/4)
            
            points.extend([
                (base_x, base_y),
                (base_x + math.cos(angle) * stroke_length,
                 base_y - math.sin(angle) * stroke_length)
            ])
            
            base_x += random.uniform(30, 50)
            base_y -= random.uniform(20, 40)
            
        return points
    
    def _generate_flowing_curve(self) -> List[Tuple[float, float]]:
        """Generate a flowing, script-like curve."""
        points = []
        num_points = random.randint(8, 12)
        amplitude = self.effective_size * random.uniform(0.1, 0.2)
        frequency = random.uniform(1, 2)
        
        for i in range(num_points):
            t = i / (num_points - 1)
            x = self.center - self.effective_size * 0.3 + t * self.effective_size * 0.6
            y = self.center + amplitude * math.sin(frequency * math.pi * t)
            points.append((x, y))
        
        return points
    
    def _generate_glyph_structure(self) -> List[Tuple[float, float]]:
        """Generate a structure similar to complex glyphs."""
        points = []
        num_components = random.randint(2, 4)
        
        for _ in range(num_components):
            component_points = []
            size = self.effective_size * random.uniform(0.15, 0.25)
            x_offset = random.uniform(-0.2, 0.2) * self.effective_size
            y_offset = random.uniform(-0.2, 0.2) * self.effective_size
            
            for i in range(4):
                angle = (i * math.pi / 2) + random.uniform(-0.2, 0.2)
                x = self.center + math.cos(angle) * size + x_offset
                y = self.center + math.sin(angle) * size + y_offset
                component_points.append((x, y))
            
            points.extend(component_points)
        
        return points
    
    def _generate_logographic(self) -> List[Tuple[float, float]]:
        """Generate a pattern similar to logographic characters."""
        points = []
        num_strokes = random.randint(3, 5)
        base_size = self.effective_size * 0.3
        
        for _ in range(num_strokes):
            stroke_type = random.choice(['horizontal', 'vertical', 'diagonal'])
            x_offset = random.uniform(-0.2, 0.2) * self.effective_size
            y_offset = random.uniform(-0.2, 0.2) * self.effective_size
            
            if stroke_type == 'horizontal':
                points.extend([
                    (self.center - base_size/2 + x_offset, self.center + y_offset),
                    (self.center + base_size/2 + x_offset, self.center + y_offset)
                ])
            elif stroke_type == 'vertical':
                points.extend([
                    (self.center + x_offset, self.center - base_size/2 + y_offset),
                    (self.center + x_offset, self.center + base_size/2 + y_offset)
                ])
            else:  # diagonal
                angle = random.uniform(0, math.pi)
                points.extend([
                    (self.center - math.cos(angle) * base_size/2 + x_offset,
                     self.center - math.sin(angle) * base_size/2 + y_offset),
                    (self.center + math.cos(angle) * base_size/2 + x_offset,
                     self.center + math.sin(angle) * base_size/2 + y_offset)
                ])
        
        return points
    
    def _generate_pictographic(self) -> List[Tuple[float, float]]:
        """Generate simplified pictographic-like symbols."""
        points = []
        num_elements = random.randint(3, 6)
        radius = self.effective_size * 0.25
        
        for i in range(num_elements):
            angle = (i * 2 * math.pi / num_elements) + random.uniform(-0.2, 0.2)
            r = radius * random.uniform(0.8, 1.2)
            x = self.center + math.cos(angle) * r
            y = self.center + math.sin(angle) * r
            points.append((x, y))
            
            if random.random() < 0.5:  # Add connecting lines
                x2 = self.center + math.cos(angle + math.pi/num_elements) * r * 0.7
                y2 = self.center + math.sin(angle + math.pi/num_elements) * r * 0.7
                points.append((x2, y2))
        
        return points

    def _add_decoration(self, draw: ImageDraw.Draw, points: List[Tuple[float, float]]):
        """Add script-like decorative elements."""
        decoration_type = random.choice(['serifs', 'dots', 'strokes', 'none'])
        
        if decoration_type == 'serifs':
            serif_length = random.randint(5, 15)
            for point in random.sample(points, len(points)//2):
                angle = random.uniform(0, math.pi)
                draw.line([
                    (point[0] - math.cos(angle) * serif_length,
                     point[1] - math.sin(angle) * serif_length),
                    (point[0] + math.cos(angle) * serif_length,
                     point[1] + math.sin(angle) * serif_length)
                ], fill='black', width=2)
                
        elif decoration_type == 'dots':
            for point in random.sample(points, len(points)//3):
                dot_size = random.randint(3, 6)
                draw.ellipse([
                    (point[0] - dot_size, point[1] - dot_size),
                    (point[0] + dot_size, point[1] + dot_size)
                ], fill='black')
                
        elif decoration_type == 'strokes':
            stroke_length = random.randint(10, 20)
            for point in random.sample(points, len(points)//3):
                draw.line([
                    point,
                    (point[0] + random.uniform(-1, 1) * stroke_length,
                     point[1] + random.uniform(-1, 1) * stroke_length)
                ], fill='black', width=2)

    def generate_symbol(self) -> Image.Image:
        max_attempts = 100
        attempts = 0
        
        while attempts < max_attempts:
            image = Image.new('RGB', (self.size, self.size), 'white')
            draw = ImageDraw.Draw(image)
            
            points = self._generate_base_shape()
            
            # Draw with varying line width for calligraphic effect
            for i in range(len(points) - 1):
                width = random.randint(3, 6)
                draw.line([points[i], points[i + 1]], fill='black', width=width)
            
            self._add_decoration(draw, points)
            
            if self._is_unique(image):
                return image
                
            attempts += 1
        
        raise Exception("Failed to generate a unique symbol after maximum attempts")
    
    def save_symbol(self, filename: str):
        image = self.generate_symbol()
        image.save(filename, 'PNG')

def generate_multiple_symbols(num_symbols: int = 28, output_dir: str = "generated_symbols"):
    os.makedirs(output_dir, exist_ok=True)
    
    generator = SymbolGenerator()
    for i in range(num_symbols):
        filename = os.path.join(output_dir, f'symbol_{i+1}.png')
        try:
            generator.save_symbol(filename)
            print(f'Generated unique symbol {i+1}/28')
        except Exception as e:
            print(f"Error generating symbol {i+1}: {str(e)}")
            break

if __name__ == "__main__":
    print("Generating 28 unique symbols...")
    generate_multiple_symbols(28)
    print("Done! Check the 'generated_symbols' folder for your symbols.")