import os
import subprocess

from base import BaseSysbench, Command

class Prepare(BaseSysbench):
    def run_task(self):
        try:        
            stdout = self.execute(Command.Prepare)
            self.log.info(f"tables creation complete: {stdout}")

            self.maintanance()
            self.log.info("vacuum analyze, checkpoint complete")

            self.prewarm()
            self.log.info("prewarm complete")

            self.ctx.db.query("SELECT pg_stat_statements_reset()")
        except Exception as e:
            self.log.error(e)
            raise

    def maintanance(self):
        """
        percona-style benchmark prep - CHECKPOINT, VACUUM ANALYZE.
        """
        workers = os.cpu_count()
        cmd = ["vacuumdb", "-j", str(workers), "-z", "-v", "--dbname", self.ctx.db.dsn]

        self.ctx.db.query("CHECKPOINT")  
        subprocess.run(cmd, check=True, capture_output=True, text=True)

    def prewarm(self):
        result = self.ctx.db.query("SELECT tablename FROM pg_tables WHERE tablename LIKE 'sbtest%'").fetchall()

        self.ctx.logger.info(result)

        for row in result:
            table_name = row["tablename"]

            self.log.info(f"Prewarming {table_name}")
            self.ctx.db.query(f"SELECT pg_prewarm('{table_name}')")



if __name__ == "__main__":
   Prepare.main()