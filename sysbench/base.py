from abc import ABC, abstractmethod
import argparse
import logging
import os
import subprocess
from enum import Enum
from params import Params

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Command(str, Enum):
    Prepare = "prepare"
    Run = "run"

class BaseSysbench(ABC):
    def __init__(self):
        self.params = Params()

        parser = argparse.ArgumentParser()
        parser.add_argument("-t", "--test", dest="test_name", required=True)
        
        self.args = parser.parse_args()
        self.test_name = self.args.test_name

        t = self.test_name
        p = self.params
        self.flags = [
            # infrastructure (env)
            f"--pgsql-host={os.getenv('DB_HOST')}",
            f"--pgsql-user={os.getenv('DB_USER')}",
            f"--pgsql-password={os.getenv('DB_PASSWORD')}",
            f"--pgsql-db={os.getenv('DB_NAME')}",
            "--db-driver=pgsql",
            # test tuning (params volume with defaults)
            f"--threads={p.get(t, 'threads', '8')}",
            f"--tables={p.get(t, 'tables', '1')}",
            f"--table-size={p.get(t, 'table_size', '10000')}",
            f"--time={p.get(t, 'time', '60')}",
            f"--report-interval={p.get(t, 'report_interval', '1')}",
        ]

    def execute(self, command: Command) -> str:
        """
        Executes a sysbench command as a subprocess.
        """
        cmd = ["sysbench"] + self.flags + [self.test_name, command.value]
        
        logging.info(f"Invoking sysbench {command.value} for {self.test_name}")
        
        try:
            subprocess.run(
                cmd,
                text=True, 
                check=True
            )
        except subprocess.CalledProcessError as e:
            # sysbench often puts specific DB errors in stderr (e.g., connection refused)
            logging.error(f"Sysbench {command.value} failed: {e.stderr.strip()}")
            raise

    def query(self, sql: str):
        """
        Executes maintenance SQL directly on the target database.
        
        Used for Percona-style preparation steps (VACUUM, ANALYZE, CHECKPOINT)
        to ensure the DB state is optimized before the benchmark 'run' begins.
        """
        logging.info(f"Executing maintenance SQL: {sql}")
        # Note: Implement using a pg-client or psycopg2 to ensure the DB 
        # actually receives and completes the command.

    @abstractmethod
    def run_task(self):
        """
        Defines the execution policy for a specific benchmark lifecycle.
        
        Concrete implementations must orchestrate the sequence of setup, 
        sysbench actions, and database maintenance required for the task.
        """
        pass