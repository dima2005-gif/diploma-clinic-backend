from datetime import datetime, timedelta
from main.models import Work_Schedule, Prescribed_Service

SLOT_DURATION = 15


def get_available_slots(doctor, date):
    days_map = {
        0: "Понеділок",
        1: "Вівторок",
        2: "Середа",
        3: "Четвер",
        4: "П'ятниця",
        5: "Субота",
        6: "Неділя",
    }
    day_name = days_map[date.weekday()]

    schedule = Work_Schedule.objects.filter(
        employee=doctor, day_of_week=day_name
    ).first()

    if not schedule:
        return []

    slots = []
    current = datetime.combine(date, schedule.start_time)
    end = datetime.combine(date, schedule.end_time)

    while current + timedelta(minutes=SLOT_DURATION) <= end:
        is_busy = Prescribed_Service.objects.filter(
            doctor=doctor, date_prescribed=current
        ).exists()

        if not is_busy:
            slots.append(current.strftime("%H:%M"))

        current += timedelta(minutes=SLOT_DURATION)
    return slots
