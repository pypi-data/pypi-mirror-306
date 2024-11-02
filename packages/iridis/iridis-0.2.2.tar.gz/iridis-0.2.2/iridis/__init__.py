from .color import Color  
from .color_prints import (
    print_error,
    print_rainbow,
    print_title,
    print_with_color,
)
from .utils import get_number_from_user 

# Define the public API
__all__ = [
    "Color",  
    "print_error", 
    "print_rainbow", 
    "print_title",  
    "print_with_color",
    "get_number_from_user", 
]
