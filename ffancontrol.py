#!/usr/bin/env python3
import logging
from pathlib import Path
from typing import Final


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        # logging.FileHandler("/var/log/ffancontrol.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Пути к системным файлам
FAN_CONTROL_PATH: Final[Path] = Path('/proc/acpi/ibm/fan')
CPU_TEMP_PATH: Final[Path] = Path('/sys/class/thermal/thermal_zone0/temp')


def read_cpu_temperature() -> float:
    """Читает температуру процессора в градусах Цельсия."""
    with CPU_TEMP_PATH.open("r") as f:
        temp_milli = int(f.read().strip())
        return temp_milli / 1000.0


def set_fan_mode(mode: str) -> None:
    """
    Устанавливает режим работы вентилятора.

    Args:
        mode: 'auto' для автоматического управления, числа 1..7 для ручного
    """
    with FAN_CONTROL_PATH.open("w") as f:
        f.write(f"level {mode}")


def get_fan_level(temp: float) -> str:
    """
    Определяет уровень вентилятора на основе температуры.

    Args:
        temp: Текущая температура CPU в градусах Цельсия

    Returns:
        Строка с режимом вентилятора ('auto')
    """
    match temp:
        case num if num < 30:
            return "2"
        case num if num in range(30, 45):
            return "4"
        case num if num in range(45, 60):
            return "6"
        case num if num >= 60:
            return "7"
        case _:
            return "auto"


def main():
    """Основной цикл программы."""
    # Проверка наличия необходимых файлов
    if not FAN_CONTROL_PATH.exists():
        logger.error(f"Файл управления вентилятором не найден: {FAN_CONTROL_PATH}")
        return 1

    if not CPU_TEMP_PATH.exists():
        logger.error(f"Файл температуры CPU не найден: {CPU_TEMP_PATH}")
        return 1

    try:
        # Читаем температуру CPU
        temp = read_cpu_temperature()
        logger.info(f"Температура CPU: {temp:.1f}°C")
    except Exception as e:
        logger.exception("Не удалось прочитать температуру CPU", e)
        return 1

    try:
        # Определяем необходимый режим вентилятора
        fan_mode = get_fan_level(temp)

        # Устанавливаем режим
        set_fan_mode(fan_mode)
        logger.info(f"Режим вентилятора установлен: {fan_mode}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
