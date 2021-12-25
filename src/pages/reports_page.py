from flask import Blueprint, render_template, request, redirect, session
import services.reports as reports
import services.users as users

reports_page = Blueprint("reports_page", __name__)

#============Reports============

@reports_page.route("/posts/create", methods=["POST"])
def create_post():
    if not users.auth():
        return redirect("/users/login")

    if not users.csrf():
        return render_template("error.html", error="CSRF Token missing")

    content = request.form["content"]
    reports.create(content, users.id())
    return redirect("/")


@reports_page.route("/<username>/<post_id>")
def view_post(username, post_id):
    if not users.auth():
        return redirect("/users/login")

    post_data = reports.get_by_id(username, post_id)
    return render_template("post.html", post=post_data)
