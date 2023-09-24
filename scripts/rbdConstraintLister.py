import hou
from PySide2 import QtWidgets, QtGui, QtCore

class HoudiniParamViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(HoudiniParamViewer, self).__init__(parent)
        
        # Layouts
        self.layout = QtWidgets.QVBoxLayout(self)
        self.node_combo_layout = QtWidgets.QHBoxLayout()
        self.params_list_layout = QtWidgets.QVBoxLayout()
        self.param_value_layout = QtWidgets.QHBoxLayout()

        # Widgets
        self.node_combo = QtWidgets.QComboBox(self)
        self.params_list = QtWidgets.QListWidget(self)
        self.param_label = QtWidgets.QLabel("Parameter Value:")
        self.param_value = QtWidgets.QLabel()

        # Populate node combo box with geo type nodes
        self.populate_nodes_of_type('geo')
        
        # Connect signals
        self.node_combo.currentIndexChanged.connect(self.populate_params)
        self.params_list.currentItemChanged.connect(self.display_param_value)

        # Add widgets to layouts
        self.node_combo_layout.addWidget(QtWidgets.QLabel("Node:"))
        self.node_combo_layout.addWidget(self.node_combo)
        
        self.params_list_layout.addWidget(QtWidgets.QLabel("Parameters:"))
        self.params_list_layout.addWidget(self.params_list)
        
        self.param_value_layout.addWidget(self.param_label)
        self.param_value_layout.addWidget(self.param_value)
        
        self.layout.addLayout(self.node_combo_layout)
        self.layout.addLayout(self.params_list_layout)
        self.layout.addLayout(self.param_value_layout)

    def populate_nodes_of_type(self, node_type):
        nodes = [node for node in hou.node('/obj').children() if node.type().name() == node_type]
        for node in nodes:
            self.node_combo.addItem(node.name(), node)
            
    def populate_params(self):
        self.params_list.clear()
        node = self.node_combo.currentData()
        if node:
            for param in node.parms():
                item = QtWidgets.QListWidgetItem(param.name())
                item.setData(QtCore.Qt.UserRole, param)
                self.params_list.addItem(item)
                
    def display_param_value(self, current, previous):
        param = current.data(QtCore.Qt.UserRole)
        if param:
            self.param_value.setText(str(param.eval()))

# Show the UI
app = QtWidgets.QApplication.instance()
if not app:
    app = QtWidgets.QApplication([])

viewer = HoudiniParamViewer()
viewer.show()
