import streamlit as st
from pawpal_system import User, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Initialize or reuse the Owner in session state so it persists across reruns
if "owner" not in st.session_state:
    st.session_state.owner = User(name=owner_name)

# If the user edits the Owner name field, allow updating the stored owner
if st.session_state.owner.name != owner_name:
    st.session_state.owner.name = owner_name

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    # Create a Task object and store it on the owner (keeps session state consistent)
    t = st.session_state.owner.add_task(type=task_title, time_constraints=None, priority=0)
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority, "id": t.id}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Manage Pets")
with st.form("add_pet_form"):
    new_name = st.text_input("New pet name", value="")
    new_species = st.selectbox("Species for new pet", ["dog", "cat", "other"], index=0)
    submitted = st.form_submit_button("Add pet")
    if submitted:
        owner = st.session_state.owner
        pet = owner.add_pet(name=new_name or "Unnamed", species=new_species)
        st.success(f"Added pet: {pet.name} ({pet.species})")

st.markdown("### Your pets")
owner = st.session_state.owner
if owner.pets:
    for p in owner.pets:
        st.write(f"- {p.name} ({p.species}) — {p.task_count} tasks")
else:
    st.info("No pets yet. Add one using the form above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
