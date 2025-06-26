# app/tasks/send_reminders.py

from datetime import datetime

from celery import Celery
from celery.schedules import crontab

from app.core.config import settings
from app.db.session import SessionLocal
from app.services import email_service
from app import crud, models

# --- Инициализация Celery ---
# Создаем экземпляр Celery, используя URL брокера из настроек.
celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_track_started=True,
)

# --- Настройка расписания (Celery Beat) ---
# Эта функция настраивает периодическую задачу, которая будет запускаться
# автоматически по расписанию.
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Настраивает периодические задачи для Celery Beat.
    """
    # Добавляем задачу `send_scheduled_reminders` в расписание.
    # Она будет запускаться каждую минуту. Для продакшена можно
    # изменить на crontab(hour='*') для ежечасного запуска.
    sender.add_periodic_task(
        crontab(minute='*'),  # Запускать каждую минуту
        send_scheduled_reminders.s(),
        name='check for due capsules every minute'
    )

# --- Определение задачи Celery ---
@celery_app.task
def send_scheduled_reminders():
    """
    Периодическая задача для поиска и отправки "просроченных" капсул.
    """
    print(f"[{datetime.utcnow()}] Запуск задачи: Поиск капсул для отправки...")
    
    # Создаем сессию базы данных для этой задачи
    db = SessionLocal()
    
    due_capsules = []
    try:
        # Получаем все капсулы, у которых подошло время отправки и которые еще не отправлены
        due_capsules = crud.capsule.get_due_capsules(db=db)
        
        if not due_capsules:
            print("Нет капсул для отправки.")
            return "Нет капсул для отправки."

        print(f"Найдено {len(due_capsules)} капсул для отправки.")
        
        for capsule in due_capsules:
            print(f"Отправка капсулы ID: {capsule.id} пользователю ID: {capsule.owner.id}")
            
            # Отправляем email-напоминание
            email_service.send_capsule_reminder(user=capsule.owner, capsule=capsule)
            
            # Помечаем капсулу как отправленную
            capsule.is_sent = True
            db.add(capsule)
        
        # Коммитим все изменения в базе данных
        db.commit()
        print("Все напоминания успешно отправлены и помечены.")

    except Exception as e:
        print(f"Произошла ошибка в задаче send_scheduled_reminders: {e}")
        db.rollback()  # Откатываем изменения в случае ошибки
    finally:
        # Всегда закрываем сессию после выполнения
        db.close()

    return f"Задача завершена. Обработано {len(due_capsules)} капсул."
