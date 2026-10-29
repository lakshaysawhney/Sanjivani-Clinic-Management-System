from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, ValidationError

IST = ZoneInfo("Asia/Kolkata")
STARTS = ["10:00", "10:45", "11:30", "13:00", "13:45", "14:30", "15:15", "16:00", "16:45", "17:30"]


def now():
    return timezone.localtime(timezone.now(), IST)


def slot_end(day, slot):
    if slot not in range(10):
        raise ValidationError("Choose a valid clinic time slot.")
    return datetime.combine(day, time.fromisoformat(STARTS[slot]), IST) + timedelta(minutes=45)


def month_floor(day, back=0):
    index = day.year * 12 + day.month - 1 - back
    return day.replace(year=index // 12, month=index % 12 + 1, day=1)


def history_scope(user, day):
    back = 1 if user.role == "THERAPIST" else 2
    if user.role != "ADMIN" and day < month_floor(now().date(), back):
        raise PermissionDenied("This date is outside your permitted history window.")


def editable(user, day):
    if user.role == "THERAPIST":
        raise PermissionDenied("Only clinic administration can change appointments.")
    history_scope(user, day)
    if user.role == "RECEPTIONIST" and now() >= datetime.combine(day, time(18), IST):
        raise PermissionDenied("Receptionist corrections close at 6:00 PM on the session date.")


def next_operating_day(day):
    for offset in range(1, 8):
        candidate = day + timedelta(days=offset)
        if candidate.weekday() in settings.OPERATING_DAYS:
            return candidate
    raise ValidationError("No clinic operating days configured.")
