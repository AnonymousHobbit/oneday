from __main__ import app

from pages.home_page import home_page
from pages.user_page import user_page
from pages.company_page import company_page

app.register_blueprint(user_page)
app.register_blueprint(home_page)
app.register_blueprint(company_page)



