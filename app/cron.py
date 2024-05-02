from django_cron import CronJobBase, Schedule
from dimpro.management.commands.updatedb import update

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 5 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        try:
            print("Updatedb starting in 5 minutes.")
            update()   # update database
            print("Database updated! :D")
        except Exception as e:
            print(f"Attempt to update database failed D: ! {e}")