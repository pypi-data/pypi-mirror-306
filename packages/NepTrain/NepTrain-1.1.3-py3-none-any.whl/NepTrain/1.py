from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class SimpleHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'File {event.src_path} has been modified')

if __name__ == "__main__":
    event_handler = SimpleHandler()
    observer = Observer()
    observer.schedule(event_handler, path='./io/nep/', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()