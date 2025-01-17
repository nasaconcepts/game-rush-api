import random
import uuid
from api.modelEntity.builder.property_config import default_score

def generate_unique_id(length=8):
    """
    Generate a unique alphanumeric ID.

    :param length: The desired length of the ID (default is 8).
    :return: A unique alphanumeric ID as a string.
    """
    # Generate a UUID and convert it to a string without hyphens
    unique_id = str(uuid.uuid4()).replace("-", "")

    # Randomly shuffle the characters to ensure better randomness
    shuffled_id = ''.join(random.sample(unique_id, len(unique_id)))

    # Limit the ID to the specified length
    return shuffled_id[:length]
# This function calculates the point accrued by player and it considers speed as well
def calculate_point(score_point_name: str, time_interval: int, time_taken: int):
    score = default_score[score_point_name]
    if time_taken == 0:
        return score

    nominal_time = time_taken if time_interval > time_taken else time_interval
    return int(score + (time_interval - nominal_time) / time_interval * score)


