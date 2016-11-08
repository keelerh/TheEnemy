import numpy


def calculate_bounds(user_data):
    """Calculates the upper and lower bound thresholds for attentiveness
       Args:
           user_data(list(list)): an array with the arrays of data collected on
                                  each user: includes, mean_distance,
                                  stillness, angular_stillness
       Return:
           bounds(dict): {"upper_bound": X, "lower_bound": Y}
    """
    # calculate mean and standard dev mean distance
    all_mean_distances = [user["mean_distance"] for user in user_data]
    mean_mean_distance = numpy.mean(all_mean_distances)
    std_mean_distance = numpy.std(all_mean_distances)

    # calculate mean and standard dev stillness
    all_mean_stillnesses = [user["stillness"] for user in user_data]
    mean_stillness = numpy.mean(all_mean_stillnesses)
    std_stillness = numpy.std(all_mean_stillnesses)

    # calculate mean and standard dev angular stillness
    all_angular_stillnesses = [user["angular_stillness"] for user in user_data]
    mean_angular_stillness = numpy.mean(all_angular_stillnesses)
    std_angular_stillness = numpy.std(all_angular_stillnesses)

    # overalls
    overall_mean = mean_mean_distance + mean_stillness + mean_angular_stillness
    overall_mean_std = (std_mean_distance ** 2 + std_stillness ** 2 + std_angular_stillness ** 2) ** 0.5

    return {"upper_bound": overall_mean + overall_mean_std,
            "lower_bound": overall_mean - overall_mean_std}


def attention_numerical_toward_combatant(mean_distance, stillness, angular_stillness):
    """Calculates a score representing the attention paid towards a given combatant
        Args:
            combatant_name(str): the name of the combatant
        Return:
            a score of how attentive the user is
    """
    return mean_distance + stillness + angular_stillness


def attention_toward_combatant(combatant_name,
                               attentiveness_score,
                               neutral_attn_threshold=4.097,
                               high_attn_threshold=4.629):
    """Calculates the general attentiveness of a user towards a given combatant,
       where 0 is negative, -1 is low attention, and 1 is high attention
       Note: Current thresholds are calculated based on historical user date,
             will need to be updated over time
        Args:
            combatant_name(str): the name of the combatant
        Return:
            a general attention score of -1 (low), 0 (neutral) and 1 (high)
    """
    if attentiveness_score < neutral_attn_threshold:
        return -1
    elif attentiveness_score < high_attn_threshold:
        return 0
    return 1


def relative_attention_across_combatants(combatant_name_1, combatant_name_2):
    """Determines if a user has a bias between the two combatants
        Args:
            combatant_name_1(str): the name of one combatant
            combatant_name_2(str): the name of the other combatant
        Return:
            a user's relative attentiveness towards the two combatants
    """
    combatant_1_attention = attention_toward_combatant(combatant_name_1)
    combatant_2_attention = attention_toward_combatant(combatant_name_2)
    return [(combatant_name_1, combatant_1_attention), (combatant_name_2,combatant_2_attention)]

