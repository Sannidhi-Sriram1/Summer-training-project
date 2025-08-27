import json
import os
DATA_FILE = "data.json"
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
def add_employee(emp):
    data = load_data()
    data.append(emp)
    save_data(data)
def get_all_employees():
    return load_data()
def search_employee_by_id(emp_id):
    return [emp for emp in load_data() if emp["id"] == emp_id]
def search_employee_by_name(name):
    return [emp for emp in load_data() if name.lower() in emp["name"].lower()]
def sort_employees_by_key(key):
    return sorted(load_data(), key=lambda x: str(x.get(key, "")).lower())
def update_employee(emp_id, updated_fields):
    data = load_data()
    for emp in data:
        if emp["id"] == emp_id:
            emp.update(updated_fields)
            save_data(data)
            return True
    return False
def delete_employee(emp_id):
    data = load_data()
    new_data = [emp for emp in data if emp["id"] != emp_id]
    save_data(new_data)
    return len(data) != len(new_data)
def generate_next_id():
    data = load_data()
    if not data:
        return "EMP001"
    ids = [int(emp["id"][3:]) for emp in data if emp["id"].startswith("EMP")]
    next_id = max(ids, default=0) + 1
    return f"EMP{next_id:03d}"
def get_departments():
    return sorted(set(emp["department"] for emp in load_data() if emp.get("department")))
def get_modes():
    return sorted(set(emp["mode"] for emp in load_data() if emp.get("mode")))