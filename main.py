from pawpal_system import User
import datetime


def _parse_start(time_range: str):
    if not time_range:
        return datetime.time(23, 59)
    try:
        start = time_range.split("-")[0].strip()
        return datetime.datetime.strptime(start, "%H:%M").time()
    except Exception:
        return datetime.time(23, 59)


def main():
    owner = User(name="Alice")

    # Create pets
    pet1 = owner.add_pet(name="Buddy", species="Dog")
    pet2 = owner.add_pet(name="Mittens", species="Cat")

    # Add tasks to pets (different times)
    owner.add_task(type="Morning Walk", time_constraints="08:00-09:00", priority=1, assigned_pet_id=pet1.id)
    # Add tasks out of order to demonstrate sorting
    owner.add_task(type="Evening Play", time_constraints="18:30-19:00", priority=1, assigned_pet_id=pet1.id)
    owner.add_task(type="Lunch Feed", time_constraints="12:00-12:15", priority=2, assigned_pet_id=pet2.id)
    owner.add_task(type="Afternoon Nap", time_constraints="12:00-13:00", priority=3, assigned_pet_id=pet1.id, frequency="daily")

    # Print today's schedule
    print(f"Today's Schedule for {owner.name}")
    # Use Scheduler to sort and filter tasks
    from pawpal_system import Scheduler

    scheduler = Scheduler(tasks=owner.tasks)
    tasks_sorted = scheduler.sort_by_time()
    for t in tasks_sorted:
        pet_name = next((p.name for p in owner.pets if p.id == t.assigned_pet_id), "Unassigned")
        print(f"- {t.type} ({t.time_constraints}) for {pet_name} [Priority {t.priority}]")

    print('\nFiltered: tasks for Buddy')
    filtered = scheduler.filter_tasks(owner=owner, pet_name="Buddy")
    for t in filtered:
        print(f"- {t.type} at {t.time_constraints}")

    # Add two conflicting tasks to demonstrate conflict detection
    owner.add_task(type="Conflict A", time_constraints="09:00-09:30", priority=1, assigned_pet_id=pet1.id)
    owner.add_task(type="Conflict B", time_constraints="09:00-09:30", priority=2, assigned_pet_id=pet2.id)
    scheduler.tasks = owner.tasks
    warns = scheduler.detect_conflicts()
    if warns:
        print('\nConflicts detected:')
        for w in warns:
            print(f"- {w}")


if __name__ == "__main__":
    main()
