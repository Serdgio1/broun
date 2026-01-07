# 🔬 Particle Physics Simulation

An interactive particle physics simulation with temperature-based state changes (solid, liquid, gas). Watch particles transform and interact based on temperature in real-time!

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-ce-2.5+-green.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

## ✨ Features

- **🌡️ Temperature-based physics**: Particles change behavior based on temperature
  - 🔵 **Solid state** (< 0°C): Particles vibrate in place
  - 🔷 **Liquid state** (0-100°C): Particles flow with gravity and viscosity
  - 🔶 **Gas state** (> 100°C): Particles move freely with increased velocity

- **⚙️ Interactive controls**:
  - Real-time temperature adjustment (Celsius & Kelvin)
  - Customizable particle count and radius
  - Reset functionality
  - Background music toggle

- **🎮 Real-time physics simulation**:
  - Collision detection between particles
  - Gravity effects
  - Viscosity modeling
  - Elastic collisions
  - Visual particle effects with glow

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/Serdgio1/broun.git
cd broun
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

**Note for macOS users**: The project uses `pygame-ce` instead of `pygame` for better compatibility. If you encounter import errors, use:
```bash
pip install pygame-ce pygame_gui numpy
```

### Running the Application

```bash
python3 main.py
```

Or with virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 🎮 Controls

| Action | Description |
|--------|-------------|
| **Temperature Sliders** | Adjust temperature in Celsius or Kelvin |
| **R Key** | Reset/restart particles |
| **Reset Button** | Reset particles to initial state |
| **Music Button** | Toggle background music on/off |
| **Exit Button** | Quit the application |

## 📦 Building Executables

### macOS
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### Windows
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

The executable will be created in the `dist/` directory.

## 🏗️ Project Structure

```
broun/
├── main.py              # Main application code
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── images/             # UI images and icons
└── music/              # Background music (optional)
```

## 🔧 Technical Details

- **Physics Engine**: Custom particle system with collision detection
- **Rendering**: Pygame for graphics and UI
- **UI Framework**: pygame_gui for interactive controls
- **Math Library**: NumPy for efficient calculations

### Physics Parameters

- **Gravity**: 0.2 (affects liquid and gas states)
- **Viscosity**: 0.98 (liquid state damping)
- **Elasticity**: 0.9 (collision energy retention)
- **Particle Radius**: 7 pixels (configurable)
- **Default Particle Count**: 150 (configurable)

## 🎨 Screenshots

*Add screenshots here to showcase the simulation in different states*

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Serdgio1**

- GitHub: [@Serdgio1](https://github.com/Serdgio1)

## 🙏 Acknowledgments

- Built with [Pygame CE](https://github.com/pygame-community/pygame-ce)
- UI powered by [pygame_gui](https://github.com/MyreMylar/pygame_gui)
- Physics calculations using [NumPy](https://numpy.org/)

---

⭐ If you find this project interesting, consider giving it a star!
