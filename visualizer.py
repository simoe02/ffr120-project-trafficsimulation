import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters as exporters
from pyqtgraph.Qt import QtWidgets, QtCore

from simulation import TrafficSimulation

# For light theme
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

QtWidgets.QApplication.setAttribute(
    QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True
)
QtWidgets.QApplication.setAttribute(
    QtCore.Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True
)

class TrafficVisualizer:
    """
    Class for visualizing the simulation using GPU-accelerated graphics with pyqtgraph. 
    """
    def __init__(self, simulation: TrafficSimulation, dt: float) -> None:
        self.simulation = simulation
        self.dt = dt
        
        vehicle_x = []
        vehicle_y = []
        for vehicle in self.simulation.vehicles:
            x, y = vehicle.current_road.start.x, vehicle.current_road.start.y
            vehicle_x.append(x)
            vehicle_y.append(y)
        self.vehicle_positions = np.column_stack([vehicle_x, vehicle_y])

        self.app = QtWidgets.QApplication([])
        self.win = pg.GraphicsLayoutWidget(show=True, title="Traffic Visualizer", size=(1000, 1000))

        self.view = pg.ViewBox()
        self.win.addItem(self.view)
        self.view.setAspectLocked(True)

        self.road_item = pg.GraphItem()
        self.view.addItem(self.road_item)
        self.render_roads()

        self.agent_item = pg.ScatterPlotItem(size=4, brush=pg.mkBrush("red"))
        self.view.addItem(self.agent_item)

        # Timer for animation
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16) # 60 FPS
        
        self.exporter = exporters.ImageExporter(self.win.scene())
        self.exporter.parameters()['width'] = 4000
        self.n = 0

    def render_roads(self) -> None:
        xs = []
        ys = []
        adj = []
        idx = 0

        for road in self.simulation.network.roads:
            
            x1, y1 = road.start.x, road.start.y
            x2, y2 = road.end.x, road.end.y

            xs += [x1, x2]
            ys += [y1, y2]

            adj.append((idx, idx + 1))
            idx += 2

        pos = np.column_stack([xs, ys])
        adj = np.array(adj, dtype=np.int32)

        self.road_item.setData(
            pos=pos,
            adj=adj,
            pen=pg.mkPen('k', width=2, alpha=0.8),
            size=1,
            symbol=None,
            pxMode=False
        )

    def update(self) -> None:
        self.simulation.step(self.dt)
        self.n += 1
        
        if self.n == 600:
            self.exporter.export("traffic_simulation.png")
        
        vehicle_x = []
        vehicle_y = []
        for vehicle in self.simulation.vehicles:
            vehicle_x.append(vehicle.x)
            vehicle_y.append(vehicle.y)
        vehicle_positions = np.column_stack([vehicle_x, vehicle_y])

        self.agent_item.setData(
            vehicle_positions[:, 0],
            vehicle_positions[:, 1]
        )

        QtWidgets.QApplication.processEvents()

    def run(self) -> None:
        self.app.exec()

