from typing import List
from enum import Enum
from abc import ABC, abstractmethod
import pygame
import sys

import rich

class PizzaCrusts(Enum):
    CHEESEBURST = "cheese burst"
    THIN = "thin"
    REGULAR = "regular"

class Pizza:
    def __init__(self):
        self.toppings: List[str] = []
        self.crust: PizzaCrusts = None
    
    def add_topping(self, topping):
        self.toppings.append(topping)
    
    def select_crust(self, crust: PizzaCrusts):
        self.crust = crust.value
    
    def display_order(self):
        rich.print(
            "🍕[b gold3] Your order is:"
            f"toppings: {self.toppings}"
            f"crust: {self.crust}"
        )

class PizzaBuilder(ABC):

    def __init__(self):
        self.pizza = None
    
    def bake_new_pizza(self):
        self.pizza = Pizza()
    
    @abstractmethod
    def add_veg_topping(self):
        pass

    @abstractmethod
    def add_non_veg_topping(self):
        pass
    
    @abstractmethod
    def add_cheese_topping(self):
        pass

    @abstractmethod
    def set_crust(self):
        pass

    def get_pizza(self):
        return self.pizza

class PepperoniPizzaBuilder(PizzaBuilder):

    def add_non_veg_topping(self):
        self.pizza.add_topping("pepperoni")
    
    def add_cheese_topping(self):
        self.pizza.add_topping("mozarella")
    
    def add_veg_topping(self):
        self.pizza.add_topping("mushrooms")
    
    def set_crust(self):
        self.pizza.select_crust(PizzaCrusts.REGULAR)

class FarmhousePizzaBuilder(PizzaBuilder):

    def add_non_veg_topping(self):
        pass

    def add_veg_topping(self):
        self.pizza.add_topping("mushrooms")
        self.pizza.add_topping("peppers")
        self.pizza.add_topping("onions")
        self.pizza.add_topping("corn")
    
    def add_cheese_topping(self):
        self.pizza.add_topping("mozarella")
    
    def set_crust(self):
        self.pizza.select_crust(PizzaCrusts.CHEESEBURST)
    
class PizzaDirector:

    def __init__(self, builder: PizzaBuilder):
        self.builder = builder
    
    def build_pizza(self):

        self.builder.bake_new_pizza()

        self.builder.add_non_veg_topping()
        self.builder.add_veg_topping()
        self.builder.add_cheese_topping()
        self.builder.set_crust()

        return self.builder.get_pizza()

def draw_text(
        screen,
        text,
        x,
        y,
        font,
        color,
):
    text_surface = font.render(
        text,
        True,
        color,
    )

    screen.blit(text_surface, (x,y))

pygame.init()
screen = pygame.display.set_mode(
    (600,400),
)
pygame.display.set_caption(
    "🍕 Pizza Builder"
)
font = pygame.font.Font(
    pygame.font.get_default_font(), 18
)

pepperoni_builder = PepperoniPizzaBuilder()
director = PizzaDirector(
    pepperoni_builder,
)
pepperoni_pizza = director.build_pizza()

farmhouse_builder = FarmhousePizzaBuilder()
director.builder = farmhouse_builder
farmhouse_pizza = director.build_pizza()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    screen.fill(
        (255,255,255),
    )
    draw_text(
        screen,
        "🐷 Pepperoni Pizza:",
        10,
        10,
        font,
        (0,0,0),
    )
    for idx, topping in enumerate(pepperoni_pizza.toppings):
        draw_text(
            screen,
            f"- {topping}",
            10,
            40 + idx*30,
            font,
            (0,0,0),
        )

    draw_text(
        screen,
        "🍄 Farmhouse Pizza",
        300,
        10,
        font,
        (0,0,0),
    )
    for idx, topping in enumerate(farmhouse_pizza.toppings):
        draw_text(
            screen,
            f"- {topping}",
            300,
            40 + idx*30,
            font,
            (0,0,0),
        )

    pygame.display.flip()
    pygame.time.delay(100)
