from flask import request
from flask.ext.restful import fields, Resource, marshal_with
from wtforms_alchemy import ModelForm
import wtforms_json

from my_app.v2014_01_19.models.todo import ToDo
from my_app.v2014_01_19.models.base import session

wtforms_json.init()

resource_fields = {
    "id": fields.Integer,
    "text": fields.String,
    "is_done": fields.Boolean,
}

class ToDoForm(ModelForm):
    class Meta:
        model = ToDo

class ToDoResource(Resource):

    def _update(self, todo):
        form = ToDoForm.from_json(request.json)
        form.validate()
        form.populate_obj(todo)
        session.commit()

    @marshal_with(resource_fields)
    def post(self):
        todo = ToDo()
        self._update(todo)
        return todo

    @marshal_with(resource_fields)
    def get(self, todo_id=None):
        if todo_id:
            todo = ToDo.query.filter(ToDo.id==todo_id).one()
            assert todo, "Handle missing todo"
            return todo
        return sorted(ToDo.query, key=lambda x: x.id)
        assert False, "handle listing todos"

    @marshal_with(resource_fields)
    def put(self, todo_id):
        todo = ToDo.query.filter(ToDo.id==todo_id).one()
        self._update(todo)
        return todo
        #TODO: "validate etag"
        #TODO: "Handle missing todo"


