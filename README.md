<div align="center">
  <h1>BYVFX Tools</h1>
</div>


<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue.svg)](https://linkedin.com/brandoncyoung)
[![Website](https://img.shields.io/badge/Website-BYVFX-green.svg)](https://byvfx.com/)
[![Email](https://img.shields.io/badge/Email-Contact-red.svg)](mailto:brandon@byvfx.com)

</div>

## Overview

### BYVFX Tools is a collection of utilities designed to streamline FX/CG workflows

## ⚡ Core Features

Pre-Built Simulation Caches
Our extensive library of pre-built caches saves valuable simulation time and ensures consistent, high-quality results.

### Geometry Caches

Debris Library: Highly detailed, physically accurate debris including rocks, paper, metal pieces, glass, and vegetation
Electrical Effects: Ready-to-use electrical animation caches for quick implementation
Production-Ready: All caches are optimized for production use with clean topology and efficient file sizes

### VDB Caches

Fire Effects: Realistic fire simulations for various scenarios
Smoke Collection: Comprehensive range from subtle dust hits to massive smoke plumes
Explosion Library: Ready-to-use explosion caches for immediate integration

### Interactive Tools (HDAs)

Powerful Houdini Digital Assets designed for artist-friendly workflow enhancement.
Effects Generation

Spark & Smoke Tool: Interactive spark and smoke generation with frame-specific control
Lightning & Electrical: Dynamic electrical effect generation system
Volume Particle Tool: Advanced particle system (Afterburn clone)
Wind Generator: Professional-grade vector field generation for pyro effects
Liquid Hit Tool: Fluid simulation setup with artist-friendly controls

### Production Utilities

Camera Setup: Automated camera creation with plate integration and resolution matching
Projection Tool: Sophisticated multilayered material projection system
VEX Snippet Manager: Efficient code management system for VEX snippets

### Utility Tools

Workflow enhancers designed to speed up common production tasks.

ABC Splitter: Right-click functionality for efficient Alembic file management
Animation Node Highlighter: Visual identification system for animated SOP nodes
Geometry Splitter: Advanced splitting tools for ABCs and geometry based on attributes

Gallery FX Setups
Comprehensive collection of production-ready effect setups and examples.
Ready-to-Use Setups

RBD Examples: Practical setups including bending metal and constraint networks
PYRO Configurations: Production-optimized Pyro setups with multiple disturb and turbulence fields
Simulation Samples: Curated examples for Vellum, POP, and MPM simulations

## 🚀 Upcoming Features

- Arnold support for the light converter
- Vray support for the light converter
- Octane support for the light converter
- Comprehensive video demonstrations
- Extended documentation and usage examples

# 📦 Installation

BYVFX Tools uses Houdini's package management system for seamless integration into your pipeline. The package system ensures that all tools, HDAs, and resources are properly organized and loaded in your Houdini environment.

## Using Houdini Packages

1. Create a `packages` directory in your Houdini preferences if it doesn't exist:

```bash
# Windows
%USERPROFILE%/Documents/HOUDINIVERSION/packages

# Linux
~/HOUDINIVERSION/packages

# macOS
~/Library/Preferences/houdini/HOUDINIVERSION/packages
```

1. Download the BYVFX Tools package and extract it to a location of your choice:

2. Create a new JSON file named `BYVFX.json` in your packages directory with the following content or use the one provided:

```json
{
    "enable" : true,
    "env": 
    
       [ {"HOUDINI_PATH" : "E:\\_houdiniFiles\\BY_python\\byvfx_tools"}]

}
```

### Verifying Installation

After installing, you can verify the setup by:

1. Opening Houdini and checking the package is loaded:

```python
# Run in Python Shell
hou.packageRegistry().packages()
```

1. Checking environment variables:

```python
# Run in Python Shell
import os
print(os.getenv("BYVFX"))
```

### Troubleshooting

If you encounter any issues:

1. Verify your `HOUDINI_PATH` includes the package directory
2. Check that all environment variables are properly set
3. Ensure file permissions are correct
4. Restart Houdini after making changes

For additional help, contact [brandon@byvfx.com](mailto:brandon@byvfx.com)

## 📬 Contact & Support

- Email: [brandon@byvfx.com](mailto:brandon@byvfx.com)
- Website: [byvfx.com](https://byvfx.com)
- LinkedIn: [Connect with me](https://linkedin.com/brandoncyoung)

---

If you find BYVFX Tools helpful, please consider starring this repository. Your support helps us continue development! ⭐
