import random
import math
from typing import List, Tuple, Set
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
        """Generate a hash for the symbol to check uniqueness."""
        # Convert to numpy array and normalize
        img_array = np.array(image)
        # Resize to smaller dimension for faster comparison while maintaining distinctiveness
        img_small = Image.fromarray(img_array).resize((50, 50))
        # Convert to bytes and hash
        return hashlib.md5(np.array(img_small).tobytes()).hexdigest()

    def _is_unique(self, image: Image.Image) -> bool:
        """Check if the symbol is unique compared to previously generated ones."""
        symbol_hash = self._get_symbol_hash(image)
        if symbol_hash in self.generated_hashes:
            return False
        self.generated_hashes.add(symbol_hash)
        return True

    def _generate_base_shape(self) -> List[Tuple[float, float]]:
        """Generate base shape type with additional variation parameters."""
        shape_type = random.choice([
            self._generate_star,
            self._generate_polygon,
            self._generate_spiral,
            self._generate_cross,
            self._generate_wave_circle,
            self._generate_diamond_pattern,
            self._generate_zigzag
        ])
        return shape_type()
    
    def _generate_star(self) -> List[Tuple[float, float]]:
        points = []
        num_points = random.randint(4, 9)
        inner_radius = self.effective_size * random.uniform(0.1, 0.2)
        outer_radius = self.effective_size * random.uniform(0.35, 0.45)
        rotation = random.uniform(0, math.pi)
        
        for i in range(num_points * 2):
            angle = rotation + (i * math.pi) / num_points
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = math.cos(angle) * radius + self.center
            y = math.sin(angle) * radius + self.center
            points.append((x, y))
        return points
    
    def _generate_polygon(self) -> List[Tuple[float, float]]:
        points = []
        num_sides = random.randint(3, 8)
        radius = self.effective_size * random.uniform(0.3, 0.45)
        rotation = random.uniform(0, math.pi * 2)
        skew = random.uniform(0.8, 1.2)
        
        for i in range(num_sides):
            angle = rotation + (i * 2 * math.pi / num_sides)
            x = math.cos(angle) * radius * skew + self.center
            y = math.sin(angle) * radius + self.center
            points.append((x, y))
        return points
    
    def _generate_spiral(self) -> List[Tuple[float, float]]:
        points = []
        num_points = random.randint(12, 20)
        max_radius = self.effective_size * random.uniform(0.3, 0.45)
        rotations = random.uniform(1.5, 3.0)
        
        for i in range(num_points):
            angle = (i * 2 * math.pi * rotations) / num_points
            radius = (i / num_points) * max_radius
            x = math.cos(angle) * radius + self.center
            y = math.sin(angle) * radius + self.center
            points.append((x, y))
        return points
    
    def _generate_cross(self) -> List[Tuple[float, float]]:
        size = self.effective_size * random.uniform(0.35, 0.45)
        offset = random.uniform(0.3, 0.7)
        rotation = random.uniform(0, math.pi / 4)
        
        base_points = [
            (-size, 0), (size, 0),
            (0, -size), (0, size),
            (-size * offset, -size * offset),
            (size * offset, size * offset),
            (-size * offset, size * offset),
            (size * offset, -size * offset)
        ]
        
        # Rotate points
        points = []
        for x, y in base_points:
            rx = x * math.cos(rotation) - y * math.sin(rotation)
            ry = x * math.sin(rotation) + y * math.cos(rotation)
            points.append((rx + self.center, ry + self.center))
            
        return points
    
    def _generate_wave_circle(self) -> List[Tuple[float, float]]:
        points = []
        num_points = random.randint(24, 36)
        base_radius = self.effective_size * random.uniform(0.25, 0.35)
        wave_amplitude = self.effective_size * random.uniform(0.08, 0.15)
        wave_frequency = random.randint(3, 7)
        phase = random.uniform(0, math.pi * 2)
        
        for i in range(num_points):
            angle = (i * 2 * math.pi) / num_points
            radius = base_radius + math.sin(angle * wave_frequency + phase) * wave_amplitude
            x = math.cos(angle) * radius + self.center
            y = math.sin(angle) * radius + self.center
            points.append((x, y))
        return points
    
    def _generate_diamond_pattern(self) -> List[Tuple[float, float]]:
        points = []
        size = self.effective_size * random.uniform(0.3, 0.4)
        num_points = random.randint(3, 5)
        rotation = random.uniform(0, math.pi / 4)
        
        for i in range(num_points):
            angle = (i * 2 * math.pi / num_points) + rotation
            x1 = math.cos(angle) * size
            y1 = math.sin(angle) * size
            x2 = math.cos(angle + math.pi/num_points) * (size * 0.5)
            y2 = math.sin(angle + math.pi/num_points) * (size * 0.5)
            points.extend([
                (x1 + self.center, y1 + self.center),
                (x2 + self.center, y2 + self.center)
            ])
        return points

    def _generate_zigzag(self) -> List[Tuple[float, float]]:
        points = []
        num_segments = random.randint(6, 10)
        radius = self.effective_size * random.uniform(0.3, 0.4)
        height = self.effective_size * random.uniform(0.1, 0.2)
        rotation = random.uniform(0, math.pi * 2)
        
        for i in range(num_segments + 1):
            angle = rotation + (i * 2 * math.pi / num_segments)
            r1 = radius - height if i % 2 else radius + height
            x = math.cos(angle) * r1 + self.center
            y = math.sin(angle) * r1 + self.center
            points.append((x, y))
        return points

    def _add_decoration(self, draw: ImageDraw.Draw, points: List[Tuple[float, float]]):
        """Add decorative elements with more variations."""
        decoration_types = ['dots', 'lines', 'none', 'circle', 'crosses', 'inner_shape']
        weights = [2, 2, 1, 2, 1, 2]  # Adjust probability of each type
        decoration_type = random.choices(decoration_types, weights=weights)[0]
        
        if decoration_type == 'dots':
            dot_size = random.randint(4, 7)
            for point in points:
                draw.ellipse([
                    (point[0] - dot_size, point[1] - dot_size),
                    (point[0] + dot_size, point[1] + dot_size)
                ], fill='black')
                
        elif decoration_type == 'lines':
            num_lines = random.randint(3, len(points))
            selected_points = random.sample(points, num_lines)
            for point in selected_points:
                draw.line([
                    (self.center, self.center),
                    point
                ], fill='black', width=2)
                
        elif decoration_type == 'circle':
            radius = self.effective_size * random.uniform(0.15, 0.25)
            draw.ellipse([
                (self.center - radius, self.center - radius),
                (self.center + radius, self.center + radius)
            ], outline='black', width=2)
            
        elif decoration_type == 'crosses':
            size = 8
            for point in random.sample(points, len(points)//2):
                draw.line([
                    (point[0] - size, point[1]),
                    (point[0] + size, point[1])
                ], fill='black', width=2)
                draw.line([
                    (point[0], point[1] - size),
                    (point[0], point[1] + size)
                ], fill='black', width=2)
                
        elif decoration_type == 'inner_shape':
            scale = random.uniform(0.4, 0.6)
            inner_points = [(
                (p[0] - self.center) * scale + self.center,
                (p[1] - self.center) * scale + self.center
            ) for p in points]
            for i in range(len(inner_points)):
                p1 = inner_points[i]
                p2 = inner_points[(i + 1) % len(inner_points)]
                draw.line([p1, p2], fill='black', width=2)

    def generate_symbol(self) -> Image.Image:
        """Generate a unique symbol as a PIL Image."""
        max_attempts = 100
        attempts = 0
        
        while attempts < max_attempts:
            image = Image.new('RGB', (self.size, self.size), 'white')
            draw = ImageDraw.Draw(image)
            
            points = self._generate_base_shape()
            
            # Draw the main shape
            for i in range(len(points)):
                p1 = points[i]
                p2 = points[(i + 1) % len(points)]
                draw.line([p1, p2], fill='black', width=4)
            
            # Add decorative elements
            self._add_decoration(draw, points)
            
            # Check if the symbol is unique
            if self._is_unique(image):
                return image
                
            attempts += 1
        
        raise Exception("Failed to generate a unique symbol after maximum attempts")
    
    def save_symbol(self, filename: str):
        """Generate and save a unique symbol to a PNG file."""
        image = self.generate_symbol()
        image.save(filename, 'PNG')

def generate_multiple_symbols(num_symbols: int = 28, output_dir: str = "generated_symbols"):
    """Generate multiple unique symbols and save them as PNGs."""
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