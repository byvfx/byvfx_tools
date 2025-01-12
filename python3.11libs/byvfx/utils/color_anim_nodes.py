import hou
def color_animated_nodes():
    user_color = hou.ui.selectColor()
    
    if user_color is None:
        return
        
    network = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if not network:
        raise RuntimeError("No network editor pane found")
        
    current_node = network.currentNode()
    if not current_node:
        raise RuntimeError("No current node found")
    
    parent = current_node.parent()
    
    for node in parent.children():
        is_animated = False
        for parm in node.parms():
            if parm.isTimeDependent():
                is_animated = True
                break
                
        if is_animated:
            node.setColor(user_color)

color_animated_nodes()