from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QMessageBox, QCalendarWidget, QLabel, QListWidgetItem)
from PySide6.QtGui import QColor, QIcon
from collections import defaultdict
from utils import save_tasks_to_file, load_tasks_from_file

class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 1000, 800)
        self.setWindowIcon(QIcon('secondlogo.png'))

        self.tasks_by_date = defaultdict(list)

        self.setup_ui()
        self.loadTasksFromFile()

    def setup_ui(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.taskInput = QLineEdit(self)
        self.taskInput.setPlaceholderText("Введите описание задачи...")
        self.layout.addWidget(self.taskInput)

        self.dateLayout = QHBoxLayout()
        self.layout.addLayout(self.dateLayout)

        self.startDateLabel = QLabel("Дата начала:", self)
        self.dateLayout.addWidget(self.startDateLabel)
        self.startDateSelector = QCalendarWidget(self)
        self.startDateSelector.setMaximumSize(400, 200)
        self.dateLayout.addWidget(self.startDateSelector)

        self.deadlineLabel = QLabel("Дедлайн:", self)
        self.dateLayout.addWidget(self.deadlineLabel)
        self.deadlineSelector = QCalendarWidget(self)
        self.deadlineSelector.setMaximumSize(400, 200)
        self.dateLayout.addWidget(self.deadlineSelector)

        self.addButton = QPushButton("Добавить задачу", self)
        self.addButton.clicked.connect(self.addTask)
        self.layout.addWidget(self.addButton)

        self.taskList = QListWidget(self)
        self.layout.addWidget(self.taskList)

        self.removeButton = QPushButton("Удалить выбранную задачу", self)
        self.removeButton.clicked.connect(self.removeTask)
        self.layout.addWidget(self.removeButton)

        self.removeAllButton = QPushButton("Удалить все задачи", self)
        self.removeAllButton.clicked.connect(self.removeAllTasks)
        self.layout.addWidget(self.removeAllButton)

        self.markDoneButton = QPushButton("Отметить как выполненную", self)
        self.markDoneButton.clicked.connect(self.markTaskDone)
        self.layout.addWidget(self.markDoneButton)

    def addTask(self):
        taskDescription = self.taskInput.text()
        startDate = self.startDateSelector.selectedDate().toString("dd-MM-yyyy")
        deadline = self.deadlineSelector.selectedDate().toString("dd-MM-yyyy")
        if taskDescription:
            taskEntry = f"{taskDescription} | Начало: {startDate} | Дедлайн: {deadline}"
            self.tasks_by_date[startDate].append(taskEntry)
            self.taskInput.clear()
            self.updateTaskList()
            self.saveTasksToFile()
        else:
            QMessageBox.information(self, "Пустая задача", "Описание задачи не может быть пустым!")

    def removeTask(self):
        selectedItems = self.taskList.selectedItems()
        if not selectedItems:
            return
        for item in selectedItems:
            for date, tasks in self.tasks_by_date.items():
                if item.text() in tasks:
                    tasks.remove(item.text())
                    break
            self.taskList.takeItem(self.taskList.row(item))
        self.saveTasksToFile()

    def removeAllTasks(self):
        self.tasks_by_date.clear()
        self.updateTaskList()
        self.saveTasksToFile()

    def markTaskDone(self):
        selectedItems = self.taskList.selectedItems()
        if not selectedItems:
            return
        for item in selectedItems:
            if "(выполнено)" not in item.text():
                item.setText(f"{item.text()} (выполнено)")
                item.setForeground(QColor('green'))
                for date, tasks in self.tasks_by_date.items():
                    for i, taskText in enumerate(tasks):
                        if taskText in item.text():
                            tasks[i] = f"{taskText} (выполнено)"
                            break
        self.saveTasksToFile()

    def updateTaskList(self):
        self.taskList.clear()
        for date, tasks in self.tasks_by_date.items():
            for task in tasks:
                item = QListWidgetItem(task)
                if "(выполнено)" in task:
                    item.setForeground(QColor('green'))
                self.taskList.addItem(item)

    def saveTasksToFile(self):
        save_tasks_to_file(self.tasks_by_date)

    def loadTasksFromFile(self):
        self.tasks_by_date = load_tasks_from_file()

