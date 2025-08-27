import streamlit as st
import pandas as pd
import altair as alt
from utils import (
    add_employee, get_all_employees, search_employee_by_id, search_employee_by_name,
    sort_employees_by_key, update_employee, delete_employee, generate_next_id,
    get_departments, get_modes
)
st.set_page_config(page_title="Employee Record System", layout="wide")
st.title("👨‍💼 Employee Record System")
menu = ["Add Employee", "View All", "Search", "Sort", "Update", "Delete", "Stats"]
choice = st.sidebar.selectbox("📂 Select Action", menu)
if choice == "Add Employee":
    st.subheader("➕ Add New Employee")
    col1, col2 = st.columns(2)
    with col1:
        auto_id = st.checkbox("Auto-generate Employee ID", value=True)
        emp_id = generate_next_id() if auto_id else st.text_input("Employee ID")
        name = st.text_input("Full Name")
        department = st.text_input("Department")
        role = st.text_input("Role")
    with col2:
        salary = st.number_input("Salary 💰", min_value=0)
        emp_type = st.selectbox("Work Type", ["Intern", "Full Time"])
        work_mode = st.selectbox("Work Mode", ["Remote", "Office", "Hybrid"])
    if st.button("Add Employee"):
        if emp_id and name:
            new_emp = {
                "id": emp_id,
                "name": name,
                "department": department,
                "role": role,
                "salary": salary,
                "type": emp_type,
                "mode": work_mode
            }
            add_employee(new_emp)
            st.success(f"✅ Employee {name} added successfully!")
        else:
            st.warning("⚠️ Employee ID and Name are required!")
elif choice == "View All":
    st.subheader("📋 All Employees")
    data = get_all_employees()
    with st.expander("🔍 Filter Options"):
        depts = get_departments()
        modes = get_modes()
        selected_dept = st.selectbox("Filter by Department", ["All"] + depts)
        selected_mode = st.selectbox("Filter by Work Mode", ["All"] + modes)
        if selected_dept != "All":
            data = [d for d in data if d["department"] == selected_dept]
        if selected_mode != "All":
            data = [d for d in data if d["mode"] == selected_mode]
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", csv, "employees.csv", "text/csv")
    else:
        st.info("No employees found.")
elif choice == "Search":
    st.subheader("🔎 Search Employee")
    search_by = st.radio("Search by", ["ID", "Name"])
    query = st.text_input("Enter search query")
    if st.button("Search"):
        result = search_employee_by_id(query) if search_by == "ID" else search_employee_by_name(query)
        if result:
            st.success(f"Found {len(result)} result(s)")
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("No employee found.")
elif choice == "Sort":
    st.subheader("↕️ Sort Employees")
    sort_key = st.selectbox("Sort by", ["id", "name", "department", "salary"])
    sorted_data = sort_employees_by_key(sort_key)
    st.dataframe(sorted_data, use_container_width=True)
elif choice == "Update":
    st.subheader("🛠️ Update Employee")
    emp_id = st.text_input("Enter Employee ID to update")
    if st.button("Fetch"):
        data = search_employee_by_id(emp_id)
        if data:
            emp = data[0]
            name = st.text_input("Name", emp["name"])
            department = st.text_input("Department", emp["department"])
            role = st.text_input("Role", emp["role"])
            salary = st.number_input("Salary", value=emp["salary"])
            emp_type = st.selectbox("Work Type", ["Intern", "Full Time"], index=["Intern", "Full Time"].index(emp["type"]))
            work_mode = st.selectbox("Work Mode", ["Remote", "Office", "Hybrid"], index=["Remote", "Office", "Hybrid"].index(emp["mode"]))
            if st.button("Update"):
                updated_fields = {
                    "name": name,
                    "department": department,
                    "role": role,
                    "salary": salary,
                    "type": emp_type,
                    "mode": work_mode
                }
                update_employee(emp_id, updated_fields)
                st.success("✅ Employee updated successfully.")
        else:
            st.warning("Employee not found.")
elif choice == "Delete":
    st.subheader("🗑️ Delete Employee")
    emp_id = st.text_input("Enter Employee ID to delete")
    confirm = st.checkbox("Yes, I want to delete this employee")
    if st.button("Delete") and confirm:
        success = delete_employee(emp_id)
        if success:
            st.success("✅ Employee deleted.")
        else:
            st.warning("⚠️ Employee ID not found.")
elif choice == "Stats":
    st.subheader("📊 Employee Overview")
    data = get_all_employees()
    if data:
        df = pd.DataFrame(data)
        dept_chart = alt.Chart(df).mark_bar().encode(
            x="department:N",
            y="count():Q",
            color="department:N"
        ).properties(title="Employees per Department")

        st.altair_chart(dept_chart, use_container_width=True)
    else:
        st.info("No data available.")