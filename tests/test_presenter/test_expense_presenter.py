from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.view.expense_view import ExpenseView

def test_expense_presenter():
    # Create mock objects
    mock_model = None
    mock_view = ExpenseView()
    mock_cat_repo = SQLiteRepository[Category]('test.db', Category)  
    mock_exp_repo = MemoryRepository[Expense]()

    # Create the presenter object
    presenter = ExpensePresenter(mock_model, mock_view, mock_cat_repo, mock_exp_repo)

    # Test the update_expense_data() method
    def test_update_expense_data():
        mock_exp_repo.add(Expense(100, 1))
        presenter.update_cat_data()
        presenter.update_expense_data()
        assert len(presenter.exp_data) == 1
        assert presenter.exp_data[0].amount == 100
        assert presenter.exp_data[0].category == "Groceries"

    # Test the update_cat_data() method
    def test_update_cat_data():
        mock_cat_repo.add("Groceries")
        presenter.update_cat_data()
        assert len(presenter.cat_data) == 1
        assert presenter.cat_data[0].name == "Groceries"

    # Test the handle_expense_add_button_clicked() method
    def test_handle_expense_add_button_clicked():
        mock_view.set_selected_cat(1)
        mock_view.set_amount("50")
        presenter.handle_expense_add_button_clicked()
        assert len(presenter.exp_data) == 2
        assert presenter.exp_data[1].amount == 50
        assert presenter.exp_data[1].category == "Groceries"

    # Test the handle_expense_delete_button_clicked() method
    def test_handle_expense_delete_button_clicked():
        mock_view.set_selected_expenses([presenter.exp_data[0]])
        presenter.handle_expense_delete_button_clicked()
        assert len(presenter.exp_data) == 1

    # Test the handle_category_edit_button_clicked() method
    def test_handle_category_edit_button_clicked():
        mock_view.set_cats_dialog_response("Groceries")
        presenter.handle_category_edit_button_clicked()
        assert len(presenter.cat_data) == 1
        assert presenter.cat_data[0].name == "Groceries"

