from flask import request
from flask.ext.restful import fields, Resource, marshal_with, abort
from wtforms_alchemy import ModelForm, ModelFormField
import wtforms_json

from my_app.v2014_01_19.models import Task, Team
from my_app.v2014_01_19.models.base import session

wtforms_json.init()

resource_fields = {
    "id": fields.Integer,
    "text": fields.String,
    "is_done": fields.Boolean,
    # TODO: The blueprint (version) endpoint should be opaque to this class,
    # but we need it so that Flask can build a URL for the object.
    # Is there a way around this?
    "uri": fields.Url('2014-01-19.todo'),
}

class TeamForm(ModelForm):
    class Meta:
        model = Team

class TaskForm(ModelForm):
    class Meta:
        model = Task

    team = ModelFormField(TeamForm)

# TODO: Auth!
class TaskResource(Resource):

    def _update(self, todo):
        form = TaskForm.from_json(request.json)
        form.validate()
        form.populate_obj(todo)
        session.commit()

    @marshal_with(resource_fields)
    def post(self):
        todo = Task()
        self._update(todo)
        return todo

    @marshal_with(resource_fields)
    def get(self, id=None):
        if id:
            todo = Task.query.filter(Task.id==id).first()
            if not todo:
                abort(404, id=id, message="ID %s not found" % id)
            return todo
        return sorted(Task.query, key=lambda x: x.id)

    @marshal_with(resource_fields)
    def put(self, id):
        todo = Task.query.filter(Task.id==id).first()
        if not todo:
            abort(404, id=id, message="ID %s not found" % id)
        #TODO: validate etag?
        self._update(todo)
        return todo

    @marshal_with(resource_fields)
    def delete(self, id):
        todo = Task.query.filter(Task.id==id).first()
        if not todo:
            abort(404, id=id, message="ID %s not found" % id)
        session.delete(todo)
        session.commit()
        return todo

