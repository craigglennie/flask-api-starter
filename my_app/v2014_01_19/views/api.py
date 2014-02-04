from flask import Blueprint
from flask.ext import restful

from my_app.v2014_01_19.views.todo_views import ToDoResource


VERSION = "2014-01-19"
blueprint = Blueprint(VERSION, __name__)

api = restful.Api(blueprint, prefix="/" + VERSION)
api.add_resource(ToDoResource, "/todos/<int:todo_id>", endpoint="todo")
api.add_resource(ToDoResource, "/todos", endpoint="todos")

