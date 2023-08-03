import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.stl_vertices = np.empty((0, 3))
        self.translate_x = 0
        self.translate_y = 0

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -6.0)
        glTranslatef(self.translate_x, self.translate_y, 0.0)
        self.draw_stl()

    def draw_stl(self):
        glBegin(GL_TRIANGLES)
        for vertex in self.stl_vertices:
            glVertex3fv(vertex)
        glEnd()

    def load_stl(self, filename):
        try:
            with open(filename, 'r') as file:
                stl_data = file.readlines()

            vertices = []
            for line in stl_data:
                if line.startswith("vertex"):
                    vertex = [float(coord) for coord in line.split()[1:]]
                    vertices.append(vertex)

            self.stl_vertices = np.array(vertices)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading STL file: {str(e)}")

    def translate(self, axis):
        if axis == 'x':
            self.translate_x += 1.0
        elif axis == 'y':
            self.translate_y += 1.0
        self.update()

    def unload_stl(self):
        self.stl_vertices = np.empty((0, 3))
        self.update()


class ViewerApp(QMainWindow):
    def __init__(self):
        super(ViewerApp, self).__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('3D Viewer')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.gl_widget = GLWidget(self)
        layout.addWidget(self.gl_widget)

        load_btn = QPushButton('Load STL', self)
        load_btn.clicked.connect(self.load_stl)
        layout.addWidget(load_btn)

        x_translate_btn = QPushButton('Translate X', self)
        x_translate_btn.clicked.connect(lambda: self.gl_widget.translate('x'))
        layout.addWidget(x_translate_btn)

        y_translate_btn = QPushButton('Translate Y', self)
        y_translate_btn.clicked.connect(lambda: self.gl_widget.translate('y'))
        layout.addWidget(y_translate_btn)

        unload_btn = QPushButton('Unload STL', self)
        unload_btn.clicked.connect(self.gl_widget.unload_stl)
        layout.addWidget(unload_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_stl(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Load STL File", "", "STL Files (*.stl);;All Files (*)", options=options)
        if filename:
            self.gl_widget.load_stl(filename)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ViewerApp()
    window.show()
    sys.exit(app.exec_())
