import sys, mood_db
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from pathlib import Path
from datetime import datetime

cur_dir = Path.cwd()

class Canvas(FigureCanvas):
    def __init__(self, parent, date):
        self.fig, self.ax = plt.subplots(figsize=(10,4))
        super().__init__(self.fig)
        self.setParent(parent)
        self.values = mood_db.show_values(date)

        self.x = [x[2] for x in self.values]
        self.y = [y[0] for y in self.values]
        self.descriptions = [d[1] for d in self.values]
        self.ax1 = plt.subplot2grid((1,1), (0,0))

        self.lines = self.ax1.bar(self.x, self.y, color="lightsteelblue", edgecolor="black", width=0.95)

        for label in self.ax1.xaxis.get_ticklabels():
            label.set_rotation(45)
    
        self.ax1.tick_params(axis="x", colors="tab:blue")
        self.ax1.tick_params(axis="y", colors="tab:blue")

        self.ax1.xaxis.label.set_color("tab:blue")
        plt.xlabel("Days (Year - Month - Day)")

        self.ax1.yaxis.label.set_color("tab:blue")
        plt.ylabel("Mood Rating")

        date = datetime.strptime(date, "%Y-%m")
        plt.title(f"Mood Rating Graph for {date.strftime('%B %Y')}")

        plt.yticks([1,2,3,4,5,6,7,8,9,10]) # Only shows the available Y values
        plt.subplots_adjust(left=0.060, bottom=0.250, right=0.990, top=0.922)

        # Cursor Hover Annotions
        # This adds the functionality of showing mood descriptions for each day.
        cursor = mplcursors.cursor(self.lines, hover=mplcursors.HoverMode.Transient)
        cursor.connect(
            "add", 
            lambda sel: sel.annotation.set_text(self.descriptions[sel.target.index]))


class AppWindow(QWidget):
    def __init__(self, date):
        super().__init__()
        self.resize(1000, 400)
        self.setMaximumSize(1000, 400)
        self.setMinimumSize(1000, 400)
        self.setWindowTitle(f"Your Mood Rating Graph")
        self.setWindowIcon(QIcon((cur_dir / "test/icon.png").as_posix()))

        self.graph = Canvas(self, date)

if __name__ == "__main__":
    print("Name Main")
    app = QApplication(sys.argv)
    graph = AppWindow("2021-10")
    graph.show()
    sys.exit(app.exec_())

