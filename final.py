import os
import json
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pprint import pprint
import nltk
import json
nltk.download('stopwords')
from Questgen import main

json_file_to_monitor = "data.json"
json_file_path = "data.json"
compile_command = "python"
json_dump_file = "dump.json"

# Function to compile and run the program
def compile_and_run():
    try:
        subprocess.run([compile_command, __file__])
        
    except Exception as e:
        print(f"Error recompiling: {e}")


def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

# Initial timestamp of the JSON file
initial_timestamp = os.path.getmtime(json_file_to_monitor)

class JSONFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == os.path.abspath(json_file_to_monitor):
            print(f"Changes detected in {json_file_to_monitor}. Recompiling and running...")
            compile_and_run()

if __name__ == "__main__":
    # Start monitoring the JSON file
    event_handler = JSONFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    qe = main.BoolQGen()
    json_file_path = "data.json"
    with open(json_file_path , 'r') as json_file:
        data1 = json.load(json_file)
    output = qe.predict_boolq(data1)
    with open(json_dump_file , 'w') as dum_file:
        json.dump(output , dum_file )



    pprint(output)
    try:
        while True:
            # Check for changes in the JSON file
            current_timestamp = os.path.getmtime(json_file_to_monitor)
            if current_timestamp != initial_timestamp:
                print(f"Changes detected in {json_file_to_monitor}. Recompiling and running...")
                initial_timestamp = current_timestamp
                compile_and_run()

            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
