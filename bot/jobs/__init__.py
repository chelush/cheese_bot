from ..bot import scheduler
from . import send_notifications


def setup_jobs():
    # scheduler.add_job(send_notifications.send_notification_sale, "interval", hours=1)
    # scheduler.add_job(send_notifications.send_notification_group, "interval", minutes=30)

    scheduler.add_job(send_notifications.send_notification_sale, "interval", minutes=1)
    scheduler.add_job(send_notifications.send_notification_group, "interval", minutes=2)
