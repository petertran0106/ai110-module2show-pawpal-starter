from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import uuid
import datetime


def _new_id() -> str:
	return str(uuid.uuid4())


@dataclass
class Pet:
	id: str = field(default_factory=_new_id)
	name: str = ""
	species: str = ""
	date_of_birth: Optional[datetime.date] = None


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

	def update(self, **kwargs: Any) -> None:
		for k, v in kwargs.items():
			if hasattr(self, k):
				setattr(self, k, v)


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
				 owner_preference: Optional[str] = None, assigned_pet_id: Optional[str] = None) -> Task:
		task = Task(type=type, time_constraints=time_constraints, priority=priority,
					owner_preference=owner_preference, assigned_to_user_id=self.id,
					assigned_pet_id=assigned_pet_id)
		self.tasks.append(task)
		return task

	def edit_task(self, task_id: str, updates: Dict[str, Any]) -> Optional[Task]:
		for t in self.tasks:
			if t.id == task_id:
				t.update(**updates)
				return t
		return None

