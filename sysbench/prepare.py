from base import BaseSysbench, Command
import traceback
import sys

class Prepare(BaseSysbench):
    def run_task(self):
        print(f"Prepare task for {self.test_name}...")
        self.execute(Command.Prepare)
        self.query("VACUUM ANALYZE;")

if __name__ == "__main__":
    try:
        app = Prepare()
        app.run_task()
    except Exception as e:
        traceback.print_exc() 
        sys.exit(1)