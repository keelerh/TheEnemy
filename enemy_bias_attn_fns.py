import numpy


# Current bounds: 
# lower: 4.097
# upper: 4.629

class Bias_Nervousness_Model():

    def __init__(self, user_data):
        self.user_data = user_data  # includes angular stillness, stillness, and mean distance
        self.prev_states = {}
        bounds = self.calculate_bounds(user_data)
        self.LOWER_BOUND = bounds["lower_bound"]
        self.UPPER_BOUND = bounds["upper_bound"]
        self.MEAN_STD = bounds["overall_mean_std"]


    def calculate_bounds(self):
        """Calculates the upper and lower bound thresholds for attentiveness
           Return:
               bounds(dict): {"upper_bound": X, "lower_bound": Y, "overall_mean_std": Z}
        """
        # calculate mean and standard dev mean distance
        all_mean_distances = [user["mean_distance"] for user in self.user_data]
        mean_mean_distance = numpy.mean(all_mean_distances)
        std_mean_distance = numpy.std(all_mean_distances)

        # calculate mean and standard dev stillness
        all_mean_stillnesses = [user["stillness"] for user in self.user_data]
        mean_stillness = numpy.mean(all_mean_stillnesses)
        std_stillness = numpy.std(all_mean_stillnesses)

        # calculate mean and standard dev angular stillness
        all_angular_stillnesses = [user["angular_stillness"] for user in self.user_data]
        mean_angular_stillness = numpy.mean(all_angular_stillnesses)
        std_angular_stillness = numpy.std(all_angular_stillnesses)

        # overalls
        overall_mean = mean_mean_distance + mean_stillness + mean_angular_stillness
        overall_mean_std = (std_mean_distance ** 2 + std_stillness ** 2 + std_angular_stillness ** 2) ** 0.5

        return {"overall_mean_std": overall_mean_std,
                "upper_bound": overall_mean + overall_mean_std,
                "lower_bound": overall_mean - overall_mean_std}


    def percentage_looking_at_face(self, combatant_name, user_id):
        """Calculates the percentage of time a user spends looking at a combatant's face
            Note: Good relationships people typically look at people 60-70% of the time
              Args:
                  combatant_name(str): name of the combatant whose face is being looked at
                  user_id(int): user to calculate percentage looking at combatant for
              Return:
                  percentage(float): percentage of time passed in combatant's face was looked at
        """
        pass


    def nervous_toward_combatant(self, combatant_name, user_id):
        """Calculates a score representing the attention paid towards a given
           combatant which is taken to represent a user's nervousness
            Args:
                combatant_name(str): name of the combatant calculating nervouseness
                                     towards
                user_id(int): id of the user of interest
            Return:
                a score of how attentive the user is
        """
        # bounds = calculate_bounds(self.user_data[user_id])
        # self.LOWER_BOUND = bounds["lower_bound"]
        # self.UPPER_BOUND = bounds["upper_bound"]
        # float
        percentage_looking_at_face = self.percentage_looking_at_face(combatant_name)
        # float
        attentiveness_value = self.user_data[user_id]['mean_angular_stillness'] + \
                              self.user_data[user_id]['mean_stillness'] + \
                              self.user_data[user_id]['mean_distance']
        # looking away from soldier (not their head) >33
        if percentage_looking_at_face < 0.66:
            if attentiveness_value < self.LOWER_BOUND:
                return attentiveness_value + self.MEAN_STD
            else:
                return attentiveness_value + 2 * self.MEAN_STD
        else:  # looking at the HEAD of the solider
            return attentiveness_value


    def nervous_toward_combatant_score(self, combatant_name, user_id):
        """Calculates a value representing the attention paid towards a given
           combatant which is taken to represent a user's nervousness where 0
           is neutral, -1 is low nervousness, and 1 is high nervousness
            Args:
                combatant_name(str): name of the combatant calculating nervouseness
                                     towards
                user_id(int): id of the user of interest
            Return:
                a general attention score of -1 (low), 0 (neutral) and 1 (high)
        """
        # bounds = calculate_bounds(self.user_data[user_id])
        # self.LOWER_BOUND = bounds["lower_bound"]
        # self.UPPER_BOUND = bounds["upper_bound"]
        adjusted_value = self.nervous_toward_combatant(combatant_name, user_id)
        if adjusted_value < self.LOWER_BOUND:
            return -1
        elif adjusted_value < self.UPPER_BOUND:
            return 0
        return 1


    def biased_toward_combatant(self, combatant_name, user_id):
        """Determines if a user has a bias towards a given combatant
            Args:
                combatant_name(str): name of a combatant
                user_id(int): id of the user of interest
            Return:
                boolean representing if a user is or is not neutral towards
                a given combatant
        """
        if self.nervous_toward_combatant(combatant_name, user_id) == 0:
            return False
        return True


    def biased_toward_either(self, conflict, user_id):
        """Determines if a user has a bias towards either combatant in a conflict
            Args:
                conflict(str): name of a given conflict
                user_id(int): id of the user of interest
            Return:
                boolean representing if a user is or is not neutral towards
                either combatant
        """
        return self.biased_toward_combatant(conflict["combatant_1"]) and \
               self.biased_toward_combatant(conflict["combatant_2"])


    def biased_toward_which(self, conflict, user_id):
        """Determines which combatant a user has a bias towards (if any)
            Args:
                conflict(str): name of a given conflict
                user_id(int): id of the user of interest
            Return:
                string representing the name of the combatant a user has a
                bias towards, neither, or both
        """
        if self.biased_toward_combatant(conflict["combatant_1"]) == -1:
            if self.biased_toward_combatant(conflict["combatant_2"] == -1):
                return "both"
            else:
                return conflict["combatant_1"]
        elif self.biased_toward_combatant(conflict["combatant_2"]):
            return conflict["combatant_2"]
        return "neither"


    def negative_bias_toward_either(self, conflict, user_id):
        """Determines if a user has a negative bias towards either combatant in
           a conflict
            Args:
                conflict(str): name of a given conflict
                user_id(int): id of the user of interest
            Return:
                boolean representing if a user has a negative bias towards either
                combatant in a conflict
        """
        return self.biased_toward_combatant(conflict["combatant_1"]) == -1 or \
               self.biased_toward_combatant(conflict["combatant_2"] == -1)


    def sky_change_test(self, combatant_name, user_id):
        """Calculates the values set for cloud/brightness states such
        that for continuous nervousness the sky goes from fully sunny
        to fully cloudy over the course of an interaction with an individual
        combatant (roughly 7.5 minutes)
            Args:
                combatant_name(str): name of a combatant
                user_id(int): id of the user of interest
            Return:
                sky_environment(float): continuous value between 0 and 1,
                                        where 0 to .5 indicates opacity of the
                                        altostratus cloud layer over the sunny
                                        layer and .5 to 1 indicates the opacity
                                        of the nimbostratus layer over altostratus
                                        layer
        """
        prev_state = self.prev_states.get("user_id", 0)
        new_state = self.biased_toward_combatant(combatant_name, user_id)
        tmp = prev_state
        self.prev_states["user_id"] = new_state
        if new_state < prev_state:
            return tmp + 1./15
        elif new_state > prev_state:
            return max(0, tmp - 1./15)
        return new_state


    def post_epilogue_transformation_mirror(self, conflict, user_id):
        """Indicates which combatant the user's avatar looks like at the end
            Args:
                conflict(str): name of a conflict
                user_id(int): id of the user of interest
            Return:
                combatant_name(str): name of the combatant the user's avatar
                                     resembles (i.e. the combatant the user
                                     expressed more bias towards); if the scores
                                     are identical aribitrarily returns the second
                                     comabatant
        """
        (combatant_1, combatant_2) = conflict.combatants
        combatant_1_bias = nervous_toward_combatant_score(combatant_1, user_id)
        combatant_2_bias = nervous_toward_combatant_score(combatant_2, user_id)
        if combatant_1_bias > combatant_2_bias:
            return combatant_1
        return combatant_2
