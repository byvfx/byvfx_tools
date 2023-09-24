"""
author:     brandon young | http://www.byvfx.com
date:       2023.07.25
version:    .6
about:      this script will split an alembic node into separate nodes based on the path attribute
            it will also add a match size node to each blast node and set the justify y to min

"""
import hou
import re

# Get the selected nodes
selected_nodes = hou.selectedNodes()

# Check if an Alembic SOP node is selected
if not selected_nodes or selected_nodes[0].type().name() != "alembic":
    raise Exception("Please select an Alembic SOP node.")

alembic_node = selected_nodes[0]

# Get the path attribute from primitives
path_attrib = alembic_node.geometry().findPrimAttrib("path")

# If there is no path attribute, display a message and raise an exception
if path_attrib is None:
    hou.ui.displayMessage(
        "The selected Alembic SOP node does not have a path attribute.",
        buttons=['OK'],
        severity=hou.severityType.Error,
    )
    raise Exception("The selected Alembic SOP node does not have a path attribute.")

# Split the path into different sections
sections = [set(prim.attribValue(path_attrib).split('/')[i] for prim in alembic_node.geometry().prims() if len(prim.attribValue(path_attrib).split('/')) > i) for i in range(max(len(prim.attribValue(path_attrib).split('/')) for prim in alembic_node.geometry().prims()))]

# Create a message with the sections and their indices
message = "\n".join(f"{i}: {section if section else 'Everything'}" for i, section in enumerate(sections))

# Ask the user to choose a section
section = hou.ui.readInput(
    "Please choose a section for splitting the geometry:\n" + message,
    buttons=["OK"],
)[1]

if not section.isdigit() or int(section) not in range(len(sections)):
    hou.ui.displayMessage(
        "Invalid section index. Please enter a number from the list.",
        buttons=['OK'],
        severity=hou.severityType.Error,
    )
    raise Exception("Invalid section index.")

# Get the unique paths for the chosen section
unique_paths = sections[int(section)]

# Ask the user if they want to center and justify the object
center_justify = hou.ui.displayMessage(
    "Do you want to center and justify the object?",
    buttons=["Yes", "No"],
    severity=hou.severityType.Message,
    default_choice=0,
    close_choice=1,
)

# Loop over each unique path
for path in unique_paths:
    # Sanitize the path to create a valid node name
    node_name = re.sub(r'\W+', '_', path)

    # Create a new blast node for each unique path
    blast_node = alembic_node.createOutputNode("blast", node_name + "_blast")

    # Update parameters of the new blast node
    blast_node.parm("group").set('@path=*' + path + '*')
    blast_node.parm("negate").set(1)

    blast_node.setDisplayFlag(True)
    blast_node.setRenderFlag(True)
    
    # If the user chose to center and justify the object
    if center_justify == 0:
        # Create a match size node after each blast node
        match_size_node = blast_node.createOutputNode("matchsize", node_name + "_matchsize")

        # Justify Y to min
        match_size_node.parm("justify_y").set(1)  # 1 = Min
        
        # Create a null with the OUT prefix
        null_node = match_size_node.createOutputNode("null", "OUT_" + node_name)
    else:
        # Create a null with the OUT prefix
        null_node = blast_node.createOutputNode("null", "OUT_" + node_name)