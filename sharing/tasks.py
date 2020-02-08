from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from sharing.models import Access, Payments, Rents
from django.utils import timezone
from rents.modules import bitx

logger = get_task_logger(__name__)

@task(name="start_renta_task")
def start_renta_task(renta,user):
    
    logger.info("start_renta_task")
    return True

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="check_current_rents",
    ignore_result=True
)
def check_current_rents():
    soap = bitx.Soap()
    data = soap.getAll()
    for i in data:
        r = soap.parse_data(i)
    logger.info("Checkin renta....")
    