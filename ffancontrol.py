#!/usr/bin/env python3
import logging
from pathlib import Path
from time import sleep
from typing import Final


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        # logging.FileHandler("/var/log/ffancontrol.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# System file paths
FAN_CONTROL_PATH: Final[Path] = Path('/proc/acpi/ibm/fan')


def read_cpu_temperature() -> float:
    """Reads CPU temperature in degrees Celsius."""
    sensors_paths = Path('/sys/class/thermal/').glob('thermal_zone*')

    for sensor in sensors_paths:
        if (sensor / 'type').read_text().startswith('TCPU'):
            values = []
            for x in range(25):
                values.append(int((sensor / 'temp').read_text()))
                sleep(0.02)
            return sum(values) / 25 / 1000.0
    return 0.0


def set_fan_mode(mode: str) -> None:
    """
    Sets fan operation mode.

    Args:
        mode: 'auto' for automatic control, numbers 1..7 for manual control
    """
    with FAN_CONTROL_PATH.open("w") as f:
        f.write(f"level {mode}")


def get_fan_level(temp: float) -> str:
    """
    Determines fan level based on temperature.

    Args:
        temp: Current CPU temperature in degrees Celsius

    Returns:
        String with fan mode ('auto')
    """
    match temp:
        case num if num < 35:
            return "3"
        case num if num <= 35:
            return "4"
        case num if num <= 55:
            return "5"
        case num if num <= 65:
            return "6"
        case num if num > 65:
            return "7"
        case _:
            return "auto"


def main():
    """Main program."""
    # Check for required files
    if not FAN_CONTROL_PATH.exists():
        logger.error(f"Fan control file not found: {FAN_CONTROL_PATH}")
        return 1

    try:
        # Read CPU temperature
        temp = read_cpu_temperature()
        logger.info(f"CPU temperature: {temp:.1f}°C")
    except Exception as e:
        logger.exception("Failed to read CPU temperature", e)
        return 1

    try:
        # Determine required fan mode
        fan_mode = get_fan_level(temp)

        # Set fan mode
        set_fan_mode(fan_mode)
        logger.info(f"Fan mode set: {fan_mode}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
