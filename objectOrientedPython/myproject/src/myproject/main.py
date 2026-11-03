import typer

app = typer.Typer()

# Import the Typer library
# Typer is used to create command-line applications (CLI)
import typer

# Step 1: Create a Typer application object
# This object manages all the commands in the application
app = typer.Typer()

# Step 2: Create an "add" command
# Users can add a task from the command line
@app.command()
def add(task: str):
    print(f"Task added: {task}")

# Example:
# python main.py add "Learn Python"

# Output:
# Task added: Learn Python


# Step 3: Create a "list" command
# Displays all available tasks
@app.command()
def list():
    print("1. Learn Python")
    print("2. Learn Typer")

# Example:
# python main.py list

# Output:
# 1. Learn Python
# 2. Learn Typer


# Step 4: Create a "delete" command
# Removes a task using its ID
@app.command()
def delete(task_id: int):
    print(f"Deleted task {task_id}")

# Example:
# python main.py delete 1

# Output:
# Deleted task 1


# Step 5: Start the Typer application
# This allows Typer to listen for and process commands
if __name__ == "__main__":
    app()