# Importing necessary modules
from crontab import CronTab
import subprocess

# Creating new cron tab
cron = CronTab(user='Hemchandhar')

# Setting the Python path and script path for execution
python_path = 'C:\Python39\python.exe'
script_path = 'H:\Assessments and Personal Projects\Securin Assessment\Python Task\app.py'

# Adding a new cron job to trigger the script
job = cron.new(command=f'{python_path} {script_path} sync_cves')
job.setall('0 0 * * *')  # Run at midnight every day

# Writing the new cron tab
cron.write()
