import hou

# Get the selected nodes
selected_nodes = hou.selectedNodes()

# For each selected node
for geo_node in selected_nodes:
    # Get its geometry
    geo = geo_node.geometry()

    # Get a list of all unique shop_materialpath values
    material_paths = list(set([prim.attribValue('shop_materialpath') for prim in geo.prims()]))

    # For each unique shop_materialpath, create a new SOP node and copy the primitives with the same shop_materialpath
    for path in material_paths:
        # Create a new SOP node and name it after the shop_materialpath
        name = path.replace('/', '_')
        new_geo_node = geo_node.parent().createNode('blast', name)
        
        # Connect the new blast node to the selected node
        new_geo_node.setInput(0, geo_node)
        
        # Set the group parameter to the current shop_materialpath
        new_geo_node.parm('group').set('@shop_materialpath="' + path + '"')
        
        # Set the negate parameter to 1 (Delete Non-Selected)
        new_geo_node.parm('negate').set(1)
        
        # Move the new blast node to a good position
        new_geo_node.moveToGoodPosition()

