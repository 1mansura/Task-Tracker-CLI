import cmd
from tasks import TaskManager


class TaskCLI(cmd.Cmd):
    intro = (
        "Welcome to Task Tracker CLI!\n"
        "Available Commands:\n"
        " add \"description\"\n"
        " update <task_id> \"new_description\"\n"
        " delete <task_id>\n"
        " mark_in_progress <task_id>\n"
        " mark_done <task_id>\n"
        " list\n"
        " list todo\n"
        " list in_progress\n"
        " list done\n"
        " help\n"
        " exit\n"
    )
    prompt = "task-cli> "

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = TaskManager()
        self.valid_statuses = ["todo", "in_progress", "done"]

    def do_list(self, arg):
        """List all tasks or tasks with a specific status."""
        arg = arg.strip().replace("-", "_")

        # Check if the input is empty or not a valid status
        if arg and arg not in self.valid_statuses:
            print(f"Error: '{arg}' is not a valid status or command.")
            return

        if arg in self.valid_statuses:
            tasks = self.manager.list_tasks(arg)
        else:
            tasks = self.manager.list_tasks()

        if tasks:
            print(tasks)
        else:
            print("No tasks available.")

    def do_add(self, arg):
        """Add a new task."""
        arg = arg.strip()
        if arg:
            print(self.manager.add_task(arg.strip('"')))
        else:
            print("Usage: add \"description\"")

    def do_update(self, arg):
        """Update an existing task."""
        try:
            task_id, new_description = arg.split(maxsplit=1)
            task_id = int(task_id)
            print(self.manager.update_task(task_id, new_description.strip('"')))
        except ValueError:
            print("Usage: update <task_id> \"new_description\"")
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_delete(self, arg):
        """Delete an existing task."""
        try:
            task_id = int(arg.strip())
            print(self.manager.delete_task(task_id))
        except ValueError:
            print("Usage: delete <task_id>")

    def do_mark_in_progress(self, arg):
        """Mark a task as in-progress."""
        try:
            task_id = int(arg.strip())
            response = self.manager.mark_in_progress(task_id)
            if response:
                print(response)
            else:
                print(f"Task {task_id} not found.")
        except ValueError:
            print("Usage: mark_in_progress <task_id>")

    def do_mark_done(self, arg):
        """Mark a task as done."""
        try:
            task_id = int(arg.strip())
            response = self.manager.mark_done(task_id)
            if response:
                print(response)
            else:
                print(f"Task {task_id} not found.")
        except ValueError:
            print("Usage: mark_done <task_id>")

    def do_help(self, arg):
        """Show help information."""
        print(self.intro)

    def do_exit(self, arg):
        """Exit the CLI."""
        print("Exiting Task Tracker CLI. Goodbye!")
        return True

    def emptyline(self):
        """Do nothing on empty input line."""
        pass

    # Override the default method to handle invalid commands
    def default(self, line):
        """Handle unrecognized commands."""
        print(f"Error: '{line}' is not a valid command. Type 'help' to see available commands.")

    # Redefine aliases for better UX
    def do_mark_inprogress(self, arg):
        self.do_mark_in_progress(arg)


def start_cli():
    TaskCLI().cmdloop()


if __name__ == "__main__":
    start_cli()
