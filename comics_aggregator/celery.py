import os
from celery import Celery
import lab
from celery.schedules import crontab
from celery.task import periodic_task

app = Celery()

@periodic_task(run_every=10)
def crawl_task():
	lab.crawl()
