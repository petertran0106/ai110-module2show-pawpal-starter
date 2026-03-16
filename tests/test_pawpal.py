import pytest

from pawpal_system import Pet, Task


def test_mark_complete():
    t = Task(type="feed")
    assert not t.completed
    t.mark_complete()
    assert t.completed


def test_add_task_to_pet():
    p = Pet(name="Fido", species="dog")
    assert p.task_count == 0
    t = p.add_task(type="walk", time_constraints="morning", priority=1)
    assert p.task_count == 1
    assert p.tasks[0] is t
    assert t.type == "walk"
    assert t.assigned_pet_id == p.id
