"""
Agent classes for bison and wolves.
"""

import numpy as np


class Agent:
    """
    Base class for all agents.
    """
    
    def __init__(self, x, y):
        """
        Initialize agent at position (x, y).
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.x = x
        self.y = y
    
    def move_to(self, new_x, new_y):
        """
        Move agent to new position.
        
        Args:
            new_x: New X coordinate
            new_y: New Y coordinate
        """
        self.x = new_x
        self.y = new_y
    
    def get_position(self):
        """
        Get current position.
        
        Returns:
            tuple: (x, y) coordinates
        """
        return (self.x, self.y)


class Bison(Agent):
    """
    Bison agent.
    """
    
    def __init__(self, x, y):
        """
        Initialize bison at position (x, y).
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        super().__init__(x, y)
        self.agent_type = "bison"
    
    def __repr__(self):
        return f"Bison(x={self.x}, y={self.y})"


class Wolf(Agent):
    """
    Wolf agent.
    """
    
    def __init__(self, x, y):
        """
        Initialize wolf at position (x, y).
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        super().__init__(x, y)
        self.agent_type = "wolf"
    
    def __repr__(self):
        return f"Wolf(x={self.x}, y={self.y})"