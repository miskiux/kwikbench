import os
import subprocess

from base import BaseSysbench, Command

class Prepare(BaseSysbench):
    def run_task(self):
        try:        
            self.execute(Command.Prepare)
            self.log.info("Tables created successfully.")

            self.log.info("Running maintanance and reseting pg_stat_statements")
            self.maintanance()
        except Exception as e:
            self.log.error(e)
            raise

    def maintanance(self):
        """
        Percona-style benchmark prep steps (CHECKPOINT, VACUUM ANALYZE, RESET PGSS)
        to ensure the DB state is optimized before the benchmark.
        """
        workers = os.cpu_count()
        cmd = ["vacuumdb", "-j", str(workers), "-z", "-v", "--dbname", self.ctx.db.dsn]

        self.ctx.db.query("CHECKPOINT")  
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        self.ctx.db.query("SELECT pg_stat_statements_reset()")
    

if __name__ == "__main__":
   Prepare.main()