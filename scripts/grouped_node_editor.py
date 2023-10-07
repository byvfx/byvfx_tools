from PySide2 import QtWidgets, QtGui

class GroupedNodeEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(GroupedNodeEditor, self).__init__(parent)

        self.setWindowTitle("Grouped Node Editor")
        self.layout = QtWidgets.QVBoxLayout(self)

        # Create the QTreeView
        self.tree = QtWidgets.QTreeView(self)
        self.layout.addWidget(self.tree)

        # Create the model
        self.model = QtGui.QStandardItemModel()
        self.tree.setModel(self.model)

        # For demonstration, let's use a dummy data model
        data_model = {
            'Group1': ['Node1', 'Node2'],
            'Group2': ['Node3']
        }

        for group, nodes in data_model.items():
            group_item = QtGui.QStandardItem(group)
            for node in nodes:
                node_item = QtGui.QStandardItem(node)
                group_item.appendRow(node_item)
            self.model.appendRow(group_item)

        self.tree.expandAll()  # This ensures all groups/nodes are visible when the editor is opened

app = QtWidgets.QApplication([])
window = GroupedNodeEditor()
window.show()
app.exec_()
