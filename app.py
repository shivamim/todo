import streamlit as st
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="My To-Do List",
    page_icon="✅",
    layout="wide"
)

# Initialize session state
if 'todos' not in st.session_state:
    st.session_state.todos = []

if 'completed' not in st.session_state:
    st.session_state.completed = []

def add_task(task, priority="Medium"):
    """Add a new task to the todo list"""
    new_task = {
        'id': len(st.session_state.todos) + len(st.session_state.completed),
        'task': task,
        'priority': priority,
        'created': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'completed': False
    }
    st.session_state.todos.append(new_task)

def complete_task(task_id):
    """Mark a task as completed"""
    for i, task in enumerate(st.session_state.todos):
        if task['id'] == task_id:
            task['completed'] = True
            task['completed_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.completed.append(task)
            st.session_state.todos.pop(i)
            break

def delete_task(task_id, from_completed=False):
    """Delete a task permanently"""
    if from_completed:
        st.session_state.completed = [task for task in st.session_state.completed if task['id'] != task_id]
    else:
        st.session_state.todos = [task for task in st.session_state.todos if task['id'] != task_id]

def main():
    st.title("✅ My Personal To-Do List")
    st.markdown("---")
    
    # Sidebar for adding new tasks
    with st.sidebar:
        st.header("Add New Task")
        new_task = st.text_input("Task description", placeholder="Enter your task here...")
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        
        if st.button("Add Task", type="primary"):
            if new_task.strip():
                add_task(new_task.strip(), priority)
                st.success(f"Task added successfully!")
                st.rerun()
            else:
                st.error("Please enter a task description")
        
        st.markdown("---")
        
        # Statistics
        st.header("📊 Statistics")
        total_tasks = len(st.session_state.todos) + len(st.session_state.completed)
        completed_tasks = len(st.session_state.completed)
        pending_tasks = len(st.session_state.todos)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", total_tasks)
            st.metric("Pending", pending_tasks)
        with col2:
            st.metric("Completed", completed_tasks)
            if total_tasks > 0:
                completion_rate = (completed_tasks / total_tasks) * 100
                st.metric("Progress", f"{completion_rate:.1f}%")
    
    # Main content area
    col1, col2 = st.columns(2)
    
    # Pending Tasks
    with col1:
        st.header("📝 Pending Tasks")
        
        if st.session_state.todos:
            # Sort by priority
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            sorted_todos = sorted(st.session_state.todos, 
                                key=lambda x: priority_order[x['priority']])
            
            for task in sorted_todos:
                # Color coding for priority
                priority_colors = {
                    "High": "🔴",
                    "Medium": "🟡", 
                    "Low": "🟢"
                }
                
                with st.container():
                    col_task, col_actions = st.columns([3, 1])
                    
                    with col_task:
                        st.write(f"{priority_colors[task['priority']]} **{task['task']}**")
                        st.caption(f"Created: {task['created']} | Priority: {task['priority']}")
                    
                    with col_actions:
                        if st.button("✅", key=f"complete_{task['id']}", help="Mark as completed"):
                            complete_task(task['id'])
                            st.rerun()
                        
                        if st.button("🗑️", key=f"delete_{task['id']}", help="Delete task"):
                            delete_task(task['id'])
                            st.rerun()
                
                st.markdown("---")
        else:
            st.info("No pending tasks! Add some tasks to get started.")
    
    # Completed Tasks
    with col2:
        st.header("✅ Completed Tasks")
        
        if st.session_state.completed:
            for task in reversed(st.session_state.completed[-10:]):  # Show last 10 completed
                with st.container():
                    col_task, col_actions = st.columns([3, 1])
                    
                    with col_task:
                        st.write(f"~~{task['task']}~~")
                        st.caption(f"Completed: {task.get('completed_date', 'N/A')}")
                    
                    with col_actions:
                        if st.button("🗑️", key=f"delete_completed_{task['id']}", help="Delete permanently"):
                            delete_task(task['id'], from_completed=True)
                            st.rerun()
                
                st.markdown("---")
        else:
            st.info("No completed tasks yet!")
    
    # Clear all button
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("🗑️ Clear All Completed Tasks", type="secondary"):
            st.session_state.completed = []
            st.success("All completed tasks cleared!")
            st.rerun()

if __name__ == "__main__":
    main()
