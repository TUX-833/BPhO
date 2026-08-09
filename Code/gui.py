from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QSizePolicy, QSlider, QCheckBox, QMainWindow, QPushButton, QComboBox, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QButtonGroup
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from noGraph import NoGraph
from task1 import Task1Walk
from task2 import Task2Simulator
from task3 import Task3Grapher
from task4 import Task4Grapher
from task5 import Task5Grapher
from task6 import Task6Simulator
from task7 import Task7Grapher
from task8 import Task8Diagramer
from task9 import Task9Grapher
from task10 import Task10Grapher

X = 1600
Y = 950

mainBgCol = "#0D1117"
midCol = "#2F81F7"
graphCol = "#21262D"

plt.rcParams['figure.facecolor'] = graphCol
plt.rcParams['axes.facecolor'] = graphCol

plt.rcParams['grid.color'] = '#666A6D'
plt.rcParams['axes.edgecolor'] = '#E6EDF3'
plt.rcParams['text.color'] = '#E6EDF3'
plt.rcParams['axes.labelcolor'] = '#E6EDF3'
plt.rcParams['ytick.color'] = '#E6EDF3'
plt.rcParams['xtick.color'] = '#E6EDF3'



class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quanta")
        self.setFixedSize(X, Y)

        self.setStyleSheet("""
            QWidget{
                background-color: #0D1117;
                border-radius: 8px;
            }
                           
            QPushButton {
                color: #E6EDF3;
                padding: 20px;
                border-radius: 8px;
            }

            QPushButton:checked {
                border: 2px solid #2F81F7;
            }
                           
            QPushButton:hover {
                background-color: #58A6FF;
                border: 2px solid #58A6FF;
            }           
            
            QLabel {
                color: #E6EDF3;
            }
                           
            QComboBox {
                background-color: #2F81F7;
                color: #E6EDF3;
                border: 2px solid #666A6D;
            }              
            QComboBox::drop-down {
                border: 0px;
                width: 0px;
            }
            QComboBox::down-arrow {
                image: none;
            }
            QComboBox QAbstractItemView {
                color: #E6EDF3;
                background-color: #E6EDF3;
                selection-background-color: #2F81F7;
            }
                           
            QLineEdit {
                border: 1px solid #666A6D;
                color: #E6EDF3;  
            }
                    
            QSlider::groove:horizontal {
                background: #666A6D;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: #2F81F7;  
                border-radius: 4px;
            }
            QSlider::add-page:horizontal {
                background: #666A6D;     
            }
            QSlider::handle:horizontal {
                background: #E6EDF3;
                width: 15px;
                margin: -5px 0;
                border-radius: 7px;
            }
                           
            QCheckBox {
                color: #E6EDF3;
            }
            """)

        self.workFuncs = [("Silver", 4.3), ("Aluminium", 4.3), ("Gold", 5.1), ("Copper", 4.7), 
                          ("Tin", 4.4), ("Lead", 4.3), ("Tungsten", 4.5), ("Nickel", 4.6), ("Sodium", 2.4)]
        self.workFunc = 4.3

        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)

        self.pageLayout = QHBoxLayout()
        self.buttonLayout = QVBoxLayout()

        buttonGroup = QButtonGroup()
        buttonGroup.setExclusive(True)

        container = QWidget()
        container.setLayout(self.pageLayout)
        self.setCentralWidget(container)
        container.setStyleSheet(f""" 
            background-color: {mainBgCol};
        """)

        self.buttonWidget = QWidget()
        self.buttonWidget.setLayout(self.buttonLayout)
        self.buttonWidget.setFixedWidth(int(X/8))
        self.pageLayout.addWidget(self.buttonWidget, 0)
        self.buttons = []

        label = QLabel("Select Task")
        label.setMaximumHeight(int(Y/20))
        label.setFixedWidth(int(X/8))
        label.setAutoFillBackground(True)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setObjectName("label")
        label.setFont(font)
        self.buttonLayout.addWidget(label)

        tasks = [["Random Walk", self.task1Inputs], ["Brownian Motion 3D Sim", self.task2Simulation], ["Black Body Radiation", self.task3Graph], 
                 ["Photo Electric Effect", self.task4Inputs], ["Hydrogen Spectra", self.task5Graph], ["Electron Diffraction", self.task6Simulation], 
                 ["Waves and uncertainty", self.task7Graph], ["QM Measurements", self.task8Gui], ["Compton Scattering", self.task9Inputs], 
                 ["Hydrogenic Orbitals", self.task10Inputs]]

        for task in tasks:
            btn = QPushButton(task[0])
            self.buttons.append(btn)
            btn.clicked.connect(task[1])
            self.buttonLayout.addWidget(btn)

        for btn in self.buttons:
            btn.setCheckable(True)
            buttonGroup.addButton(btn)

        self.canvas = QWidget()
        self._replace_canvas(NoGraph)

    def _create_input_layout(self, divisor:int = 1.2):
        self.pageLayout.removeWidget(self.canvas)
        self.canvas.deleteLater()
        self.canvas = QWidget()
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pageLayout.addWidget(self.canvas, 1)

        self.horiLayout = QHBoxLayout()
        self.inputHoldLayout = QVBoxLayout()
        self.inputLayout = QVBoxLayout()

        inputHoldWidget = QWidget()
        inputHoldWidget.setLayout(self.inputHoldLayout)
        inputHoldWidget.setStyleSheet(f"background-color: {graphCol};")
        inputHoldWidget.setFixedHeight(int(Y/1.2))
        inputHoldWidget.setFixedWidth(int(X/8))
        self.horiLayout.addWidget(inputHoldWidget, 0)

        inputWidget = QWidget()
        inputWidget.setLayout(self.inputLayout)
        inputWidget.setFixedHeight(int(Y/divisor))
        inputWidget.setFixedWidth(int(X/8))
        self.inputHoldLayout.addWidget(inputWidget, 0)

        self.canvas.setLayout(self.horiLayout)
    
    def _replace_canvas(self, GrapherClass:type = None):
        self.pageLayout.removeWidget(self.canvas)
        self.canvas.deleteLater()
        self.canvas = QWidget()
        self.canvas.setStyleSheet("background-color: #21262D;")
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pageLayout.addWidget(self.canvas, 1)

        containerLayout = QVBoxLayout()
        
        graphMaker = GrapherClass()
        container = FigureCanvas(graphMaker.getGraph())
        containerLayout.addWidget(container)

        self.canvas.setLayout(containerLayout)

    def _checking(self, btn):
        for b in self.buttons:
            b.setChecked(b == btn)


    def task1Inputs(self):
        btn = self.sender()
        self._checking(btn)

        self._create_input_layout(6)

        self.steps = 1000
        self.stepsLabel = QLabel(f"Steps: {self.steps}")
        self.inputLayout.addWidget(self.stepsLabel)
        stepsSlider = QSlider(QtCore.Qt.Orientation.Horizontal)
        stepsSlider.setFixedWidth(int(X/10))
        stepsSlider.setMinimum(1); stepsSlider.setMaximum(1000)
        stepsSlider.setTickInterval(100); stepsSlider.setValue(self.steps)
        stepsSlider.valueChanged.connect(self.stepSliderAction)
        self.inputLayout.addWidget(stepsSlider, alignment=QtCore.Qt.AlignCenter)

        self.lines = 50
        self.linesLabel = QLabel(f"Rabdom Walks: {self.lines}")
        self.inputLayout.addWidget(self.linesLabel)
        linesSlider = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        linesSlider.setFixedWidth(int(X/10))
        linesSlider.setMinimum(1); linesSlider.setMaximum(50); linesSlider.setValue(self.steps)
        linesSlider.valueChanged.connect(self.lineSliderAction)
        self.inputLayout.addWidget(linesSlider, alignment=QtCore.Qt.AlignCenter)

        self.canvas1 = FigureCanvas(NoGraph().getGraph())

        self.task1OpenGraph()
        

    def task1OpenGraph(self):
        self.pageLayout.removeWidget(self.canvas1)
        self.canvas1.deleteLater()
        self.canvas1 = QWidget()
        self.canvas1.setStyleSheet("background-color: #21262D;")
        self.horiLayout.addWidget(self.canvas1)

        containerLayout = QVBoxLayout()
        
        graphMaker = Task1Walk(self.lines, self.steps)        
        container = FigureCanvas(graphMaker.getGraph())
        containerLayout.addWidget(container)

        self.canvas1.setLayout(containerLayout)

    def lineSliderAction(self, value):
        self.lines = value
        self.linesLabel.setText(f"Random Walks: {self.lines}")
        self.task1OpenGraph()
    
    def stepSliderAction(self, value):
        self.steps = value
        self.stepsLabel.setText(f"Steps: {self.steps}")
        self.task1OpenGraph()


    def task2Simulation(self):
        btn = self.sender()
        self._checking(btn)

        self._replace_canvas(NoGraph)
        sim = Task2Simulator()
        sim.simulate()


    def task3Graph(self):
        btn = self.sender()
        self._checking(btn)

        self._replace_canvas(Task3Grapher)


    def task4Inputs(self):
        btn = self.sender()
        self._checking(btn)

        self._create_input_layout(9)

        font = QtGui.QFont()
        font.setPointSize(12)

        label = QLabel("Metal:", font = font)
        self.inputLayout.addWidget(label)

        combobox = QComboBox()
        combobox.setFixedWidth(int(X/10))
        self.inputLayout.addWidget(combobox, alignment=QtCore.Qt.AlignCenter)
        combobox.addItems([x[0] for x in self.workFuncs])
        combobox.setFont(font)
        combobox.currentIndexChanged.connect(self.dropDownState)

        self.canvas4 = FigureCanvas(NoGraph().getGraph())

        self.task4OpenGraph()

        self.canvas.setLayout(self.horiLayout)

    def task4OpenGraph(self): 
        self.pageLayout.removeWidget(self.canvas4)
        self.canvas4.deleteLater()
        self.canvas4 = QWidget()
        self.canvas4.setStyleSheet("background-color: #21262D;")
        self.horiLayout.addWidget(self.canvas4)

        containerLayout = QVBoxLayout()
        
        graphMaker = Task4Grapher(self.workFunc)        
        container = FigureCanvas(graphMaker.getGraph())
        containerLayout.addWidget(container)

        self.canvas4.setLayout(containerLayout)

    def dropDownState(self, index):
        self.workFunc = self.workFuncs[index][1]
        self.task4OpenGraph()


    def task5Graph(self):
        btn = self.sender()
        self._checking(btn)

        self._replace_canvas(Task5Grapher)


    def task6Simulation(self):
        btn = self.sender()
        self._checking(btn)

        self._replace_canvas(NoGraph)
        sim = Task6Simulator()
        sim.simulate()
        self._replace_canvas(Task6Simulator)


    def task7Graph(self):
        btn = self.sender()
        self._checking(btn)

        self._replace_canvas(Task7Grapher)


    def task8Gui(self):
        btn = self.sender()
        self._checking(btn)

        font = QtGui.QFont()
        font.setPointSize(15)

        self.pageLayout.removeWidget(self.canvas)
        self.canvas.deleteLater()
        self.canvas = QWidget()
        self.canvas.setStyleSheet(f"background-color: {graphCol}")
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pageLayout.addWidget(self.canvas, 1)

        self.inputLayout = QVBoxLayout()

        self.diagramLayout = QHBoxLayout()
        self.diagramHolder = QWidget()
        self.inputLayout.addWidget(self.diagramHolder)
        self.diagramHolder.setLayout(self.diagramLayout)
        self.canvas.setLayout(self.inputLayout)

        self.theta = -30
        self.phi = 30
        self.canvas8 = FigureCanvas(NoGraph().getGraph())
        self.diagramLayout.addWidget(self.canvas8)

        self.horiLayout = QHBoxLayout()
        sliderHolder = QWidget()
        self.inputLayout.addWidget(sliderHolder)
        sliderHolder.setLayout(self.horiLayout)
        
        thetaHolder =QWidget()
        thetaHolder.setFixedHeight(int(Y/8))
        self.horiLayout.addWidget(thetaHolder)
        thetaLayout = QVBoxLayout()
        thetaHolder.setLayout(thetaLayout)

        self.thetaLabel = QLabel(f"θ: {self.theta}", font = font)
        thetaLayout.addWidget(self.thetaLabel)
        thetaSlider = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        thetaSlider.setFixedWidth(int(X/3))
        thetaSlider.setMinimum(-90); thetaSlider.setMaximum(90); thetaSlider.setValue(self.theta)
        thetaSlider.valueChanged.connect(self.thetaSliderAction)
        thetaLayout.addWidget(thetaSlider)

        phiHolder =QWidget()
        phiHolder.setFixedHeight(int(Y/8))
        self.horiLayout.addWidget(phiHolder)
        phiLayout = QVBoxLayout()
        phiHolder.setLayout(phiLayout)

        self.phiLabel = QLabel(f"ϕ: {self.phi}", font = font)
        phiLayout.addWidget(self.phiLabel)
        phiSlider = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        phiSlider.setFixedWidth(int(X/3))
        phiSlider.setMinimum(-90); phiSlider.setMaximum(90); phiSlider.setValue(self.phi)
        phiSlider.valueChanged.connect(self.phiSliderAction)
        phiLayout.addWidget(phiSlider)

        self.classicProb = 0
        self.classicalLabel = QLabel("", font = font)
        self.inputLayout.addWidget(self.classicalLabel, alignment=QtCore.Qt.AlignCenter)

        self.QMProb = 0
        self.QMLabel = QLabel("", font = font)
        self.inputLayout.addWidget(self.QMLabel, alignment=QtCore.Qt.AlignCenter)

        self.task8OpenDiagram()
        
    def thetaSliderAction(self, value):
        self.theta = value
        self.thetaLabel.setText(f"θ: {self.theta}")
        self.task8OpenDiagram()

    def phiSliderAction(self, value):
        self.phi = value
        self.phiLabel.setText(f"ϕ: {self.phi}")
        self.task8OpenDiagram()

    def calculateProbs(self):
        diagramMaker = Task8Diagramer(self.theta, self.phi)
        self.classicProb, self.QMProb = diagramMaker.calculateProbs()
        self.classicalLabel.setText(f"Classical P(mismatch) = {round(self.classicProb, 3)}")
        self.QMLabel.setText(f"Quantum Mechanics P(mismatch) = {round(self.QMProb, 3)}")

    def task8OpenDiagram(self):
        self.diagramLayout.removeWidget(self.canvas8)
        self.canvas8.deleteLater()

        diagramMaker = Task8Diagramer(self.theta, self.phi)
        self.canvas8 = FigureCanvas(diagramMaker.getDiagram())
        self.diagramLayout.addWidget(self.canvas8)
        self.calculateProbs()

    def task9Inputs(self):
        btn = self.sender()
        self._checking(btn)

        self._create_input_layout(4)

        defaultEnergy = 662
        self.energyLabel = QLabel(f"Energy: {defaultEnergy} keV")
        
        self.energySlider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.energySlider.setRange(1, 1500)
        self.energySlider.setValue(defaultEnergy)
        self.energySlider.valueChanged.connect(self.task9SliderChange)
        
        self.lockAxes = QCheckBox(text="Lock Axes")
        self.probability = QCheckBox(text="show probabilties")

        self.lockAxes.clicked.connect(self.task9OpenGraph)
        self.probability.clicked.connect(self.task9OpenGraph)

        self.inputLayout.addWidget(self.energyLabel)
        self.inputLayout.addWidget(self.energySlider, alignment=QtCore.Qt.AlignCenter) 
        self.inputLayout.addWidget(self.lockAxes) 
        self.inputLayout.addWidget(self.probability)

        self.canvas9 = QWidget()
        self.canvas9.setStyleSheet("background-color: #21262D;")
        self.horiLayout.addWidget(self.canvas9)

        containerLayout = QVBoxLayout()
        self.canvas9.setLayout(containerLayout)

        graphMaker = NoGraph()
        container = FigureCanvas(graphMaker.getGraph())
        containerLayout.addWidget(container)
 
        self.canvas.setLayout(self.horiLayout)

        self.task9OpenGraph()


    def task9SliderChange(self):
        self.energyLabel.setText(f"Energy: {self.energySlider.value()} keV")
        self.task9OpenGraph()

    def task9OpenGraph(self):
        self.horiLayout.removeWidget(self.canvas9)
        self.canvas9.deleteLater()
        self.canvas9 = QWidget()
        self.canvas9.setStyleSheet("background-color: #21262D;")
        self.horiLayout.addWidget(self.canvas9)

        containerLayout = QVBoxLayout()
        self.canvas9.setLayout(containerLayout)

        graphMaker = Task9Grapher(self.energySlider.value(), probs=self.probability.isChecked(), lock=self.lockAxes.isChecked())
        container = FigureCanvas(graphMaker.getGraph())
        containerLayout.addWidget(container)


    def task10Inputs(self):
        btn = self.sender()
        self._checking(btn)

        self._create_input_layout()

        self.inputLayout.addWidget(QLabel(f"Enter wanted orbital:"))
        self.text_input = QLineEdit()
        self.text_input.setFixedWidth(int(X/10))
        self.text_input.setPlaceholderText("Enter orbital, eg. '1S'")
        self.inputLayout.addWidget(self.text_input, alignment=QtCore.Qt.AlignCenter)

        self.inputLayout.addSpacing(10)  

        self.slidersUse = [("M value", -4, 4, 0), ("A value", 1, 12, 1), 
                           ("Z value", 1, 12, 1), ("resolution", 1, 200, 40), ("graph size", 1, 40, 10)]
        self.sliders = []
        self.slidersLabel = []
        for use in self.slidersUse:
            slider = QSlider(QtCore.Qt.Orientation.Horizontal)
            slider.setFixedWidth(int(X/10))
            slider.setRange(use[1], use[2]); slider.setValue(use[3])
            slider.valueChanged.connect(self.task10SliderUpdate)
            label = QLabel(f"{use[0]}: {use[3]}")
            self.slidersLabel.append(label)
            self.inputLayout.addWidget(label)
            self.inputLayout.addWidget(slider, alignment=QtCore.Qt.AlignCenter)
            self.sliders.append(slider)
            self.inputLayout.addSpacing(10)  

        self.radialButton = QPushButton("Open radial graph")
        self.graphButton = QPushButton("Open z = 0 graph")
        self.graph3dButton = QPushButton("Open 3d graph")

        self.inputLayout.addWidget(self.radialButton)
        self.inputLayout.addWidget(self.graphButton)
        self.inputLayout.addWidget(self.graph3dButton)

        self.radialButton.clicked.connect(self.task10OpenRadial)
        self.graphButton.clicked.connect(self.task10OpenGraph)
        self.graph3dButton.clicked.connect(self.task10Open3dGraph)

        self.canvas10 = QWidget()
        self.canvas10.setStyleSheet("background-color: #21262D;")
        self.horiLayout.addWidget(self.canvas10)

        containerLayout = QVBoxLayout()
        self.canvas10.setLayout(containerLayout)

        graphMaker = NoGraph()
        container = FigureCanvas(graphMaker.getGraph())
        containerLayout.addWidget(container)
 
        self.canvas.setLayout(self.horiLayout)

    def task10SliderUpdate(self):
        for i, slider in enumerate(self.sliders):
            self.slidersLabel[i].setText(f"{self.slidersUse[i][0]}: {slider.value()}")

    def task10OpenRadial(self):
        self.horiLayout.removeWidget(self.canvas10)
        self.canvas10.deleteLater()
        self.canvas10 = QWidget()
        self.canvas10.setStyleSheet("background-color: #21262D;")
        self.horiLayout.addWidget(self.canvas10)

        containerLayout = QVBoxLayout()
        self.canvas10.setLayout(containerLayout)

        if self.text_input.text() and self.sliders[1].value() and self.sliders[2].value():
            graphMaker = Task10Grapher(orbital = self.text_input.text(), Z = self.sliders[1].value(), 
                                    A = self.sliders[2].value())
            container = FigureCanvas(graphMaker.getRadialGraph())
            containerLayout.addWidget(container)
        else:
            self.task10Error()

    def task10OpenGraph(self):
        self.horiLayout.removeWidget(self.canvas10)
        self.canvas10.deleteLater()
        self.canvas10 = QWidget()
        self.canvas10.setStyleSheet("background-color: #21262D;")
        self.horiLayout.addWidget(self.canvas10)

        containerLayout = QVBoxLayout()
        self.canvas10.setLayout(containerLayout)

        if self.text_input.text() and self.sliders[1].value() and self.sliders[2].value() and self.sliders[3].value() and self.sliders[4].value():
            graphMaker = Task10Grapher(self.text_input.text(), self.sliders[0].value(), self.sliders[1].value(), 
                                    self.sliders[2].value(), self.sliders[3].value(), self.sliders[4].value())
            container = FigureCanvas(graphMaker.getGraph())
            containerLayout.addWidget(container)
        else:
            self.task10Error()

    def task10Open3dGraph(self):
        self.horiLayout.removeWidget(self.canvas10)
        self.canvas10.deleteLater()
        self.canvas10 = QWidget()
        self.canvas10.setStyleSheet("background-color: #21262D;")
        self.horiLayout.addWidget(self.canvas10)

        containerLayout = QVBoxLayout()
        self.canvas10.setLayout(containerLayout)

        if self.text_input.text() and self.sliders[1].value() and self.sliders[2].value() and self.sliders[3].value() and self.sliders[4].value():
            graphMaker = Task10Grapher(self.text_input.text(), self.sliders[0].value(), self.sliders[1].value(), 
                                    self.sliders[2].value(), self.sliders[3].value(), self.sliders[4].value())
            container = FigureCanvas(graphMaker.get3dGraph())
            containerLayout.addWidget(container)
        else:
            self.task10Error()

    def task10Error(self):
        self.horiLayout.removeWidget(self.canvas10)
        self.canvas10.deleteLater()

        self.canvas10 = QLabel("Enter required values!")
        self.canvas10.setAlignment(QtCore.Qt.AlignCenter)
        self.horiLayout.addWidget(self.canvas10)
