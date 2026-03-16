from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import uuid
import datetime
from datetime import datetime as _dt, date as _date, timedelta


def _new_id() -> str:
	return str(uuid.uuid4())


@dataclass
class Pet:
	id: str = field(default_factory=_new_id)
	name: str = ""
	species: str = ""
	date_of_birth: Optional[datetime.date] = None
	tasks: List["Task"] = field(default_factory=list)

	def add_task(self, *, type: str, time_constraints: Optional[str] = None, priority: int = 0,
				 owner_preference: Optional[str] = None, assigned_to_user_id: Optional[str] = None) -> "Task":
		task = Task(type=type, time_constraints=time_constraints, priority=priority,
					owner_preference=owner_preference, assigned_to_user_id=assigned_to_user_id,
					assigned_pet_id=self.id)
		self.tasks.append(task)
		return task

	@property
	def task_count(self) -> int:
		return len(self.tasks)


@dataclass
class Task:
	id: str = field(default_factory=_new_id)
	type: str = ""
	time_constraints: Optional[str] = None
	priority: int = 0
	owner_preference: Optional[str] = None
	assigned_to_user_id: Optional[str] = None
	assigned_pet_id: Optional[str] = None
	completed: bool = False
	frequency: Optional[str] = None  # e.g., 'daily', 'weekly'
	due_date: Optional[_date] = None

	def update(self, **kwargs: Any) -> None:
		for k, v in kwargs.items():
			if hasattr(self, k):
				setattr(self, k, v)

	def mark_complete(self) -> Optional["Task"]:
		"""Mark this task complete. If the task is recurring ('daily' or 'weekly'),
		create and return a new Task instance for the next occurrence. Otherwise return None.
		"""
		self.completed = True

		if not self.frequency:
			return None

		freq = self.frequency.lower() if isinstance(self.frequency, str) else ""
		if freq not in ("daily", "weekly"):
			return None

		days = 1 if freq == "daily" else 7

		new_due: Optional[_date] = None
		if self.due_date:
			new_due = self.due_date + timedelta(days=days)
		else:
			# if no explicit due_date, set to today + days
			new_due = _date.today() + timedelta(days=days)

		new_task = Task(
			type=self.type,
			time_constraints=self.time_constraints,
			priority=self.priority,
			owner_preference=self.owner_preference,
			assigned_to_user_id=self.assigned_to_user_id,
			assigned_pet_id=self.assigned_pet_id,
			frequency=self.frequency,
			due_date=new_due,
		)

		return new_task


@dataclass
class Availability:
	day: str
	start_time: str
	end_time: str


@dataclass
class Scheduler:
	tasks: List[Task] = field(default_factory=list)
	availability: List[Availability] = field(default_factory=list)

	def schedule_tasks(self) -> List[Task]:
		# TODO: implement scheduling algorithm
		return self.tasks

	def _parse_start_time(self, t: Task) -> Optional[_dt.time]:
		"""Return a time object parsed from a Task's time_constraints (HH:MM[-...])
		or from due_date (as midnight) if present. Returns None if unavailable.
		"""
		if t.time_constraints:
			try:
				start = t.time_constraints.split("-")[0].strip()
				return _dt.strptime(start, "%H:%M").time()
			except Exception:
				return None
		if t.due_date:
			return _dt.min.time()
		return None

	def sort_by_time(self) -> List[Task]:
		"""Return tasks sorted by parsed start time, then by priority."""
		return sorted(self.tasks, key=lambda t: (
			self._parse_start_time(t) or _dt.max.time(),
			t.priority
		))

	def filter_tasks(self, owner: Optional["User"] = None, *, completed: Optional[bool] = None,
					 pet_name: Optional[str] = None) -> List[Task]:
		"""Filter tasks by completion status and/or pet name (requires owner to resolve names)."""
		results = list(self.tasks)
		if completed is not None:
			results = [t for t in results if t.completed is completed]

		if pet_name and owner is not None:
			matching_ids = [p.id for p in owner.pets if p.name == pet_name]
			results = [t for t in results if t.assigned_pet_id in matching_ids]

		return results

	def detect_conflicts(self) -> List[str]:
		"""Lightweight conflict detection: tasks with identical start times are considered conflicts.
		Returns a list of warning messages."""
		warnings: List[str] = []
		bucket: Dict[str, List[Task]] = {}
		for t in self.tasks:
			key = t.time_constraints or (t.due_date.isoformat() if t.due_date else "")
			if not key:
				continue
			bucket.setdefault(key, []).append(t)

		for k, group in bucket.items():
			if len(group) > 1:
				ids = [f"{g.type} (pet={g.assigned_pet_id})" for g in group]
				warnings.append(f"Conflict at {k}: " + ", ".join(ids))

		return warnings


@dataclass
class User:
	id: str = field(default_factory=_new_id)
	name: str = ""
	pets: List[Pet] = field(default_factory=list)
	tasks: List[Task] = field(default_factory=list)

	def add_pet(self, name: str, species: str, date_of_birth: Optional[datetime.date] = None) -> Pet:
		pet = Pet(name=name, species=species, date_of_birth=date_of_birth)
		self.pets.append(pet)
		return pet

	def add_task(self, *, type: str, time_constraints: Optional[str] = None, priority: int = 0,
				 owner_preference: Optional[str] = None, assigned_pet_id: Optional[str] = None,
				 frequency: Optional[str] = None, due_date: Optional[_date] = None) -> Task:
		task = Task(type=type, time_constraints=time_constraints, priority=priority,
					owner_preference=owner_preference, assigned_to_user_id=self.id,
					assigned_pet_id=assigned_pet_id, frequency=frequency, due_date=due_date)
		self.tasks.append(task)
		return task

	def edit_task(self, task_id: str, updates: Dict[str, Any]) -> Optional[Task]:
		for t in self.tasks:
			if t.id == task_id:
				t.update(**updates)
				return t
		return None

