import hou
from typing import Optional

def merge_selected_nodes() -> Optional[hou.Node]:
    """
    Merges selected nodes into a single merge node.
    
    Allows the user to choose between creating a merge node in the /obj context
    or selecting a custom location for the merge.
    
    Returns:
        Optional[hou.Node]: The newly created merge node, or None if the operation failed
    """
    
    try:
        # Get selected nodes
        selected_nodes = hou.selectedNodes()
        
        if not selected_nodes:
            hou.ui.displayMessage(
                "No nodes selected.",
                severity=hou.severityType.Warning,
                title='Mass Merger'
            )
            return None
        
        # Ask user where to place the merged node
        location_choice = hou.ui.displayMessage(
            "Where do you want to merge the nodes?",
            buttons=('Create at Obj level', 'Custom location', 'Cancel'),
            default_choice=0, 
            close_choice=2,
            title='Mass Merger'
        )
                    
        if location_choice == 2:  # Cancel
            return None
            
        if location_choice == 0:  # Create at Obj level
            return _create_obj_level_merge(selected_nodes)
        else:  # Custom Location
            return _create_custom_location_merge(selected_nodes)

    except hou.OperationFailed as e:
        hou.ui.displayMessage(
            f'Operation failed: {str(e)}',
            severity=hou.severityType.Error,
            title='Mass Merger'
        )
        return None


def _create_obj_level_merge(selected_nodes) -> Optional[hou.Node]:
    """Create merge at /obj level with proper organization."""
    try:
        name = hou.ui.readInput(
            'Enter name for the merged node container:', 
            buttons=('OK', 'Cancel'),
            severity=hou.severityType.ImportantMessage,
            default_choice=0, 
            close_choice=1, 
            title='Mass Merger'
        )[1]
        
        if not name:
            name = 'merged_geo'
            
        # Create container at /obj level
        obj_node = hou.node('/obj')
        merge_node = obj_node.createNode('geo', name)
        merge = merge_node.createNode('merge')
        null_node = merge_node.createNode('null', 'OUT')
        
        # Connect the merge to the OUT null
        null_node.setInput(0, merge)
        
        # Set display/render flags on the null
        null_node.setDisplayFlag(True)
        null_node.setRenderFlag(True)
        
        # Create object merges for each selected node
        for i, node in enumerate(selected_nodes):
            obj_merge = merge_node.createNode('object_merge')
            obj_merge.parm('objpath1').set(node.path())
            obj_merge.parm('xformtype').set(1)  # Preserve transforms
            merge.setInput(i, obj_merge)
            
        # Layout the network for clarity
        merge_node.layoutChildren()
        
        # Create network box for organization
        network_box = merge_node.createNetworkBox()
        network_box.setComment("Mass Merger Generated")
        for node in merge_node.children():
            network_box.addNode(node)
            
        # Position and select the new container
        merge_node.setPosition([0, 0])
        merge_node.setSelected(True)
        
        return merge_node
        
    except Exception as e:
        hou.ui.displayMessage(
            f'Error creating merge: {str(e)}',
            severity=hou.severityType.Error,
            title='Mass Merger'
        )
        return None


def _create_custom_location_merge(selected_nodes) -> Optional[hou.Node]:
    """Create merge at custom user-selected location."""
    try:
        # Use selectNode without a filter - allow selecting any valid container
        path = hou.ui.selectNode(
            title='Select Merge Location',
            node_type_filter=hou.nodeTypeFilter.Obj
        )
        
        if not path:  # User cancelled selection
            return None
            
        parent_node = hou.node(path)
        
        if not parent_node:
            hou.ui.displayMessage(
                f'Invalid path: {path}',
                severity=hou.severityType.Error,
                title='Mass Merger'
            )
            return None
        
        # Check if the parent node can contain nodes (safe check)
        try:
            test_node = parent_node.createNode('null', '__test_node__')
            test_node.destroy()
        except Exception:
            hou.ui.displayMessage(
                f'Cannot create nodes at this location: {path}',
                severity=hou.severityType.Error,
                title='Mass Merger'
            )
            return None
            
        name = hou.ui.readInput(
            'Enter name prefix for the merged nodes:',
            buttons=('OK', 'Cancel'),
            severity=hou.severityType.ImportantMessage,
            default_choice=0, 
            close_choice=1,
            title='Mass Merger'
        )[1]
        
        if name is None:  # User cancelled
            return None
            
        if not name:
            name = 'merged'
        
        # Create merge node at the specified location
        merge = parent_node.createNode('merge', f"{name}_merge")
        null_node = parent_node.createNode('null', f"{name}_OUT")
        
        # Connect the merge to the OUT null
        null_node.setInput(0, merge)
        
        # Set display/render flags on the null
        null_node.setDisplayFlag(True)
        null_node.setRenderFlag(True)
        
        # Connect selected nodes to the merge via object_merge nodes
        for i, node in enumerate(selected_nodes):
            obj_merge = parent_node.createNode('object_merge', f"{name}_{node.name()}")
            obj_merge.parm('objpath1').set(node.path())
            obj_merge.parm('xformtype').set(1)  # Preserve transforms
            merge.setInput(i, obj_merge)
        
        # Layout the network for clarity
        parent_node.layoutChildren()
        
        # Select the new nodes for visibility
        merge.setSelected(True)
        null_node.setSelected(True)
        
        return parent_node  # Return the parent node in this case
                
    except Exception as e:
        hou.ui.displayMessage(
            f'Error creating merge: {str(e)}',
            severity=hou.severityType.Error,
            title='Mass Merger'
        )
        return None