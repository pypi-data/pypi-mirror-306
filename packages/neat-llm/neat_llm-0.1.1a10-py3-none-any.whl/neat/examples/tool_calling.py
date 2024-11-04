"""
This module implements a weather assistant.
It provides a synchronous interface for fetching weather information and generating clothing recommendations based on weather conditions.
"""

import random
from typing import List

from neat import neat
from pydantic import BaseModel, Field


class WeatherInfo(BaseModel):
    """Represents weather information for a specific location.

    Attributes:
        temperature (float): Current temperature in Celsius
        conditions (str): Brief description of current weather conditions
    """

    temperature: float = Field(..., description="Current temperature in Celsius")
    conditions: str = Field(..., description="Brief description of weather conditions")


WEATHER_CONDITIONS = ["Sunny", "Cloudy", "Rainy", "Windy", "Snowy"]


@neat.tool()
def get_weather(location: str) -> WeatherInfo:
    """Fetch current weather information for a given location.

    Args:
        location (str): Name of the location to get weather for

    Returns:
        WeatherInfo: Weather information including temperature and conditions
    """
    temp = round(random.uniform(-5, 35), 1)
    conditions = random.choice(WEATHER_CONDITIONS)
    return WeatherInfo(temperature=temp, conditions=conditions)


@neat.lm(tools=[get_weather], max_iterations=2)
def weather_assistant() -> List:
    """Create a weather assistant interaction.

    Returns:
        List: List of system and user messages for the LLM
    """
    return [
        neat.system(
            """You are a helpful weather assistant. Use the get_weather tool to check the weather for specific locations."""
        ),
        neat.user("What's the weather like in Paris today?"),
    ]


def main() -> None:
    """Run example of the weather assistant."""
    result = weather_assistant()
    print(result)


if __name__ == "__main__":
    main()
