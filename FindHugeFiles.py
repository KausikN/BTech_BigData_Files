import os

def FindHugeFiles(path, max_file_size):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_stats = os.stat(os.path.join(root, name))
            if file_stats.st_size / (1024 * 1024) > max_file_size:
                print(os.path.join(root, name), ":", file_stats.st_size / (1024 * 1024))

FindHugeFiles("E:\UnityProjects\\GameDevPile\\", 75)