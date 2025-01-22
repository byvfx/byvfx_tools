# scripts/byvfx/tools/mass_merger.py

import hou

def merge_selected_nodes():
    """
    Creates a merged geometry setup from selected nodes, preserving transforms.
    Each selected node is connected via an object_merge into a single merge node.
    """
    # Get selected nodes
    selected_nodes = hou.selectedNodes()

    # Make sure there are nodes selected
    if not selected_nodes:
        hou.ui.displayMessage('Please select some nodes to merge.', 
                            severity=hou.severityType.Warning,
                            title='Mass Merger')
        return

    # Create a geo node with a descriptive name
    obj_node = hou.node('/obj')
    merge_node = obj_node.createNode('geo', 'merged_geo')

    # Initialize a merge node under the geo node
    merge = merge_node.createNode('merge')

    # Iterate over selected nodes and create object merges
    for i, node in enumerate(selected_nodes):
        # Create object_merge with the original node's name for clarity
        object_merge = merge_node.createNode('object_merge', node.name())

        # Set the object path and preserve transforms
        object_merge.parm('objpath1').set(node.path())
        object_merge.parm('xformtype').set(1)  # Preserve transforms
    
        # Connect to merge node and position nicely
        merge.setInput(i, object_merge)
        object_merge.moveToGoodPosition()

    # Clean up the network layout
    merge.moveToGoodPosition()
    merge_node.layoutChildren()
    
    # Select the new merged geometry node
    merge_node.setSelected(True)