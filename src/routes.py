from __main__ import app

from pages.home_page import home_page
from pages.user_page import user_page
from pages.reports_page import reports_page

app.register_blueprint(user_page)
app.register_blueprint(reports_page)
app.register_blueprint(home_page)



