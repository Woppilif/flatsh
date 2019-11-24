from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from sharing.models import Access, Payments, Rents
from django.utils import timezone

logger = get_task_logger(__name__)

@task(name="start_renta_task")
def start_renta_task(renta,user):
    print(renta,user)
    """sends an email when feedback form is filled successfully"""
    depo = Payments.paym.createDeposit(renta,user)
    print(depo)
    full = Payments.paym.createFull(renta,user)
    print(full)
    logger.info("start_renta_task")
    return True

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="check_current_rents",
    ignore_result=True
)
def check_current_rents():
    rents = Rents.objects.filter(start__gte=timezone.now(),booking__lte=timezone.now(),status=True,paid=False)

    for i in rents:
        if i.paid is False:
            depo = Payments.paym.createDeposit(i.pk,i.rentor.pk)
            print(depo)
            full = Payments.paym.createFull(i.pk,i.rentor.pk)
            print(full)
            logger.info("Renta started. Reason: BOOKING TIME IS UP! {0}".format(i.pk))

    acc_list = Access.objects.filter(end__lte=timezone.now(),renta__status=True,stype=False)
    for i in acc_list:
        if i.stype is False and i.renta.paid is False:
            depo = Payments.paym.createDeposit(i.renta.pk,i.user.pk)
            print(depo)
            full = Payments.paym.createFull(i.renta.pk,i.user.pk)
            print(full)

            logger.info("Renta started. Reason: no action!")
        
    logger.info("Checkin renta....")
    