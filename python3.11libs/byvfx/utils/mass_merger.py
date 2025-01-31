# scripts/byvfx/tools/mass_merger.py

import hou
from typing import Optional

def merge_selected_nodes() -> Optional[hou.Node]:
    """Creates a merged geometry setup from selected nodes, preserving transforms.

    Creates a new geometry node containing object_merge nodes for each selected node,
    all feeding into a single merge node. Transforms are preserved.

    Returns:
        hou.Node: The created merge geometry node, or None if operation failed
    """
    selected_nodes = hou.selectedNodes()

    if not selected_nodes:
        hou.ui.displayMessage('Please select some nodes to merge.', 
                            severity=hou.severityType.Warning,
                            title='Mass Merger')
        return None

    try:
        obj_node = hou.node('/obj')
        
        name = hou.ui.readInput('Enter name for the merged node container:', buttons=('OK', 'Cancel'),severity=hou.severityType.ImportantMessage,default_choice=0, close_choice=1, title='Mass Merger')[1]
        if not name:
            name = 'merged_geo'
        merge_node = obj_node.createNode('geo', name)
        merge = merge_node.createNode('merge')

        for i, node in enumerate(selected_nodes):
            object_merge = merge_node.createNode('object_merge', node.name())
            object_merge.parm('objpath1').set(node.path())
            object_merge.parm('xformtype').set(1)  # Preserve transforms
            merge.setInput(i, object_merge)
            object_merge.moveToGoodPosition()

        merge.moveToGoodPosition()
        merge_node.layoutChildren()
        merge_node.setSelected(True)
        
        return merge_node

    except hou.OperationFailed as e:
        hou.ui.displayMessage(f'Failed to create merge setup: {str(e)}',
                            severity=hou.severityType.Error,
                            title='Mass Merger Error')
        return None