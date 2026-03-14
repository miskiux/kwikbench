from base import BaseSysbench

class Run(BaseSysbench):
    def run_task(self):
        try:        
            self.log.info("Running test")
        except Exception as e:
            self.log.error(e)

if __name__ == "__main__":
   Run.main()