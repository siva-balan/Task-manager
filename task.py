import os
import sys


def readFile(path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            content = file.read().strip()
            if content:
                return content.split("\n")

    return []


def stringify(array):
    string = ""
    for element in array:
        string += (str(element) + "\n")
    
    return string


def writeFile(path, content, append=False):
    if not append: content = stringify(content)
    mode = 'a' if append else 'w'
    with open(path, mode) as file:
        file.write(content)


def add(priority, task):
    if task:
        tasks = readFile("task.txt")
        if priority is not None: tasks.insert(priority, task)
        else: tasks.append(task)

        writeFile("task.txt", tasks)
        return f'Added task: "{task}" with priority {priority}'

    return "Error: Missing tasks string. Nothing added!"


def ls():
    tasks = readFile("task.txt")

    messages = ""
    for i, message in enumerate(tasks):
        messages += f"{i + 1}. {message} [{i + 1}]\n"

    return messages.strip() if messages else "There are no pending tasks!"


def delete(idx):
    if idx is None:
        return "Error: Missing NUMBER for deleting tasks."

    tasks = readFile("task.txt")
    if idx < 1 or idx > len(tasks):
        return f"Error: task with index #{idx} does not exist. Nothing deleted."

    tasks.pop(idx - 1)
    writeFile("task.txt", tasks)
    return f"Deleted task #{idx}"


def done(idx):
    if idx is None:
        return "Error: Missing NUMBER for marking tasks as done."

    pending_tasks = readFile("task.txt")
    if idx < 1 or idx > len(pending_tasks):
        return f"Error: no incomplete item with index #{idx} exists."

    completed_task = pending_tasks.pop(idx - 1)
    writeFile("completed.txt", f"{completed_task}\n", True)
    writeFile("task.txt", pending_tasks)
    return f"Marked item as done."


def report():
    pending_tasks = readFile("task.txt")
    completed_tasks = readFile("completed.txt")

    report = f"Pending : {len(pending_tasks)}\n"
    report += ls()
    report += "\n\n"
    
    report += f"Completed : {len(completed_tasks)}\n"
    for i, task in enumerate(completed_tasks):
        report += f"{i+1}. {task}\n"


    return report.strip()


def help():
    return '''Usage :-
$ ./task add 2 hello world     # Add a new item with priority 2 and text "hello world" to the list
$ ./task ls                    # Show incomplete priority list items sorted by priority in ascending order
$ ./task del NUMBER   # Delete the incomplete item with the given priority number
$ ./task done NUMBER  # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ ./task help                  # Show usage
$ ./task report                # Statistics'''


def route(action, params):
    if action == "add":
        priority = int(params[0]) if len(params) > 1 else None
        task = params[1] if len(params) > 1 else params[0] if len(params) > 0 else None
        return add(priority, task)
    elif action == "ls":
        return ls()
    elif action == "del":
        number = int(params[0]) if len(params) else None
        return delete(number)
    elif action == "done":
        number = int(params[0]) if len(params) else None
        return done(number)
    elif action == "report":
        return report()

    return help()


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "help"
    params = sys.argv[2:]

    result = route(action, params)
    print(result)
