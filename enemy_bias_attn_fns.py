def attention_numerical_toward_combatant(combatant_name):
    """Calculates a score representing the attention paid towards a given combatant
        Args:
            combatant_name(str): the name of the combatant
        Return:
            attentiveness_score(float): a score of how attentive the user is
    """
    # TODO: based on the metrics we determine
    return attentiveness_score


def attention_toward_combatant(combatant_name,
                               attentiveness_score,
                               neutral_attn_threshold=.4,
                               high_attn_threshold=.7):
    """Calculates the general attentiveness of a user towards a given combatant
        Args:
            combatant_name(str): the name of the combatant
        Return:
            a general attention score from low, neutral and high
    """
    if attentiveness_score < neutral_attn_threshold:
        return "low_attention"
    elif attentiveness_score < high_attn_threshold:
        return "neutral_attention"
    return "high_attention"


def attention_bool_toward_combatant(combatant_name,
                                    attentiveness_score,
                                    is_attentive_threshold=.5):
    """Determines if a user is attentive towards a given combatant
        Args:
            combatant_name(str): the name of the combatant
            attentiveness_score(float): a numberical representation of a
                                        user's attentiveness
            is_attentive_threshold(float): the threshold value to be considered attentive
        Return:
            true if user is attentive else false
    """
    if attentiveness_score < is_attentive_threshold:
        return False
    return True


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

