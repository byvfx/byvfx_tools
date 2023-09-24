"""
author:     brandon young | http://www.byvfx.com  
about:      this script will split an alembic node into separate groups if they exist.

"""
import hou

# Get selected nodes
selected_nodes = hou.selectedNodes()

if not selected_nodes:
    hou.ui.displayMessage("No node is selected.")
else:
    for node in selected_nodes:
        # Check if selected node is Alembic SOP
        if node.type().name() == "alembic":
            # Get all group names in the Alembic node
            group_names = node.geometry().primGroups()

            if not group_names:
                hou.ui.displayMessage("No groups exist in the selected Alembic SOP node.")
            else:
                for group_name in group_names:
                    # Create blast node
                    blast_node = node.createOutputNode('blast')
                    blast_node.parm('group').set(group_name.name())
                    blast_node.parm('negate').set(True)

                    # Create null node
                    null_node = blast_node.createOutputNode('null')
                    null_node.setName('OUT_'+group_name.name())
        else:
            hou.ui.displayMessage("Selected node is not an Alembic SOP.")

