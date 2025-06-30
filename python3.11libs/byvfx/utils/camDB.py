from PySide2 import QtWidgets, QtCore
import hou
import urllib.request
import urllib.error
import json
import gzip
import traceback # Keep import here, use conditionally

# ┌──────────────────────────────────────────────────────────────────────────┐
# │ GLOBAL DEBUG FLAG                                                        │
# │ Set to True to enable debug prints, False to disable them.               │
# └──────────────────────────────────────────────────────────────────────────┘
DEBUG_MODE = False  # <-- TOGGLE DEBUGGING HERE

def debug_log(*args, **kwargs):
    """Prints messages only if DEBUG_MODE is True."""
    if DEBUG_MODE:
        print("DEBUG:", *args, **kwargs)

# Keep a module-level reference so Python doesn't garbage-collect the window
camdb_win = None

class CamDBPanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CamDBPanel, self).__init__(parent)
        self.setWindowTitle("CamDB Houdini Camera Browser")
        self.resize(800, 600)
        
        # Store camera data
        self.camera_data = []
        self.filtered_cameras = []
        self.selected_camera = None
        self.sensor_data = []
        
        # ─── Layout ─────────────────────────────────────────────────
        main_layout = QtWidgets.QVBoxLayout(self)
        
        # Top section: Load cameras button
        load_layout = QtWidgets.QHBoxLayout()
        self.load_all_button = QtWidgets.QPushButton("Load All Cameras from CamDB")
        self.load_all_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; }")
        load_layout.addWidget(self.load_all_button)
        
        self.status_label = QtWidgets.QLabel("Click 'Load All Cameras' to start")
        load_layout.addWidget(self.status_label)
        load_layout.addStretch()
        main_layout.addLayout(load_layout)
        
        # Filter section
        filter_layout = QtWidgets.QHBoxLayout()
        
        # Camera make dropdown
        make_layout = QtWidgets.QVBoxLayout()
        make_layout.addWidget(QtWidgets.QLabel("Filter by Make:"))
        self.make_combo = QtWidgets.QComboBox()
        self.make_combo.addItem("All Makes")
        make_layout.addWidget(self.make_combo)
        filter_layout.addLayout(make_layout)
        
        # Camera type dropdown
        type_layout = QtWidgets.QVBoxLayout()
        type_layout.addWidget(QtWidgets.QLabel("Filter by Type:"))
        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.addItem("All Types")
        type_layout.addWidget(self.type_combo)
        filter_layout.addLayout(type_layout)
        
        # Search box
        search_layout = QtWidgets.QVBoxLayout()
        search_layout.addWidget(QtWidgets.QLabel("Search Name:"))
        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setPlaceholderText("Search camera names...")
        search_layout.addWidget(self.search_edit)
        filter_layout.addLayout(search_layout)
        
        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)
        
        # Splitter for camera list and details
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left side: Camera list
        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.addWidget(QtWidgets.QLabel("Cameras:"))
        
        self.camera_list = QtWidgets.QListWidget()
        self.camera_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        left_layout.addWidget(self.camera_list)
        
        splitter.addWidget(left_widget)
        
        # Right side: Camera details and sensor info
        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        
        # Camera info section
        right_layout.addWidget(QtWidgets.QLabel("Camera Details:"))
        self.camera_info = QtWidgets.QTextEdit()
        self.camera_info.setMaximumHeight(100)
        self.camera_info.setReadOnly(True)
        right_layout.addWidget(self.camera_info)
        
        # Load sensors button
        self.load_sensors_button = QtWidgets.QPushButton("Load Sensor Data for Selected Camera")
        self.load_sensors_button.setEnabled(False)
        right_layout.addWidget(self.load_sensors_button)
        
        # Sensor data section
        right_layout.addWidget(QtWidgets.QLabel("Available Sensor Configurations:"))
        self.sensor_list = QtWidgets.QListWidget()
        right_layout.addWidget(self.sensor_list)
        
        # Sensor details
        right_layout.addWidget(QtWidgets.QLabel("Sensor Details:"))
        self.sensor_info = QtWidgets.QTextEdit()
        self.sensor_info.setMaximumHeight(150)
        self.sensor_info.setReadOnly(True)
        right_layout.addWidget(self.sensor_info)
        
        # Create camera button
        self.create_camera_button = QtWidgets.QPushButton("Create Camera in Houdini")
        self.create_camera_button.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; padding: 10px; }")
        self.create_camera_button.setEnabled(False)
        right_layout.addWidget(self.create_camera_button)
        
        splitter.addWidget(right_widget)
        splitter.setSizes([300, 500])
        
        # ─── Signals ────────────────────────────────────────────────
        self.load_all_button.clicked.connect(self.load_all_cameras)
        self.make_combo.currentTextChanged.connect(self.filter_cameras)
        self.type_combo.currentTextChanged.connect(self.filter_cameras)
        self.search_edit.textChanged.connect(self.filter_cameras)
        self.camera_list.currentItemChanged.connect(self.on_camera_selected)
        self.load_sensors_button.clicked.connect(self.load_sensor_data)
        self.sensor_list.currentItemChanged.connect(self.on_sensor_selected)
        self.create_camera_button.clicked.connect(self.create_houdini_camera)

    def api_request(self, endpoint):
        """Make API request with proper headers"""
        url = f"https://camdb.matchmovemachine.com{endpoint}"
        
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            req.add_header('Accept', 'application/json, text/plain, */*')
            req.add_header('Accept-Language', 'en-US,en;q=0.9')
            req.add_header('Connection', 'keep-alive')
            
            with urllib.request.urlopen(req) as response:
                raw_data = response.read()
                
                # Handle compression
                content_encoding = response.info().get('Content-Encoding', '').lower()
                if content_encoding == 'gzip':
                    raw_data = gzip.decompress(raw_data)
                elif content_encoding == 'deflate':
                    import zlib
                    raw_data = zlib.decompress(raw_data)
                
                encoding = response.info().get_content_charset("utf-8")
                text_data = raw_data.decode(encoding)
                return json.loads(text_data)
                
        except Exception as e:
            raise Exception(f"API request failed: {e}")

    def load_all_cameras(self):
        """Load all cameras from the API"""
        self.status_label.setText("Loading cameras...")
        self.load_all_button.setEnabled(False)
        
        try:
            # Load cameras
            data = self.api_request("/cameras/")
            self.camera_data = data if isinstance(data, list) else []
            
            # Populate filter dropdowns
            makes = set()
            types = set()
            
            for camera in self.camera_data:
                if camera.get('make'):
                    makes.add(camera['make'])
                if camera.get('cam_type'):
                    types.add(camera['cam_type'])
            
            # Update make combo
            self.make_combo.clear()
            self.make_combo.addItem("All Makes")
            for make in sorted(makes):
                self.make_combo.addItem(make)
            
            # Update type combo
            self.type_combo.clear()
            self.type_combo.addItem("All Types")
            for cam_type in sorted(types):
                self.type_combo.addItem(cam_type)
            
            # Filter and display cameras
            self.filter_cameras()
            
            self.status_label.setText(f"Loaded {len(self.camera_data)} cameras")
            
        except Exception as e:
            self.status_label.setText(f"Error loading cameras: {e}")
        
        finally:
            self.load_all_button.setEnabled(True)

    def filter_cameras(self):
        """Filter cameras based on selected criteria"""
        if not self.camera_data:
            return
        
        selected_make = self.make_combo.currentText()
        selected_type = self.type_combo.currentText()
        search_text = self.search_edit.text().lower()
        
        self.filtered_cameras = []
        
        for camera in self.camera_data:
            # Filter by make
            if selected_make != "All Makes" and camera.get('make') != selected_make:
                continue
            
            # Filter by type
            if selected_type != "All Types" and camera.get('cam_type') != selected_type:
                continue
            
            # Filter by search text
            if search_text and search_text not in camera.get('name', '').lower():
                continue
            
            self.filtered_cameras.append(camera)
        
        # Update camera list
        self.camera_list.clear()
        for camera in self.filtered_cameras:
            name = camera.get('name', 'Unknown')
            make = camera.get('make', 'Unknown')
            item_text = f"{make} - {name}"
            item = QtWidgets.QListWidgetItem(item_text)
            item.setData(QtCore.Qt.UserRole, camera)
            self.camera_list.addItem(item)

    def on_camera_selected(self, current, previous):
        """Handle camera selection"""
        if current:
            self.selected_camera = current.data(QtCore.Qt.UserRole)
            
            # Display camera info
            info = f"ID: {self.selected_camera.get('id', 'N/A')}\n"
            info += f"Make: {self.selected_camera.get('make', 'N/A')}\n"
            info += f"Name: {self.selected_camera.get('name', 'N/A')}\n"
            info += f"Type: {self.selected_camera.get('cam_type', 'N/A')}"
            
            self.camera_info.setPlainText(info)
            self.load_sensors_button.setEnabled(True)
            
            # Clear sensor data
            self.sensor_list.clear()
            self.sensor_info.clear()
            self.create_camera_button.setEnabled(False)
        else:
            self.selected_camera = None
            self.camera_info.clear()
            self.load_sensors_button.setEnabled(False)

    def load_sensor_data(self):
        """Load sensor data for the selected camera"""
        if not self.selected_camera:
            return
        
        camera_id = self.selected_camera.get('id')
        if not camera_id:
            return
        
        self.status_label.setText("Loading sensor data...")
        self.load_sensors_button.setEnabled(False)

        try:
            endpoint = f"/cameras/{camera_id}/sensors/"
            debug_log(f"Requesting: {endpoint}")
            
            data = self.api_request(endpoint)
            
            debug_log(f"Raw sensor response: {data}")
            
            # Handle different response formats
            if isinstance(data, dict):
                if 'sensors' in data:
                    self.sensor_data = data['sensors']
                elif 'data' in data:
                    self.sensor_data = data['data']
                elif 'results' in data:
                    self.sensor_data = data['results']
                else:
                    self.sensor_data = [data] # Might be a single sensor object
            elif isinstance(data, list):
                self.sensor_data = data
            else:
                self.sensor_data = []
            
            debug_log(f"Processed sensor data: {self.sensor_data}")
            
            self.sensor_list.clear()
            
            if not self.sensor_data:
                item = QtWidgets.QListWidgetItem("No sensor data available")
                self.sensor_list.addItem(item)
                self.status_label.setText("No sensor configurations found")
                return
            
            for i, sensor in enumerate(self.sensor_data):
                debug_log(f"Processing sensor {i}: {sensor}")
                
                mode = sensor.get('mode_name', f'Mode {i+1}')
                res_w = sensor.get('res_width', 'N/A')
                res_h = sensor.get('res_height', 'N/A')
                sensor_w = sensor.get('sensor_width', 'N/A')
                sensor_h = sensor.get('sensor_height', 'N/A')
                
                res = f"{res_w}x{res_h}"
                sensor_size = f"{sensor_w}x{sensor_h}mm"
                
                item_text = f"{mode} - {res} ({sensor_size})"
                item = QtWidgets.QListWidgetItem(item_text)
                item.setData(QtCore.Qt.UserRole, sensor)
                self.sensor_list.addItem(item)
            
            self.status_label.setText(f"Loaded {len(self.sensor_data)} sensor configurations")
            
        except urllib.error.HTTPError as http_err:
            error_msg = f"HTTP {http_err.code}: {http_err.reason}"
            try:
                error_body = http_err.read().decode('utf-8')
                error_msg += f"\nResponse: {error_body}"
            except:
                pass # Ignore if reading body fails
            self.status_label.setText(f"HTTP Error: {error_msg.splitlines()[0]}") # Show first line in status
            debug_log(f"HTTP Error loading sensors: {error_msg}")
            
        except Exception as e:
            self.status_label.setText(f"Error loading sensors: {e}")
            debug_log(f"Error loading sensors: {e}")
            if DEBUG_MODE:
                traceback.print_exc()
        
        finally:
            self.load_sensors_button.setEnabled(True)

    def on_sensor_selected(self, current, previous):
        """Handle sensor selection"""
        if current:
            sensor = current.data(QtCore.Qt.UserRole)
            if not isinstance(sensor, dict): # Guard against "No sensor data" item
                self.sensor_info.clear()
                self.create_camera_button.setEnabled(False)
                return

            # Display sensor info
            info = f"Sensor ID: {sensor.get('id', 'N/A')}\n"
            info += f"Mode: {sensor.get('mode_name', 'N/A')}\n"
            info += f"Resolution: {sensor.get('res_width', 'N/A')} x {sensor.get('res_height', 'N/A')}\n"
            info += f"Sensor Size: {sensor.get('sensor_width', 'N/A')} x {sensor.get('sensor_height', 'N/A')} mm\n"
            info += f"Format Aspect: {sensor.get('format_aspect', 'N/A')}\n"
            info += f"Approved: {sensor.get('approve', 'N/A')}"
            
            self.sensor_info.setPlainText(info)
            self.create_camera_button.setEnabled(True)
        else:
            self.sensor_info.clear()
            self.create_camera_button.setEnabled(False)

    def create_houdini_camera(self):
        """Create a camera in Houdini with the selected settings"""
        if not self.selected_camera:
            hou.ui.displayMessage("No camera selected")
            return
        
        current_sensor_item = self.sensor_list.currentItem()
        if not current_sensor_item:
            hou.ui.displayMessage("No sensor configuration selected")
            return
        
        sensor = current_sensor_item.data(QtCore.Qt.UserRole)
        if not isinstance(sensor, dict): # Ensure it's actual sensor data
            hou.ui.displayMessage("Invalid sensor data selected.")
            return
        
        try:
            obj = hou.node("/obj")
            
            camera_make = self.selected_camera.get('make', 'UnknownCam')
            camera_model_name = self.selected_camera.get('name', 'Model')
            
            # Sanitize names for Houdini nodes
            sane_make = "".join(c if c.isalnum() else "_" for c in camera_make)
            sane_model = "".join(c if c.isalnum() else "_" for c in camera_model_name)
            
            camera_name = f"{sane_make}_{sane_model}"
            
            cam_node = obj.createNode("cam", camera_name)
            
            res_w = sensor.get('res_width')
            res_h = sensor.get('res_height')
            sensor_w_mm = sensor.get('sensor_width')
            format_aspect = sensor.get('format_aspect')

            if res_w and res_h:
                try:
                    cam_node.parm("resx").set(int(res_w))
                    cam_node.parm("resy").set(int(res_h))
                except (ValueError, TypeError) as e:
                    debug_log(f"Could not set resolution {res_w}x{res_h}: {e}")


            if sensor_w_mm:
                try:
                    aperture_inches = float(sensor_w_mm) / 25.4
                    cam_node.parm("aperture").set(aperture_inches)
                except (ValueError, TypeError) as e:
                    debug_log(f"Could not set aperture {sensor_w_mm}mm: {e}")
            
            if format_aspect:
                try:
                    aspect = float(format_aspect)
                    cam_node.parm("aspect").set(aspect)
                except (ValueError, TypeError) as e:
                    debug_log(f"Could not set aspect ratio {format_aspect}: {e}")
            
            comment = f"CamDB Camera: {self.selected_camera.get('make')} {self.selected_camera.get('name')}\n"
            comment += f"Mode: {sensor.get('mode_name', 'N/A')}\n"
            comment += f"Sensor: {sensor.get('sensor_width','N/A')}x{sensor.get('sensor_height','N/A')}mm\n"
            comment += f"Resolution: {res_w or 'N/A'}x{res_h or 'N/A'}"
            
            cam_node.setComment(comment)
            cam_node.setGenericFlag(hou.nodeFlag.DisplayComment, True)
            
            cam_node.parmTuple("t").set((0, 0, 5))
            cam_node.moveToGoodPosition()
            
            self.status_label.setText(f"Created camera: {cam_node.name()}")
            
            if hou.ui.displayMessage(f"Camera '{cam_node.name()}' created. Look through it?", 
                                   buttons=("Yes", "No")) == 0:
                scene_viewer = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
                if scene_viewer:
                    viewport = scene_viewer.curViewport()
                    if viewport:
                        viewport.setCamera(cam_node)
            
        except Exception as e:
            hou.ui.displayMessage(f"Error creating camera: {e}")
            self.status_label.setText(f"Error creating camera: {e}")
            debug_log(f"Full error creating camera: {e}")
            if DEBUG_MODE:
                traceback.print_exc()

def show_camdb_floating():
    global camdb_win
    
    if camdb_win:
        if camdb_win.isVisible():
            camdb_win.raise_()
            camdb_win.activateWindow()
            return
        else:
            # Window exists but is hidden, show it
            try:
                camdb_win.show()
                camdb_win.raise_()
                camdb_win.activateWindow()
                return
            except RuntimeError: # Window might have been closed/deleted
                camdb_win = None # Reset so it gets recreated

    if camdb_win is None: # Create anew if not existing or recreated
        parent = hou.ui.mainQtWindow()
        camdb_win = CamDBPanel(parent)
        camdb_win.setWindowFlags(QtCore.Qt.Window) # Make it a floating window
        camdb_win.show()

# Execute immediately when the shelf tool is clicked
show_camdb_floating()