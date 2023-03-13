from bookkeeper.models.expense import Expense

class ExpensePresenter:

    def __init__(self, model, view, cat_repo, exp_repo):
        self.model = model
        self.view = view
        self.cat_repo = cat_repo
        self.exp_repo = exp_repo
        self.exp_data = None
        self.cat_data = None
        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)
        self.view.on_expense_delete_button_clicked(self.handle_expense_delete_button_clicked)
        self.view.on_category_edit_button_clicked(self.handle_category_edit_button_clicked)
        self.update_cat_data()

    def update_expense_data(self):
        self.exp_data = self.exp_repo.get_all()
        if self.exp_data is None or len(self.exp_data) == 0:
            # handle the case where there is no data
            print("No expense data found.")
        else:
            for e in self.exp_data:
                for c in self.cat_data:
                    if c.pk == e.category:
                        e.category = c.name
                        break
            self.view.set_expense_table(self.exp_data)

    def update_cat_data(self):
        self.cat_data = self.cat_repo.get_all()
        if self.cat_data is None or len(self.cat_data) == 0:
            print("No categories found. Please add some categories first.")
        else:
            self.view.set_category_dropdown(self.cat_data)

    def show(self):
        self.view.show()
        self.update_expense_data()
        self.update_cat_data()

    def handle_expense_add_button_clicked(self) -> None:
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        exp = Expense(int(amount), int(cat_pk))
        self.exp_repo.add(exp)
        self.update_expense_data()

    def handle_expense_delete_button_clicked(self) -> None:
        selected = self.view.get_selected_expenses()
        if selected:
            for e in selected:
                self.exp_repo.delete(e)
            self.update_expense_data()

    def handle_category_edit_button_clicked(self):
        self.view.show_cats_dialog(self.cat_data)
