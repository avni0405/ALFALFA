"""Class for database operations."""
from ..constant import TASK, USER  # type: ignore
from ...db_config import configure  # type: ignore
db = configure()


class CrudOperations():
    """Perform database operations."""

    def __init__(self):
        """Initialize class."""
        pass

    def add_task(self, userid, task):
        """Add task in firebase.

        Args:
            userid (int): unique id of user
            task (str): task name
        """
        user_id = USER+str(userid)
        try:
            count = db.child(user_id).child("Count").get().val()
            point = db.child(user_id).child("Points").get().val()
            total_task = count + point
            task_title = TASK + str(int(total_task)+1)
            task_obj = {task_title: task, "is_completed": False}
            db.child(user_id).child("Count").set(int(count)+1)
        except Exception as e:
            print(e)
            task_obj = {"Task 1": task, "is_completed": False}
            task_title = "Task 1"
            db.child(user_id).child("Count").set(1)
            db.child(user_id).child("Points").set(0)
        db.child(user_id).child(task_title).set(task_obj)

    def finish_task(self, numbers, user_id):
        """Finish the task.

        Args:
            numbers (int): task number

        Returns:
            int: point
        """
        previous_point = db.child(user_id).child("Points").get().val()
        # Increment point
        db.child(user_id).child("Points").set(previous_point+1)
        rename_task = "completed_" + str(previous_point+1)
        task = db.child(user_id).child(TASK + str(numbers)).get().val()
        update_task = {
            rename_task: task[TASK + str(numbers)], "is_completed": True}
        db.child(user_id).child(rename_task).set(update_task)
        db.child(user_id).child(TASK + str(numbers)).remove()
        # Decrement Count
        previous_count = db.child(user_id).child("Count").get().val()
        db.child(user_id).child("Count").set(previous_count-1)

        point = db.child(user_id).child("Points").get().val()
        return point

    def show_completed_task(self, user_id):
        """Display completed task."""
        point = db.child(user_id).child("Points").get().val()
        task_name = "completed_"
        try:
            loop_range = point
            msg_send = ""
            for task in range(loop_range):
                task_info = db.child(user_id).child(
                    task_name+str(task + 1)).get().val()
                print(task_info)
                check_complete = task_info["is_completed"]
                if check_complete:
                    msg_send += str(task + 1) + ". " + \
                        task_info[task_name+str(task + 1)] + "\n"
            return msg_send
        except Exception as e:
            print(e)
            return "You don't have any completed task"

    def show_outstanding_task(self, user_id):
        """Show outstanding tasks.

        Args:
            user_id (str): user id

        Returns:
            [str]: outstanding task
        """
        total_tasks = db.child(user_id).child("Count").get().val()
        n = 1
        msg_send = ""
        while total_tasks != 0:
            data = db.child(user_id).get().val()

            task_query = "Task " + str(n)
            try:
                print(data[task_query]["is_completed"])
                if not data[task_query]["is_completed"]:
                    msg_send += str(n)+". " + \
                        data[task_query][task_query]+"\n"
                total_tasks -= 1

            except Exception:
                n = n + 1
                continue
            n = n + 1

        return msg_send
