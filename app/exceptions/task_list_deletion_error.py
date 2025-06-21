class TaskListDeletionError(Exception):
    def __init__(self, message: str = "Cannot Delete a List with Active Tasks."):
        self.message = message
        super().__init__(self.message)
