from nose.tools import *
import factory

from my_app.v2014_01_19.models import Task, Team
from my_app.v2014_01_19.views import TaskResource
from tests.v2014_01_19 import ResourceTestCase
from tests.model_factory import ModelFactory

class TeamFactory(ModelFactory):
    FACTORY_FOR = Team
    name = "Test team"

class TaskFactory(ModelFactory):
    FACTORY_FOR = Task
    text = "Buy eggs"
    team = factory.SubFactory(TeamFactory)

class TestTasks(ResourceTestCase):
    RESOURCE = TaskResource

    def assert_URI(self, json, id):
        assert_equal(json["uri"], "/2014-01-19/todos/%s" % id)

    def test_list(self):
        todo_1 = TaskFactory()
        todo_2 = TaskFactory(text="Buy bananas")
        json = self.json_GET()
        assert_equal(len(json), 2)
        assert_equal(json[0]["text"], todo_1.text)
        self.assert_URI(json[0], todo_1.id)
        assert_equal(json[1]["text"], todo_2.text)
        self.assert_URI(json[1], todo_2.id)

    def test_create(self):
        text = "Buy milk"
        team = TeamFactory()
        json = self.json_POST(text=text, team_id=team.id)
        assert_equal(json["id"], 1)
        assert_equal(json["text"], text)
        assert_false(json["is_done"])
        self.assert_URI(json, 1)

        todo = Task.by_id(1)
        assert_equal(todo.text, text)
        assert_false(todo.is_done)

    def test_get(self):
        todo = TaskFactory()
        json = self.json_GET(id=todo.id)
        assert_equal(json["text"], todo.text)
        self.assert_URI(json, todo.id)

    def test_get_not_found(self):
        json = self.json_GET(id=1, expect_status_code=404)
        assert_equal(json["id"], 1)

    def test_update(self):
        todo = TaskFactory()
        new_text = "Buy bananas"
        json = self.json_PUT(id=todo.id, text=new_text, is_done=True)
        assert_equal(json["text"], new_text)
        todo = Task.by_id(todo.id)
        assert_equal(todo.text, new_text)

    def test_update_not_found(self):
        json = self.json_PUT(id=1, is_done=True, expect_status_code=404)
        assert_equal(json["id"], 1)

    def test_delete(self):
        todo = TaskFactory()
        json = self.json_DELETE(id=todo.id)
        assert_is_none(Task.by_id(todo.id))
