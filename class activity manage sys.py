import os
import json

# 数据存储结构
students = []
classes = []
credentials = {}  # 添加账号和密码本

# 用户信息文件路径
user_info_file = "user_info.json"

# 检查用户信息文件是否存在，如果存在则加载
if os.path.exists(user_info_file):
    with open(user_info_file, "r") as file:
        user_data = json.load(file)
        users = user_data.get("users", [])
        credentials = user_data.get("credentials", {})
else:
    # 如果文件不存在，创建一个空的用户列表
    users = []

# 学生信息管理
def add_student():
    student = {}
    student["姓名"] = input("请输入学生姓名: ")
    student["性别"] = input("请输入学生性别: ")
    student["出生日期"] = input("请输入学生出生日期(YYYY-MM-DD): ")
    student["联系方式"] = input("请输入学生联系方式: ")

    # 添加班级录入
    student_class = input("请输入学生所在班级: ")
    if student_class not in classes:
        create_class(student_class)

    student["班级"] = student_class

    students.append(student)
    print("学生信息添加成功!")

    # 保存学生信息到班级文件
    add_student_to_class(student, student_class)

def delete_student():
    name_to_delete = input("请输入要删除的学生姓名: ")
    found = False

    for student in students:
        if student["姓名"] == name_to_delete:
            students.remove(student)
            found = True
            print(f"{name_to_delete} 的信息已删除")
            break

    if not found:
        print(f"找不到姓名为 {name_to_delete} 的学生信息")

def modify_student():
    name_to_modify = input("请输入要修改的学生姓名: ")
    found = False

    for student in students:
        if student["姓名"] == name_to_modify:
            print("请选择要修改的信息项:")
            print("1. 姓名")
            print("2. 性别")
            print("3. 出生日期")
            print("4. 联系方式")
            print("5. 班级")
            choice = input("请输入选项: ")
            new_value = input("请输入新的值: ")

            if choice == "1":
                student["姓名"] = new_value
            elif choice == "2":
                student["性别"] = new_value
            elif choice == "3":
                student["出生日期"] = new_value
            elif choice == "4":
                student["联系方式"] = new_value
            elif choice == "5":
                if new_value not in classes:
                    create_class(new_value)
                student["班级"] = new_value

            found = True
            print("学生信息修改成功!")
            break

    if not found:
        print(f"找不到姓名为 {name_to_modify} 的学生信息")

def query_student():
    name_to_query = input("请输入要查询的学生姓名: ")
    found = False

    for student in students:
        if student["姓名"] == name_to_query:
            print("学生信息如下:")
            for key, value in student.items():
                print(f"{key}: {value}")
            found = True
            break

    if not found:
        print(f"找不到姓名为 {name_to_query} 的学生信息")

# 创建班级
def create_class(class_name):
    classes.append(class_name)
    print(f"班级 {class_name} 添加成功!")

    # 创建对应的班级文件
    class_info_file = get_class_info_file(class_name)
    with open(class_info_file, "w") as file:
        class_data = {
            "students": []
        }
        json.dump(class_data, file, indent=4)

# 获取班级文件路径
def get_class_info_file(class_name):
    return f"{class_name}_info.json"

# 添加学生到班级文件中
def add_student_to_class(student, class_name):
    class_info_file = get_class_info_file(class_name)

    if os.path.exists(class_info_file):
        with open(class_info_file, "r") as file:
            class_data = json.load(file)
            class_data["students"].append(student)
            with open(class_info_file, "w") as file:
                json.dump(class_data, file, indent=4)
    else:
        print(f"班级文件 {class_info_file} 不存在，请先创建该班级文件。")

# 用户管理
def register_user():
    username = input("请输入用户名: ")
    password = input("请输入密码: ")
    users.append({"用户名": username, "密码": password})
    user_roles[username] = "普通用户"
    credentials[username] = password  # 将用户名和密码添加到账号和密码本
    print("用户注册成功!")

    # 保存用户信息到文件
    with open(user_info_file, "w") as file:
        user_data = {
            "users": users,
            "credentials": credentials
        }
        json.dump(user_data, file, indent=4)

# 用户登录功能
def login_user():
    username = input("请输入用户名: ")
    password = input("请输入密码: ")
    stored_password = credentials.get(username)  # 获取存储的密码
    if stored_password and stored_password == password:
        print("登录成功!")
        return username

    print("用户名或密码错误")
    return None

def change_password(username):
    new_password = input("请输入新密码: ")
    credentials[username] = new_password  # 更新密码本中的密码
    print("密码修改成功!")

    # 保存用户信息到文件
    with open(user_info_file, "w") as file:
        user_data = {
            "users": users,
            "credentials": credentials
        }
        json.dump(user_data, file, indent=4)

def view_user_info(username):
    print("用户信息如下:")
    print(f"用户名: {username}")

# 主程序
print("欢迎使用班级学生信息管理系统")
logged_in_user = None

while not logged_in_user:
    choice = input("1. 登录\n2. 注册\n请选择: ")

    if choice == "1":
        logged_in_user = login_user()
        if logged_in_user:
            print(f"欢迎您，{logged_in_user}!")
    elif choice == "2":
        register_user()
    else:
        print("无效的选项，请重新选择。")

while True:
    print("\n班级学生信息管理系统")
    print("1. 学生信息管理")
    print("2. 用户管理")
    print("0. 退出")

    choice = input("请输入功能选项: ")

    if choice == "1":
        print("\n学生信息管理")
        print("1. 添加学生信息")
        print("2. 删除学生信息")
        print("3. 修改学生信息")
        print("4. 查询学生信息")
        sub_choice = input("请输入子功能选项: ")

        if sub_choice == "1":
            add_student()
        elif sub_choice == "2":
            delete_student()
        elif sub_choice == "3":
            modify_student()
        elif sub_choice == "4":
            query_student()
        else:
            print("无效的子功能选项，请重新输入。")

    elif choice == "2":
        print("\n用户管理")
        print("1. 用户注册")
        print("2. 修改密码")
        sub_choice = input("请输入子功能选项: ")

        if sub_choice == "1":
            register_user()
        elif sub_choice == "2":
            change_password(logged_in_user)
        else:
            print("无效的子功能选项，请重新输入。")

    elif choice == "0":
        print("感谢使用班级学生信息管理系统，再见!")
        break

    else:
        print("无效的选项，请重新输入。")

# 在退出程序前保存用户信息到文件
with open(user_info_file, "w") as file:
    user_data = {
        "users": users,
        "credentials": credentials
    }
    json.dump(user_data, file, indent=4)
