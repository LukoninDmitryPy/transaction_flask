# tasks.py
from celery import Celery
from models import db, Transaction, User
from datetime import datetime, timedelta
from celery.schedules import crontab
import requests
import logging
from app import app as flask_app

logger = logging.getLogger('celery')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

celery = Celery('transactions', 
                broker='amqp://guest:guest@rabbitmq:5672//',
                include=['tasks'])

class Config:
    broker_url = 'amqp://guest:guest@rabbitmq:5672//'
    imports = ('tasks',)
    task_serializer = 'json'
    accept_content = ['json']
    result_serializer = 'json'
    timezone = 'UTC'
    enable_utc = True
    beat_schedule = {
        'check-pending-transactions': {
            'task': 'tasks.check_transactions',
            'schedule': crontab(minute='*'),
        },
    }

celery.config_from_object(Config)

@celery.task(name='tasks.check_transactions')
def check_transactions():
    with flask_app.app_context():
        try:
            transactions = Transaction.query.filter_by(status='pending').all()
            for transaction in transactions:
                if datetime.now() - transaction.created_at > timedelta(minutes=15):
                    transaction.status = 'expired'
                    db.session.commit()
                    
                    user = User.query.get(transaction.user_id)
                    if user and user.webhook_url:
                        try:
                            requests.post(user.webhook_url, 
                                        json={
                                            'id': transaction.id, 
                                            'status': transaction.status
                                        },
                                        timeout=5)
                        except requests.exceptions.RequestException as e:
                            print(f"Webhook delivery failed: {e}")
            
            return "Transactions checked successfully"
        except Exception as e:
            print(f"Error checking transactions: {e}")
            return str(e)