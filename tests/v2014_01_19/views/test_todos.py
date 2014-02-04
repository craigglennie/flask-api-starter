from nose.tools import *

from my_app.v2014_01_19.models import ToDo
from my_app.v2014_01_19.views import ToDoResource
from tests.v2014_01_19 import ResourceTestCase
from tests.model_factory import ModelFactory

class ToDoFactory(ModelFactory):
    FACTORY_FOR = ToDo
    text = "Buy eggs"

class TestToDos(ResourceTestCase):
    RESOURCE = ToDoResource

    def test_create_todo(self):
        text = "Buy milk"
        json = self.json_POST(text=text)
        assert_equal(json["text"], text)
        assert_false(json["is_done"])
        assert_equal(json["id"], 1)
        todo = ToDo.by_id(1)
        assert_equal(todo.text, text)
        assert_false(todo.is_done)

    def test_get_todo(self):
        todo = ToDoFactory()
        json = self.json_GET(id=todo.id)
        assert_equal(json["text"], todo.text)

    def test_list_todos(self):
        todo_1 = ToDoFactory()
        todo_2 = ToDoFactory(text="Buy bananas")
        json = self.json_GET()
        assert_equal(len(json), 2)
        assert_equal(json[0]["text"], todo_1.text)
        assert_equal(json[1]["text"], todo_2.text)

    def test_update_todo(self):
        todo = ToDoFactory()
        new_text = "Buy bananas"
        json = self.json_PUT(id=todo.id, text=new_text, is_done=True)
        assert_equal(json["text"], new_text)
        todo = ToDo.by_id(todo.id)
        assert_equal(todo.text, new_text)

