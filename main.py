from gui import controller
from gui import view
from gui import model

model = model.Model()
app = view.View(model)
app.Run()
