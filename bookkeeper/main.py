from PySide6.QtWidgets import QApplication
from bookkeeper.view.expense_view import MainWindow
from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.abstract_repository import AbstractRepository
import sys

DB_NAME = 'test.db'

if __name__ == '__main__':
    app = QApplication(sys.argv)

    view = MainWindow()
    model = None  # TODO: здесь должна быть модель

    cat_repo = SQLiteRepository[Category](DB_NAME, Category)
    exp_repo = SQLiteRepository[Expense](DB_NAME, Expense)
    mem_repo = MemoryRepository[Expense]()

    window = ExpensePresenter(model, view, cat_repo, exp_repo)
    window.show()
    app.exec_()
