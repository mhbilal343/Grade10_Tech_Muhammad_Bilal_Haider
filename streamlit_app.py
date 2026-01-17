import streamlit as st
from datetime import datetime


#__________________________________________

st.set_page_config(page_title="Student Planner", page_icon='🤓', layout='centered')

#__________________________________________

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

def add_task(name, due_date, priority):
    task = {
        "name": name,
        "due_date": due_date,
        "priority": priority,
        'completed': False
    }
    st.session_state.tasks.append(task)

def view_tasks():
    if not st.session_state.tasks:
        st.info("No tasks added yet.")
        return

    mark_complete_index = None
    remove_index = None
    today = datetime.today().date()
#__________________________________________
    for i, task in enumerate(st.session_state.tasks):
        task_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
        if task["completed"]:
            color = 'green'
        elif task_date < today:
            color = "red"
        else:
            color = 'black'

        
        
        
        with st.container():
            cols = st.columns([3, 2, 2, 2, 2, 2])
            cols[0].markdown(f"<span style='color:{color}'><b>{task['name']}</b></span>", unsafe_allow_html=True)
            cols[1].markdown(f"<span style='color:{color}'>{task['due_date']}</span>", unsafe_allow_html=True)
            cols[2].markdown(f"<span style='color:{color}'>{task['priority']}</span>", unsafe_allow_html=True)
            status_text = 'Completed' if task['completed'] else 'Incomplete'
            cols[3].markdown(f"<span style='color:{color}'>{status_text}</span>", unsafe_allow_html=True)

            if not task["completed"] and cols[4].button('Mark Complete', key=f'complete_{i}'):
                mark_complete_index = i

            if cols[5].button('Remove', key=f'remove_{i}'):
                remove_index = i

    if mark_complete_index is not None:
        st.session_state.tasks[mark_complete_index]['completed'] = True
        st.success(f"'{st.session_state.tasks[mark_complete_index]['name']}' marked as complete")

    if remove_index is not None:
        removed_task = st.session_state.tasks.pop(remove_index)
        st.success(f"'{removed_task['name']}' has been removed")
#__________________________________________


def main():
    st.title("Student Planner / To-Do List App")

    menu = ['Add Task', 'View Tasks']
    choice = st.sidebar.radio('Menu', menu)

    if choice == "Add Task":
        st.subheader('Add a New Task')
        with st.form('add_task_form'):
            name = st.text_input('Task Name')
            due_date = st.date_input('Due Date', min_value=datetime.today())
            priority = st.selectbox('Priority', ['High', 'Medium', 'Low'])
            submit = st.form_submit_button('Add Task')
            if submit:
                if name.strip() == '':
                    st.error('Task name cannot be empty')
                else:
                    add_task(name, due_date.strftime('%Y-%m-%d'), priority)
                    st.success(f'Task "{name}" added successfully')

    elif choice == 'View Tasks':
        st.subheader('All Tasks')
        view_tasks()

main()