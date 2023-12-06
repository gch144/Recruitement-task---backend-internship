import argparse
from functions import (
    import_data_recursive,
    remove_duplicates,
    write_to_json,
)


class UserScript:
    ADMIN_ROLES = {"admin"}

    def __init__(self, dataset):
        self.dataset = dataset
        self.user = None

    def validate_login(self, login, password):
        user = self.find_user_by_login(login)
        print(f"Provided login: {login}, Provided password: {password}")
        # print(f"Found user: {user}")
        if user and user["password"] == password:
            self.user = user
            self.login = login
            return True
        return False

    def has_admin_access(self):
        # user = self.get_user_by_login()
        # print(self.user["role"])
        return self.user and self.user["role"] in self.ADMIN_ROLES

    def print_all_accounts(self):
        if self.has_admin_access():
            print(len(self.dataset))
        else:
            print("Access denied.")

    def print_oldest_account(self):
        if self.has_admin_access():
            oldest_account = max(self.dataset, key=lambda x: x["created_at"])
            print(f"Oldest account:")
            print(f"name: {oldest_account['firstname']}")
            print(f"email_address: {oldest_account['email']}")
            print(f"created_at: {oldest_account['created_at']}")
        else:
            print("Access denied.")

    def group_by_age(self):
        if self.has_admin_access():
            children_by_age = {}
            for user in self.dataset:
                for child in user.get("children", []):
                    age = child.get("age")
                    if age:
                        if age not in children_by_age:
                            children_by_age[age] = {"count": 0, "names": set()}
                        children_by_age[age]["count"] += 1
                        children_by_age[age]["names"].add(child["name"])

            sorted_by_age = sorted(children_by_age.items(), key=lambda x: x[1]["count"])
            for age, children_info in sorted_by_age:
                children_str = ", ".join(children_info["names"])
                print(
                    f"age: {age}, count: {children_info['count']}, names: {children_str}"
                )
        else:
            print("Access denied. Admin role required.")

    def print_children(self):
        # Display information about the user's children. Sort children alphabetically by name.
        user = self.get_user_by_login()
        if user:
            children = sorted(user.get("children", []), key=lambda x: x["name"])
            if len(children) == 0:
                print("User has no children")
            else:
                for child in children:
                    print(f"{child['name']}, {child['age']}")

    def find_similar_children_by_age(self):
        # Find users with children of the same age as at least one own child
        user = self.get_user_by_login()
        if user:
            user_children = user.get("children", [])
            for other_user in self.dataset:
                if other_user != user:
                    matching_children = [
                        f"{child['name']}, {child['age']}"
                        for child in other_user.get("children", [])
                        if any(
                            child["age"] == user_child["age"]
                            for user_child in user_children
                        )
                    ]
                    if matching_children:
                        print(
                            f"{other_user['firstname']}, {other_user['telephone_number']}: "
                            f"{'; '.join(matching_children)}"
                        )

    def get_user_by_login(self):
        self.user = self.find_user_by_login(self.login)
        return self.user

    def find_user_by_login(self, login):
        for user in self.dataset:
            if user["email"] == login or user["telephone_number"] == login:
                return user
        return None

    def execute_command(self, command_name):
        if command_name == "print-all-accounts":
            self.print_all_accounts()
        elif command_name == "print-oldest-account":
            self.print_oldest_account()
        elif command_name == "group-by-age":
            self.group_by_age()
        elif command_name == "print-children":
            self.print_children()
        elif command_name == "find-similar-children-by-age":
            self.find_similar_children_by_age()
        else:
            print(f"Invalid command: {command_name}")


if __name__ == "__main__":
    # Example usage
    data_folder = "data"
    output_json_file = "Result.json"

    merged_dataset = []

    import_data_recursive(data_folder, merged_dataset)

    merged_dataset = remove_duplicates(merged_dataset)

    write_to_json(merged_dataset, output_json_file)

    user_script = UserScript(merged_dataset)

    parser = argparse.ArgumentParser(description="User Script")
    parser.add_argument(
        "--login", required=True, help="User login (email or telephone number)"
    )
    parser.add_argument("--password", required=True, help="User password")
    args, unknown_args = parser.parse_known_args()

    # Validate login credentials
    if user_script.validate_login(args.login, args.password):
        if unknown_args:
            user_script.execute_command(unknown_args[0])
        else:
            print("No command provided.")
    else:
        print("Invalid Login")
