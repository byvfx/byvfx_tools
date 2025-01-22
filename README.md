# Official page of BYVFX tools

[BYVFX](https://byvfx.com/) | [My Linkedin](https://linkedin.com/brandoncyoung)

> **If my tools are helpful to you, please help star this repo. Thanks!**
# byvfx_tools
official page of BYVFX tools
<div align="center">

<div class="logo">
   <a href="https://shangchenzhou.com/projects/ProPainter/">
      <img src="assets/propainter_logo1_glow.png" style="width:180px">
   </a>
</div>

<h1>Official page of BYVFX tools</h1>

<div>
    <a href='https://byvfx.com/' target='_blank'>BYVFX</a>&emsp;
    <a href='https://linkedin.com/brandoncyoung' target='_blank'>My Linkedin</a>&emsp;

</div>


<div> 
**If my tools are helpful to you , please help star this repo. Thanks!** 
</div> 

---

## Update


- **2023.09.23**: This repo is created.

## TODO
## TODO

- [ ] Add Arnold support for the light converter.  
- [ ] Add Vray support for the light converter.  
- [ ] Add Arnold support for the light converter.  
- [ ] Add Vray support for the light converter.  
- [ ] Add video demos for tools.

---

---

## Contact

If you have any questions, please get in touch with me at [brandon@byvfx.com](mailto:brandon@byvfx.com).

**Installation**: Please use the JSON/package workflow; the package JSON is in the package directory.

If you have any questions, please feel free to reach me out at `brandon@byvfx.com`.

# BYVFX Tools

## Light Converter Tool

### Programmatic Usage

You can use the light converter programmatically in your Python scripts:

```python
import hou
from byvfx.tools.light_converter import convert_light, convert_lights_in_path

# Convert a single light
light = hou.node("/obj/hlight1")
converted = convert_light(light, "redshift")

# Convert all lights in a path
converted_lights = convert_lights_in_path("/obj", "redshift")

# Convert specific lights
selected_lights = hou.selectedNodes()
for light in selected_lights:
    try:
        converted = convert_light(light, "mantra")
        if converted:
            print(f"Converted {light.path()} to {converted.path()}")
    except Exception as e:
        print(f"Failed to convert {light.path()}: {str(e)}")

# Convert lights in multiple contexts
paths = ["/obj", "/obj/geo1", "/obj/subnet1"]
for path in paths:
    try:
        converted = convert_lights_in_path(path, "redshift")
        print(f"Converted {len(converted)} lights in {path}")
    except ValueError as e:
        print(f"Error in {path}: {str(e)}")
```

### Running Tests

To run the unit tests:

```bash
cd /path/to/byvfx_tools
python -m unittest tests/test_light_converter.py