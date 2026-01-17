import streamlit as st
from datetime import datetime




#_____________
st.set_page_config(page_title="Student Planner", page_icon="🤓", layout="centered")

if "tasks" not in st.session_state:
    st.session_state.tasks = []  # CREATE EMPTY LIST FOR TASKS

# ADD TASK FUNCTION
def add_task(name, due_date, priority):
    task = {
        "name": name,
        "due_date": due_date,
        "priority": priority,
        "completed": False
    }
    st.session_state.tasks.append(task)
#_____________


# SINGLE CLICK CALLBACKS
def mark_complete(idx):
    st.session_state.tasks[idx]["completed"] = True

def remove_task(idx):
    st.session_state.tasks.pop(idx)

# VIEW TASKS FUNCTION
def view_tasks():
    if not st.session_state.tasks:
        st.info("No tasks added yet.")
        return

    today = datetime.today().date()

    for i, task in enumerate(st.session_state.tasks):
        task_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
        color = "green" if task["completed"] else "red" if task_date < today else "black"

        with st.container():
            cols = st.columns([3, 2, 2, 2, 2, 2])
       #_____________#_____________     
            # TASK DETAILS
            cols[0].markdown(f'<span style="color:{color}"><b>{task["name"]}</b></span>', unsafe_allow_html=True)
#_____________
            cols[1].markdown(f'<span style="color:{color}">{task["due_date"]}</span>', unsafe_allow_html=True)
#_____________
            cols[2].markdown(f'<span style="color:{color}">{task["priority"]}</span>', unsafe_allow_html=True)
#_____________
            status_text = "Completed" if task["completed"] else "Incomplete"
            cols[3].markdown(f'<span style="color:{color}">{status_text}</span>', unsafe_allow_html=True)
#_____________
            # SINGLE CLICK BUTTONS USING CALLBACKS
            if not task["completed"]:
                cols[4].button("Mark Complete", key=f"complete_{i}", on_click=mark_complete, args=(i,))
            cols[5].button("Remove", key=f"remove_{i}", on_click=remove_task, args=(i,))
#_____________
    # TASK STATS
    st.markdown(f"**Total Tasks:** {len(st.session_state.tasks)}")
    completed_count = sum(1 for t in st.session_state.tasks if t["completed"])
    st.markdown(f"**Completed Tasks:** {completed_count}")
    st.markdown(f"**Incomplete Tasks:** {len(st.session_state.tasks) - completed_count}")

# MAIN FUNCTION
def main():
    st.title("Student Planner")

    menu = ["Add Task", "View Tasks"]
    choice = st.sidebar.radio("Menu", menu)

    if choice == "Add Task":
        st.subheader("Add a New Task")
        with st.form("add_task_form"):
            name = st.text_input("Task Name")
            due_date = st.date_input("Due Date", min_value=datetime.today())
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            submit = st.form_submit_button("Add Task")
            if submit:
                if name.strip() == "":
                    st.error("Task name cannot be empty")
                else:
                    add_task(name, due_date.strftime("%Y-%m-%d"), priority)
                    st.success(f'Task "{name}" added successfully')

    elif choice == "View Tasks":
        st.subheader("All Tasks")
        view_tasks()

main()
