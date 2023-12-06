# UserScript Documentation

UserScript is a command-line utility for managing user accounts. It provides various commands to perform operations on user data, including printing account details, finding similar children by age, and more.

# Installation

## Prerequisites

- Python 3.10
- pipenv (Python package manager) (not Compulsory)

## Setting up the Environment

It is recommended to use `pipenv` to manage project dependencies. Follow these steps:

1. Install Python 3.10 from the [official Python website](https://www.python.org/downloads/release).

2. Open a terminal and navigate to your project folder.

3. Create a virtual environment with `pipenv`:

   ```bash
   pipenv install --python 3.10
   pipenv shell

   ```

```bash
pip install python3.10
# pip install db-sqlite3
```

## Usage

Run the script with the desired command. Below is an example of usage:

```bash
python script.py <command> --login "<login>" --password "<password>"
```

Replace `script.py` with the actual script filename.

## Available Commands

### 1. `print-all-accounts`

Prints the total number of valid accounts.

```bash
python script.py print-all-accounts --login "<login>" --password "<password>"
```

### 2. `print-oldest-account`

Prints information about the account with the longest existence.

```bash
python script.py print-oldest-account --login "<login>" --password "<password>"
```

### 3. `group-by-age`

Groups children by age and displays relevant information.

```bash
python script.py group-by-age --login "<login>" --password "<password>"
```

### 4. `print-children`

Displays information about the user's children. Sorts children alphabetically by name.

```bash
python script.py print-children --login "<login>" --password "<password>"
```

### 5. `find-similar-children-by-age`

Finds users with children of the same age as at least one of their own children.

```bash
python script.py find-similar-children-by-age --login "<login>" --password "<password>"
```

<!-- ## Creating SQLite Database

To create an SQLite database and use it for the rest of the tasks, use the following command:

```bash
python script.py create_database --login <login> --password <password>
```

This command creates the database file `user_data.db` and populates it with user data. -->

**Note:** Replace `<login>` and `<password>` with your actual login credentials , and remember to use `" "`.
**Note:** There are two file one is `functions.py` ans `script.py` and remember that `data_folder` give proper name of main folder.

## Example Usage

```bash
python script.py print-all-accounts --login "<login>" --password "<password>"

python script.py find-similar-children-by-age --login "victoriataylor@example.net" --password "+Wu@Pu)y(0"

python script.py print-all-accounts --login "joshua75@example.org" --password "&T)u+DAa31"

python script.py print-oldest-account --login "joshua75@example.org"  --password "&T)u+DAa31"

python script.py group-by-age --login "joshua75@example.org"  --password "&T)u+DAa31"
```

## Additional Notes

- Make sure to replace `<login>` and `<password>` with your actual login credentials.
- Some commands may require admin access. Ensure that your account has the necessary permissions.

Feel free to explore other commands and tailor them to your specific use case.
