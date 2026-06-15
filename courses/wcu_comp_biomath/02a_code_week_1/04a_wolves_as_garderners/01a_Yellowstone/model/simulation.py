"""
Main simulation orchestration with NEW RULES.
"""

import numpy as np
from model.grid import Grid
from model.environment import Environment
from model.agents import Bison, Wolf
from model.movement import move_wolves, move_all_bison_new_protocol
from model.update_rules import apply_all_updates
from model.interactions import detect_wolf_bison_encounters
from config.config import (
    NX, NY, N_BISON, N_WOLVES, N_STEPS, RANDOM_SEED, WOLF_MOVE_PERIOD
)
from config.initialization import initialize_environment


class Simulation:
    """
    Main simulation class orchestrating all components with NEW RULES.
    """
    
    def __init__(self, nx=None, ny=None, n_bison=None, n_wolves=None, random_seed=None):
        """
        Initialize simulation.
        
        Args:
            nx: Grid width (uses config.NX if None)
            ny: Grid height (uses config.NY if None)
            n_bison: Number of bison (uses config.N_BISON if None)
            n_wolves: Number of wolves (uses config.N_WOLVES if None)
            random_seed: Random seed (uses config.RANDOM_SEED if None)
        """
        # Use defaults from config if not provided
        self.nx = nx if nx is not None else NX
        self.ny = ny if ny is not None else NY
        self.n_bison = n_bison if n_bison is not None else N_BISON
        self.n_wolves = n_wolves if n_wolves is not None else N_WOLVES
        self.random_seed = random_seed if random_seed is not None else RANDOM_SEED
        
        # Set random seed
        if self.random_seed is not None:
            np.random.seed(self.random_seed)
        
        # Initialize grid FIRST
        self.grid = Grid(self.nx, self.ny)
        
        # Initialize environment SECOND
        cell_types, grass_stages, stage5_counter = initialize_environment(
            random_seed=self.random_seed, nx=self.nx, ny=self.ny
        )
        self.environment = Environment(self.grid, cell_types, grass_stages, stage5_counter)
        
        # Initialize agents THIRD (after environment exists)
        self.bison = self._initialize_bison()
        self.wolves = self._initialize_wolves()
        
        # Initialize statistics tracking
        self.statistics = {
            'step': [],
            'n_bison': [],
            'n_wolves': [],
            'forest_cells': [],
            'grassland_cells': [],
            'mean_grass_stage': [],
            'overgrazed_cells': [],
            'stage10_cells': [],
            'wolf_bison_encounters': [],
            'bison_escaped': [],
            'bison_grazed': [],
            'bison_resolved': [],
            'forest_conversions': []
        }
        
        # State history for animation
        self.state_history = []
        self.save_state_history = False
        self.state_save_interval = 1
        
        self.current_step = 0
    
    def _initialize_bison(self):
        """
        Initialize bison at random grassland positions.
        
        Returns:
            list: List of Bison objects
        """
        bison_list = []
        
        # Find all grassland cells
        grassland_cells = []
        for y in range(self.ny):
            for x in range(self.nx):
                if self.environment.is_grassland(x, y):
                    grassland_cells.append((x, y))
        
        # Randomly select positions for bison
        if len(grassland_cells) < self.n_bison:
            print(f"Warning: Not enough grassland cells ({len(grassland_cells)}) for {self.n_bison} bison")
            n_to_place = len(grassland_cells)
        else:
            n_to_place = self.n_bison
        
        selected_positions = np.random.choice(len(grassland_cells), n_to_place, replace=False)
        
        for idx in selected_positions:
            x, y = grassland_cells[idx]
            bison = Bison(x, y)
            bison_list.append(bison)
            self.environment.increment_bison_count(x, y)
        
        return bison_list
    
    def _initialize_wolves(self):
        """
        Initialize wolves at random positions (can be on any cell type).
        
        Returns:
            list: List of Wolf objects
        """
        wolf_list = []
        
        # All cells are valid for wolves
        all_cells = [(x, y) for y in range(self.ny) for x in range(self.nx)]
        
        # Randomly select positions
        selected_positions = np.random.choice(len(all_cells), self.n_wolves, replace=False)
        
        for idx in selected_positions:
            x, y = all_cells[idx]
            wolf = Wolf(x, y)
            wolf_list.append(wolf)
            self.environment.increment_wolf_count(x, y)
        
        return wolf_list
    
    def _record_statistics(self, step_stats):
        """
        Record statistics for current step.
        
        Args:
            step_stats: Dictionary with step-specific statistics
        """
        # Get environment summary
        env_summary = self.environment.get_state_summary()
        
        # Record all statistics
        self.statistics['step'].append(self.current_step)
        self.statistics['n_bison'].append(len(self.bison))
        self.statistics['n_wolves'].append(len(self.wolves))
        self.statistics['forest_cells'].append(env_summary['total_forest'])
        self.statistics['grassland_cells'].append(env_summary['total_grassland'])
        self.statistics['mean_grass_stage'].append(env_summary['mean_grass_stage'])
        self.statistics['overgrazed_cells'].append(env_summary['overgrazed_cells'])
        self.statistics['stage10_cells'].append(env_summary['stage10_cells'])
        self.statistics['wolf_bison_encounters'].append(step_stats.get('encounters', 0))
        self.statistics['bison_escaped'].append(step_stats.get('escaped', 0))
        self.statistics['bison_grazed'].append(step_stats.get('grazed', 0))
        self.statistics['bison_resolved'].append(step_stats.get('resolved', 0))
        self.statistics['forest_conversions'].append(step_stats.get('forest_conversions', 0))
    
    def step(self):
        """
        Execute one simulation time step with NEW PROTOCOL.
        
        NEW ORDER:
        1. Reset occupancy counts
        2. Count current occupancy
        3. Move wolves (only if step is multiple of k)
        4. Detect wolf-bison encounters
        5. Execute 3-phase bison movement protocol
        6. Update grass stages and convert to forest
        7. Record statistics
        """
        step_stats = {}
        
        # 1. Reset occupancy tracking
        self.environment.reset_occupancy()
        
        # 2. Count current occupancy
        for bison in self.bison:
            self.environment.increment_bison_count(bison.x, bison.y)
        
        for wolf in self.wolves:
            self.environment.increment_wolf_count(wolf.x, wolf.y)
        
        # 3. Move wolves (only every k-th step)
        if self.current_step % WOLF_MOVE_PERIOD == 0:
            move_wolves(self.wolves, self.grid, self.environment)
        
        # 4. Detect encounters (before bison escape)
        step_stats['encounters'] = detect_wolf_bison_encounters(
            self.bison, self.wolves, self.grid, self.environment
        )
        
        # 5. Execute NEW 3-phase bison movement protocol
        movement_stats = move_all_bison_new_protocol(
            self.bison, self.grid, self.environment
        )
        step_stats.update(movement_stats)
        
        # 6. Update grass stages and convert to forest
        update_stats = apply_all_updates(self.environment)
        step_stats.update(update_stats)
        
        # 7. Record statistics
        self._record_statistics(step_stats)
        
        # 8. Save state for animation if enabled
        if self.save_state_history and (self.current_step % self.state_save_interval == 0):
            self.state_history.append(self.get_current_state())
        
        # Increment step counter
        self.current_step += 1
    
    def run(self, n_steps=None, verbose=False, save_history=False, history_interval=1):
        """
        Run simulation for specified number of steps.
        
        Args:
            n_steps: Number of steps to run (uses config.N_STEPS if None)
            verbose: If True, print progress information
            save_history: If True, save state history for animation
            history_interval: Interval for saving states (e.g., 5 = save every 5 steps)
        """
        if n_steps is None:
            n_steps = N_STEPS
        
        # Enable state history saving
        self.save_state_history = save_history
        self.state_save_interval = history_interval
        
        # Save initial state
        if save_history:
            self.state_history.append(self.get_current_state())
        
        if verbose:
            print(f"\nStarting simulation:")
            print(f"  Grid: {self.nx} x {self.ny}")
            print(f"  Bison: {len(self.bison)}")
            print(f"  Wolves: {len(self.wolves)}")
            print(f"  Steps: {n_steps}")
            print(f"  Wolf move period: {WOLF_MOVE_PERIOD}")
            if save_history:
                print(f"  Saving state history every {history_interval} steps")
            print()
        
        for step in range(n_steps):
            self.step()
            
            if verbose and (step % 50 == 0 or step == n_steps - 1):
                env_summary = self.environment.get_state_summary()
                print(f"Step {step:4d}: "
                      f"Forest={env_summary['total_forest']:4d}, "
                      f"Grass={env_summary['mean_grass_stage']:.2f}, "
                      f"Overgrazed={env_summary['overgrazed_cells']:4d}")
        
        if verbose:
            print(f"\nSimulation complete!")
            if save_history:
                print(f"Saved {len(self.state_history)} state snapshots")
            print(f"Final statistics:")
            print(f"  Forest cells: {self.statistics['forest_cells'][-1]}")
            print(f"  Mean grass stage: {self.statistics['mean_grass_stage'][-1]:.2f}")
            print(f"  Overgrazed cells: {self.statistics['overgrazed_cells'][-1]}")
            print(f"  Total encounters: {sum(self.statistics['wolf_bison_encounters'])}")
    
    def get_current_state(self):
        """
        Get current state of simulation for visualization.
        
        Returns:
            dict: Current state including all arrays and agent positions
        """
        return {
            'step': self.current_step,
            'cell_types': self.environment.cell_types.copy(),
            'grass_stages': self.environment.grass_stages.copy(),
            'bison_count': self.environment.bison_count.copy(),
            'wolf_count': self.environment.wolf_count.copy(),
            'bison_positions': [(b.x, b.y) for b in self.bison],
            'wolf_positions': [(w.x, w.y) for w in self.wolves],
            'n_bison': len(self.bison),
            'n_wolves': len(self.wolves)
        }