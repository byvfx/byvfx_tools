import hou

# Get selected nodes
selected_nodes = hou.selectedNodes()

# Make sure there are nodes selected
if not selected_nodes:
    print('No nodes selected.')
else:
    # Create a geo node
    obj_node = hou.node('/obj')
    merge_node = obj_node.createNode('geo', 'merged_geo')

    # Initialize a merge node under the geo node
    merge = merge_node.createNode('merge')

    # Iterate over selected nodes
    for i, node in enumerate(selected_nodes):
       
        object_merge = merge_node.createNode('object_merge', node.name())

        object_merge.parm('objpath1').set(node.path())
        object_merge.parm('xformtype').set(1)
    
        merge.setInput(i, object_merge)
        object_merge.moveToGoodPosition()

    merge.moveToGoodPosition()
    merge_node.layoutChildren()