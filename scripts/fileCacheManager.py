
#TODO - add ability to remove from group
#TODO - add ability to delete group
#TODO - add drag and drop
#TODO - add ability to edit path in tree
#TODO - add ability to edit path in file browser
#TODO - add ability to cache from tree
#TODO - add ability to cache from groups

from PySide2 import QtWidgets, QtCore, QtGui
import hou
import json

def get_filecache_nodes():
    filecache_nodes = []
    for node in hou.node("/").allSubChildren():
        if node.type().name().startswith("filecache"):
            filecache_nodes.append(node)
    return filecache_nodes

def get_filemethod(node):
    return node.parm("filemethod").eval()

def change_group_color(self, item):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        item.setBackground(0, QtGui.QBrush(color))
        self.group_colors[item.text(0)] = color.name()
        self.save_groups_to_json()

class FileCacheNodeEditor(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(FileCacheNodeEditor, self).__init__(parent)
        self.setWindowTitle("File Cache Manager")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        

        self.layout = QtWidgets.QVBoxLayout(self)

        self.tree = QtWidgets.QTreeWidget(self)
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(['Node Name', 'Node Location', 'Path'])
        self.tree.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.layout.addWidget(self.tree)

        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        self.tree.header().setStretchLastSection(False)
        self.tree.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.load_groups_from_json()
        self.update_tree()
        
    def load_groups_from_json(self, json_file_path="groups_data.json"):
        try:
            with open(json_file_path, 'r') as file:
                self.data = json.load(file)
                self.data_model = self.data.get("nodes", {})
                self.group_colors = self.data.get("colors", {})
        except (FileNotFoundError, json.JSONDecodeError):
            self.data_model = {'Ungrouped': [node.path() for node in get_filecache_nodes()]}
            self.group_colors = {}



    def save_groups_to_json(self, json_file_path="groups_data.json"):
        with open(json_file_path, 'w') as file:
            json.dump({"nodes": self.data_model, "colors": self.group_colors}, file, indent=4)

    def adjust_sizes(self):
    # Adjusting column width for QTreeWidget
        for i in range(self.tree.columnCount()):
            self.tree.resizeColumnToContents(i)

        width_required = self.tree.header().length()
        for i in range(self.tree.columnCount()):
            width_required += self.tree.columnWidth(i)

        # Adding some additional width for a better look, you can adjust the value 50 to your liking
        self.resize(width_required + 500, self.height())
    
    def update_tree(self):
        self.tree.clear()
        for group, node_paths in self.data_model.items():
            parent_item = QtWidgets.QTreeWidgetItem(self.tree, [group])
            color = self.group_colors.get(group)
            if color:
                parent_item.setBackground(0, QtGui.QBrush(QtGui.QColor(color)))
            for node_path in node_paths:
                node = hou.node(node_path)
                if node:
                    QtWidgets.QTreeWidgetItem(parent_item, [node.name(), node.parent().path(), node.parm("file").eval()])
        self.adjust_sizes()
        self.tree.expandAll()



    def show_context_menu(self, position):
        print("Debug: Entered show_context_menu")

        global_position = self.tree.viewport().mapToGlobal(position)
        context_menu = QtWidgets.QMenu(self)
        
        selected_items = self.tree.selectedItems()
        if not selected_items:
            print("Debug: No tree item selected")
            return

        # Check if all selected items are group items (don't have a parent)
        all_group_items = all([item.parent() is None for item in selected_items])

        # Initialize the action variables
        focus_node_action = None
        create_group_action = None
        add_to_group_action = None
        rename_group_action = None
        change_group_color_action = None
        delete_group_action = None

        if all_group_items:
            print("Debug: Context menu for group items")
            change_group_color_action = context_menu.addAction("Change Group Color")
            create_group_action = context_menu.addAction("Create Group")
            rename_group_action = context_menu.addAction("Rename Group")
            delete_group_action = context_menu.addAction("Delete Group")
        else:
            print("Debug: Context menu for node items")
            focus_node_action = context_menu.addAction("Focus on Node(s)")
            add_to_group_action = context_menu.addAction("Add Selected to Group")

        action = context_menu.exec_(global_position)
        if action is None:
            print("Debug: No action selected")
            return
            
        print(f"Debug: Selected action: {action}")

        if action == focus_node_action:
            print("Debug: Executing focus_on_selected_node()")
            self.focus_on_selected_node()  # Make sure this method can handle multiple nodes
        elif action == change_group_color_action:
            print("Debug: Executing change_group_color()")
            # Decide how to handle color change for multiple groups
        elif action == create_group_action:
            print("Debug: Executing create_group()")
            self.create_group()
        elif action == add_to_group_action:
            print("Debug: Executing add_to_group()")
            self.add_to_group()  # Make sure this method can handle multiple nodes
        elif action == rename_group_action:
            print("Debug: Executing rename_group()")
            # Decide how to handle renaming for multiple groups
        elif action == delete_group_action:
            print("Debug: Executing delete_group()")
            self.delete_group()



    
    def add_to_group(self):
        # Get all selected tree items
        selected_items = self.tree.selectedItems()
        
        # Filter out items that are group items
        nodes_to_add = [item for item in selected_items if item.parent() is not None]
        
        if not nodes_to_add:
            # Display a message if no valid nodes are selected
            QtWidgets.QMessageBox.warning(self, "Warning", "No valid nodes selected to add to a group!")
            return
        
        # Get the paths of the nodes
        node_paths = [item.text(1) + "/" + item.text(0) for item in nodes_to_add]
        
        group_names = list(self.data_model.keys())
        selected_group, ok = QtWidgets.QInputDialog.getItem(self, "Add to Group", "Select Group:", group_names, 0, False)
        
        if ok and selected_group:
            for full_node_path in node_paths:
                # Remove from the source group (if it exists in any group)
                for group, paths in self.data_model.items():
                    if full_node_path in paths:
                        paths.remove(full_node_path)
                
                # Add to the selected group
                if full_node_path not in self.data_model[selected_group]:
                    self.data_model[selected_group].append(full_node_path)

            self.save_groups_to_json()  # Save after moving nodes
            self.update_tree()

    def delete_group(self):
        # Get all selected tree items
        selected_items = self.tree.selectedItems()
        
        # Filter out items that are not group items
        groups_to_delete = [item for item in selected_items if item.parent() is None]

        if not groups_to_delete:
            # Display a message if no valid groups are selected
            QtWidgets.QMessageBox.warning(self, "Warning", "No valid groups selected for deletion!")
            return

        for group_item in groups_to_delete:
            group_name = group_item.text(0)
            
            # Move nodes to "Ungrouped"
            if "Ungrouped" not in self.data_model:
                self.data_model["Ungrouped"] = []

            self.data_model["Ungrouped"].extend(self.data_model[group_name])

            # Delete the group from data model
            del self.data_model[group_name]
            
            # If the group has a color, remove it
            if group_name in self.group_colors:
                del self.group_colors[group_name]
        
        self.save_groups_to_json()  # Save after deleting groups
        self.update_tree()



    def focus_on_selected_node(self):
        item = self.tree.currentItem()
        if item and item.parent():  # Ensure it's a child item (a node, not a group)
            node_name = item.text(0)
            node_path = item.text(1)
            full_node_path = node_path + "/" + node_name
            node = hou.node(full_node_path)
            print(node)
            print(full_node_path)
            if node:
                # Select only the desired node
                node.setSelected(True, clear_all_selected=True)

                # Frame the selected node in the network editor
                for pane in hou.ui.paneTabs():
                    if isinstance(pane, hou.NetworkEditor):
                        pane.setPwd(node.parent())
                        pane.frameSelection()
                        pane.setZoom(2)

    def create_group(self):
        group_name, ok = QtWidgets.QInputDialog.getText(self, "Create Group", "Group Name:")
        if ok and group_name not in self.data_model:
            self.data_model[group_name] = []
            self.save_groups_to_json()  # Save after creating a group
            self.update_tree()
            self.load_groups_from_json()
            self.update_tree()


    def rename_group(self):
        items = list(self.data_model.keys())
        item, ok = QtWidgets.QInputDialog.getItem(self, "Rename Group", "Select Group to Rename:", items, 0, False)
        if ok and item:
            new_group_name, ok2 = QtWidgets.QInputDialog.getText(self, "Rename Group", "New Group Name:")
            if ok2 and new_group_name:
                self.data_model[new_group_name] = self.data_model.pop(item)
                if item in self.group_colors:
                    self.group_colors[new_group_name] = self.group_colors[item]
                
                    
            self.save_groups_to_json()  # Save after renaming a group
            self.update_tree()
            self.load_groups_from_json()
            self.update_tree()   

app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
window = FileCacheNodeEditor()
window.show()