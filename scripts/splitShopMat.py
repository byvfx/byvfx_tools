import hou
import re

# Get the selected nodes
selected_nodes = hou.selectedNodes()

# Check if a geometry node is selected
if not selected_nodes or not selected_nodes[0].geometry():
    raise Exception("Please select a geometry node.")

geo_node = selected_nodes[0]

# Get the shop_materialpath attribute from primitives
path_attrib = geo_node.geometry().findPrimAttrib("shop_materialpath")

# If there is no shop_materialpath attribute, display a message and raise an exception
if path_attrib is None:
    hou.ui.displayMessage(
        "The selected geometry node does not have a shop_materialpath attribute.",
        buttons=['OK'],
        severity=hou.severityType.Error,
    )
    raise Exception("The selected geometry node does not have a shop_materialpath attribute.")

# Split the shop_materialpath into different sections
sections = [set(prim.attribValue(path_attrib).split('/')[i] for prim in geo_node.geometry().prims() if len(prim.attribValue(path_attrib).split('/')) > i) for i in range(max(len(prim.attribValue(path_attrib).split('/')) for prim in geo_node.geometry().prims()))]

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
    blast_node = geo_node.createOutputNode("blast", node_name + "_blast")

    # Update parameters of the new blast node
    blast_node.parm("group").set('@shop_materialpath=*' + path + '*')
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

