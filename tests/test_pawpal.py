def test_add_task_to_pet():
import datetime
from pawpal_system import User, Task, Scheduler


def test_sorting_correctness():
    owner = User(name="Test")
    # add out-of-order tasks
    owner.add_task(type="Evening", time_constraints="18:00-18:30")
    owner.add_task(type="Morning", time_constraints="08:00-08:30")
    owner.add_task(type="Noon", time_constraints="12:00-12:30")

    scheduler = Scheduler(tasks=owner.tasks)
    sorted_tasks = scheduler.sort_by_time()
    assert [t.type for t in sorted_tasks] == ["Morning", "Noon", "Evening"]


def test_recurrence_logic():
    owner = User(name="Tester")
    today = datetime.date.today()
    t = owner.add_task(type="Daily Clean", time_constraints="07:00-07:15", frequency="daily", due_date=today)

    # mark complete and ensure a new task for tomorrow is returned
    new_task = t.mark_complete()
    assert t.completed is True
    assert new_task is not None
    assert new_task.frequency == "daily"
    assert new_task.due_date == today + datetime.timedelta(days=1)


def test_conflict_detection():
    owner = User(name="ConflictOwner")
    pet1 = owner.add_pet(name="A", species="dog")
    pet2 = owner.add_pet(name="B", species="cat")

    owner.add_task(type="Task1", time_constraints="09:00-09:30", assigned_pet_id=pet1.id)
    owner.add_task(type="Task2", time_constraints="09:00-09:30", assigned_pet_id=pet2.id)

    scheduler = Scheduler(tasks=owner.tasks)
    warns = scheduler.detect_conflicts()
    assert len(warns) >= 1
    assert "09:00-09:30" in warns[0]
