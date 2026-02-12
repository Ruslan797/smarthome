from __future__ import annotations

import logging
import re
from typing import Optional, Tuple

from celery import shared_task
from django.db import transaction

from .models import Scenario
from sensors.models import Sensor
from devices.models import Device

logger = logging.getLogger(__name__)


# --- Helpers (вспомогательные функции) ---

_TRIGGER_RE = re.compile(r"temperature\s*>\s*(\d+(?:\.\d+)?)", re.IGNORECASE)


def _parse_temperature_threshold(trigger_condition: str) -> Optional[float]:

    if not trigger_condition:
        return None

    match = _TRIGGER_RE.search(trigger_condition)
    if not match:
        return None

    return float(match.group(1))


def _should_trigger_for_temperature(sensor_value: Optional[float], threshold: float) -> bool:
    """
    Проверка условия 'сенсор > threshold'. Если значения нет — считаем, что не срабатывает.
    """
    if sensor_value is None:
        return False
    return sensor_value > threshold


# --- Main task ---

@shared_task(
    bind=True,
    name="scenarios.check_scenarios",
    autoretry_for=(Exception,),  # если внезапная ошибка (Redis hiccup/DB), Celery сможет повторить
    retry_backoff=True,          # увеличение интервала между повторами
    retry_jitter=True,           # небольшой random, чтобы не долбить ровно по секундам
    retry_kwargs={"max_retries": 3},
)
def check_scenarios(self) -> dict:
    """
    Главная задача проверки сценариев.

    Что возвращаем:
      dict с метриками — удобно смотреть в логах/flower, удобно тестировать.

    Почему так:
      - В проде хочется видеть: сколько сценариев проверили, сколько сработало,
        сколько устройств включили, какие сценарии пропустили и почему.
    """
    logger.info("Scenario check started")

    # 1) Берём активные сценарии одним запросом
    scenarios_qs = Scenario.objects.filter(is_active=True).only("id", "name", "trigger_condition")
    scenarios = list(scenarios_qs)

    if not scenarios:
        logger.info("No active scenarios found")
        return {
            "checked_scenarios": 0,
            "triggered_scenarios": 0,
            "updated_devices": 0,
            "skipped_scenarios": 0,
            "reason": "no_active_scenarios",
        }

    # 2) Готовим сенсоры и устройства заранее (не внутри каждого сценария)
    #    Это уменьшает количество запросов (важно при росте данных).
    temp_sensors_qs = Sensor.objects.filter(sensor_type="temperature").only("id", "name", "value")
    temp_sensors = list(temp_sensors_qs)

    devices_qs = Device.objects.filter(device_type="air_conditioner").only("id", "name", "status")

    checked = 0
    triggered = 0
    skipped = 0

    updated_devices_total = 0

    # 3) Проходим по сценариям и решаем: срабатывать или нет
    for scenario in scenarios:
        checked += 1

        threshold = _parse_temperature_threshold(getattr(scenario, "trigger_condition", ""))
        if threshold is None:
            skipped += 1
            logger.debug(
                "Scenario skipped (unsupported trigger_condition): id=%s name=%s condition=%r",
                scenario.id,
                scenario.name,
                scenario.trigger_condition,
            )
            continue

        # Проверяем сенсоры: если хотя бы один сенсор выше порога — считаем сработало
        triggered_by_sensor: Optional[Tuple[int, str, float]] = None
        for s in temp_sensors:
            if _should_trigger_for_temperature(getattr(s, "value", None), threshold):
                triggered_by_sensor = (s.id, getattr(s, "name", ""), float(s.value))
                break

        if not triggered_by_sensor:
            logger.info(
                "Scenario not triggered: id=%s name=%s threshold=%s",
                scenario.id,
                scenario.name,
                threshold,
            )
            continue

        triggered += 1
        sensor_id, sensor_name, sensor_value = triggered_by_sensor

        # 4) Bulk update устройств
        #    Ставим status=True только там, где сейчас False, чтобы:
        #    - меньше лишних обновлений
        #    - логика была идемпотентной
        with transaction.atomic():
            updated_count = devices_qs.filter(status=False).update(status=True)

        updated_devices_total += updated_count

        logger.warning(
            "Scenario triggered: id=%s name=%s | sensor=%s(%s) value=%s threshold=%s | devices_turned_on=%s",
            scenario.id,
            scenario.name,
            sensor_id,
            sensor_name,
            sensor_value,
            threshold,
            updated_count,
        )

    result = {
        "checked_scenarios": checked,
        "triggered_scenarios": triggered,
        "updated_devices": updated_devices_total,
        "skipped_scenarios": skipped,
    }

    logger.info("Scenario check finished: %s", result)
    return result



