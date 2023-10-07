#TODO - add grouping for nodes and  collaspable groups and color coding for grou

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

        self.layout = QtWidgets.QVBoxLayout(self)

        self.tree = QtWidgets.QTreeWidget(self)
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(['Node Name', 'Node Location', 'Path'])
        #self.tree.doubleClicked.connect(self.edit_path_in_tree)
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
        
        width_required = self.tree.verticalScrollBar().width()
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
        global_position = self.tree.viewport().mapToGlobal(position)
        context_menu = QtWidgets.QMenu(self)
        
        item = self.tree.currentItem()
        if item is None:
            # Handle the case where no item is selected or other unusual states
            return

        # Initialize the action variables
        focus_node_action = None
        create_group_action = None
        add_to_group_action = None
        rename_group_action = None
        change_group_color_action = None

        if item.parent() is None:  # Ensures we're on a group item
            change_group_color_action = context_menu.addAction("Change Group Color")
            create_group_action = context_menu.addAction("Create Group")
            rename_group_action = context_menu.addAction("Rename Group")
        else:
            focus_node_action = context_menu.addAction("Focus on Node")
            add_to_group_action = context_menu.addAction("Add to Group")

        action = context_menu.exec_(global_position)

        if action == focus_node_action:
            self.focus_on_selected_node()
        elif action == change_group_color_action:
            change_group_color(self, item)
        elif action == create_group_action:
            self.create_group()
        elif action == add_to_group_action:
            self.add_to_group()
        elif action == rename_group_action:
            self.rename_group()

    
    def add_to_group(self):
        item = self.tree.currentItem()  # Get the selected tree item
        if item and item.parent():  # Ensure it's not a group item
            node_name = item.text(0)
            node_path = item.text(1)
            full_node_path = node_path + "/" + node_name
            group_names = list(self.data_model.keys())
            selected_group, ok = QtWidgets.QInputDialog.getItem(self, "Add to Group", "Select Group:", group_names, 0, False)
            self.load_groups_from_json()
            self.update_tree()
            
            if ok and selected_group:
                if full_node_path not in self.data_model[selected_group]:
                    self.data_model[selected_group].append(full_node_path)
                    self.save_groups_to_json()  # Save after adding to a group
                    self.update_tree()

    def focus_on_selected_node(self):
        item = self.tree.currentItem()
        if item and item.parent():
            full_node_path = item.text(2)
            node = hou.node(full_node_path)
            if node:
                # Deselect all nodes at the node's parent level
                for sibling in node.parent().children():
                    sibling.setSelected(False)
                
                # Now, select only the desired node
                node.setSelected(True)

                for pane in hou.ui.paneTabs():
                    if isinstance(pane, hou.NetworkEditor):
                        pane.setPwd(node.parent())
                        pane.frameSelection()

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
                self.save_groups_to_json()  # Save after renaming a group
                self.update_tree()
                self.load_groups_from_json()
                self.update_tree()


app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
window = FileCacheNodeEditor()
window.show()