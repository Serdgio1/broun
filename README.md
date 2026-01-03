# Particle Physics Simulation

A particle physics simulation with temperature-based state changes (solid, liquid, gas).

## Requirements

- Python 3.8 or higher
- pygame
- pygame_gui
- numpy

## Installation

### Quick Fix (if you get DIRECTION_LTR import errors)

Run the fix script:
```bash
./fix_dependencies.sh
```

Or manually:
```bash
source venv_mac/bin/activate
pip uninstall -y pygame pygame-ce
pip install pygame-ce pygame_gui numpy
```

### Option 1: Install dependencies directly (recommended for macOS)

```bash
pip3 install pygame-ce pygame_gui numpy
```

**Note:** Use `pygame-ce` instead of `pygame` for better macOS compatibility.

### Option 2: Create a new virtual environment

```bash
# Create a new virtual environment
python3 -m venv venv_mac

# Activate it
source venv_mac/bin/activate

# Install dependencies (use pygame-ce for macOS)
pip install pygame-ce pygame_gui numpy
```

## Running the Application

### If you installed dependencies directly:
```bash
python3 main.py
```

### If you're using a virtual environment:
```bash
# Activate the virtual environment first
source venv_mac/bin/activate

# Then run
python main.py
```

## Controls

- **Temperature Sliders**: Adjust temperature in Celsius or Kelvin
- **R Key**: Reset/restart particles
- **Reset Button**: Reset particles
- **Music Button**: Toggle background music
- **Exit Button**: Quit the application

## Features

- **Color-coded particles**:
  - 🔵 Blue = Solid state (temperature < 0°C)
  - 🔷 Cyan = Liquid state (0-100°C)
  - 🔶 Orange = Gas state (>100°C)

- **Real-time physics simulation** with:
  - Collision detection
  - Gravity effects
  - Viscosity
  - Elasticity
  - Temperature-based state changes

