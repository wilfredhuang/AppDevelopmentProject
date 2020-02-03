from storageManager_Hieu import StorageManager

db = None


def init():
    global db
    db = StorageManager()


def reset():
    StorageManager.reset()


