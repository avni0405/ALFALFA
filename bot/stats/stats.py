"""Class for generate all statistics."""
import matplotlib.pyplot as plt  # type: ignore
from ...db_config import configure, GLOBAL_PATH  # type: ignore
import os
db = configure()


class Statistics():
    """Generate Statistics."""

    def __init__(self):
        """Initialize class statistics."""
        pass

    def generate_task_stats(self, user_list, path):
        """Generate a bar chart.

        Args:
            user_list (dict): dict object
            db (object): firebase object
            path (str): path to save image

        Returns:
            str: absolute path of  image
        """
        user_task_info = {}
        for key, value in user_list.items():
            print("user_" + str(value))
            count = db.child("user_" + str(value)).child("Count").get().val()
            point = db.child("user_" + str(value)).child("Points").get().val()
            user_task_info.__setitem__(key, (count+point))
        users = list(user_task_info.keys())
        tasks = list(user_task_info.values())

        # creating the bar plot
        plt.bar(users, tasks, color='maroon',
                width=0.4)

        plt.xlabel("Users")
        plt.ylabel("No of task")
        plt.title("Task Statistics.")
        abs_path = os.path.join(path, "images", "tasks.png")
        plt.savefig(abs_path)
        return abs_path

    def generate_user_stats(self, user_info):
        """Generate user stats.

        Args:
            user_info (dict): user information

        Returns:
            [str]: path
        """
        users = list(user_info.keys())
        tasks = list(user_info.values())
        # creating the bar plot
        plt.bar(users, tasks, color='blue',
                width=0.4)

        plt.xlabel("Users")
        plt.ylabel("No of messages")
        plt.title("User Statistics.")
        abs_path = os.path.join(GLOBAL_PATH, "images", "users.png")
        plt.savefig(abs_path)
        return abs_path
