import numpy


# Current bounds: 
# lower: 4.097
# upper: 4.629

class Bias_Nervousness_Model():

    def __init__(self, user_data):
        self.user_data = user_data  # includes angular stillness, stillness, and mean distance
        self.prev_states = {}
        self.bias_per_conflict = {conflict_name_1: [], conflict_name_1: [], conflict_name_1: []}
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

        #overall stillness
        overall_stillness_mean = mean_stillness + mean_angular_stillness
        overall_stillness_mean_std = (std_stillness ** 2 + std_angular_stillness ** 2) ** 0.5

        return {"stillness": {"overall_stillness_mean_std": overall_stillness_mean_std,
                "overall_stillness_upper_bound": overall_stillness_mean + overall_stillness_mean_std,
                "overall_stillness_lower_bound": overall_stillness_mean - overall_stillness_mean_std},
                "distance": {"distance_mean_std": std_mean_distance,
                "distance_upper_bound": mean_mean_distance + std_mean_distance,
                "distance_lower_bound": mean_mean_distance - std_mean_distance}}

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
        attentiveness_values = {
                                "stillness": self.user_data[user_id]['mean_angular_stillness'] + \
                                             self.user_data[user_id]['mean_stillness'],
                                "distance": self.user_data[user_id]['mean_distance']
                                }
        # looking away from soldier (not their head) >33
        if percentage_looking_at_face < 0.66:
            adjusted_attentiveness = {"stillness": attentiveness_value["stillness"] + 2 * self.STILLNESS_MEAN_STD, "distance": attentiveness_value["distance"]}
            for key, value in adjusted_attentiveness.iteritems():
                attentiveness_value[key] = 1.0 / value
        elif self.user_data[user_id]['mean_distance'] > 1.5 * self.DISTANCE_MEAN_STD:  # looking at the HEAD of the soldier, but standing very far away (can be commented out if distance is not to be included in nervousness calculation)
            adjusted_attentiveness = {"stillness": attentiveness_value["stillness"] + self.STILLNESS_MEAN_STD, "distance": attentiveness_value["distance"] + 2 * self.DISTANCE_MEAN_STD}
            for key, value in adjusted_attentiveness.iteritems():
                attentiveness_value[key] = 1.0 / value
        return attentiveness_values

    def nervous_toward_combatant_web_reg(self, combatant_name, user_id):
        """Calculates a score representing the attention paid towards a given combatant which is taken
        to represent a users nervousness; please note that this function takes into account the user web
        registration data whereas the Nervous_Toward_Combatant function does not.

        Note:
            The Questions 2-4 from the updated online user registration questions in the spec should be
            used for this "test" on evaluating if user.web_registration_bias_data(combatant_name) is True or False.

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
                if user.web_registration_bias_data(combatant_name):
                        return attentiveness_value + 2*self.MEAN_STD
                else:
                        return attentiveness_value + self.MEAN_STD
            else:
                if user.web_registration_bias_data(combatant_name):
                         return attentiveness_value + 3 * self.MEAN_STD
                else:
                        return attentiveness_value + 2*self.MEAN_STD
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
        if adjusted_value["distance"] < self.DISTANCE_LOWER_BOUND:
            return -1
        elif adjusted_value["stillness"] < self.STILLNESS_LOWER_BOUND:
            return -1
        elif adjusted_value["distance"] > self.DISTANCE_UPPER_BOUND:
            return 1
        elif adjusted_value["stillness"] > self.STILLNESS_UPPER_BOUND:
            return 1
        return 0

    def nervous_toward_combatant_score_web_reg(self, combatant_name, user_id):
        """Calculates a value representing the attention paid towards a given
           combatant which is taken to represent a user's nervousness where 0
           is neutral, -1 is low nervousness, and 1 is high nervousness; please note that this function takes into account the user registration date whereas the nervous_toward_combatant_score function does not
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

    def biased_toward_combatant_web_reg(self, combatant_name, user_id):
        """Determines if a user has a bias towards a given combatant; please note that this function uses the web registration data while the other biased_toward_combatant function does not.
            Args:
                combatant_name(str): name of a combatant
                user_id(int): id of the user of interest
            Return:
                boolean representing if a user is or is not neutral towards
                a given combatant
        """
        if self.nervous_toward_combatant_web_reg(combatant_name, user_id) == 0:
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

     def biased_toward_either_web_reg(self, conflict, user_id):
        """Determines if a user has a bias towards either combatant in a conflict; please note that this function uses the web registration data while the other biased_toward_either function does not.
            Args:
                conflict(str): name of a given conflict
                user_id(int): id of the user of interest
            Return:
                boolean representing if a user is or is not neutral towards
                either combatant
        """
        return self.biased_toward_combatant_web_reg(conflict["combatant_1"]) and \
               self.biased_toward_combatant_web_reg(conflict["combatant_2"])


    def biased_toward_which(self, conflict, user_id):
        """Determines which combatant a user has a bias towards (if any)
        """Also updates the User_Bias_Per_Conflict array based on their bias towards Both ("B"), Neither ("N"), or one combatant (1)
            Args:
                conflict(str): name of a given conflict
                user_id(int): id of the user of interest
            Return:
                string representing the name of the combatant a user has a
                bias towards, neither, or both
        ""
        if self.biased_toward_combatant(conflict["combatant_1"]) == -1:
            if self.biased_toward_combatant(conflict["combatant_2"] == -1):
                user.Bias_Per_Conflict[conflict] = "B"
                return "both"
            else:
                user.Bias_Per_Conflict[conflict] = "1"
                return conflict["combatant_1"]
        elif self.biased_toward_combatant(conflict["combatant_2"]):
            return conflict["combatant_2"]
        user.Bias_Per_Conflict[conflict] = "N"
        return "neither"

    def biased_toward_which_web_reg(self, conflict, user_id):
        """Determines which combatant a user has a bias towards (if any); please note that this function uses the web_reg version of the biased_toward_combatant function.
        """Also updates the User_Bias_Per_Conflict array based on their bias towards Both ("B"), Neither ("N"), or one combatant (1)
            Args:
                conflict(str): name of a given conflict
                user_id(int): id of the user of interest
            Return:
                string representing the name of the combatant a user has a
                bias towards, neither, or both
        ""
        if self.biased_toward_combatant_web_reg(conflict["combatant_1"]) == -1:
            if self.biased_toward_combatant_web_reg(conflict["combatant_2"] == -1):
                user.Bias_Per_Conflict[conflict] = "B"
                return "both"
            else:
                user.Bias_Per_Conflict[conflict] = "1"
                return conflict["combatant_1"]
        elif self.biased_toward_combatant_web_reg(conflict["combatant_2"]):
            return conflict["combatant_2"]
        user.Bias_Per_Conflict[conflict] = "N"
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

    def negative_bias_toward_either_web_reg(self, conflict, user_id):
        """Determines if a user has a negative bias towards either combatant in a conflict; please note that this function uses the web registration data while the other negative_bias_toward_either function does not.
 
            Args:
                conflict(str): name of a given conflict
                user_id(int): id of the user of interest
            Return:
                boolean representing if a user has a negative bias towards either
                combatant in a conflict
        """
        return self.biased_toward_combatant_web_reg(conflict["combatant_1"]) == -1 or \
               self.biased_toward_combatant_web_reg(conflict["combatant_2"] == -1)

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

    def epilogue_intro(self,user_id):
        """Determines whether or not the user is a “hawk” 
            (someone who is pro-war) or “dove” (someone who 
            is anti-war) based on the user's web registration 
            data to Question 1 on the survey which asks them 
            about their feelings on war.

            Args:
                user_id(int): id of the user of interest
            Return:
                case_id: an id labelled 0-5 which indicates which epilogue 
                the user should hear based on their feelings towards war.

        KEY:
        case_id = 0:  Null; User did not fill out web registration survey
        case_id = 1:  User is most pro-war
        case_id = 2:  User is somewhat pro-war
        case_id = 3:  User is neutral
        case_id = 4:  User is somewhat anti-war
        case_id = 5:  User is most anti-war
        """
        # declares the variable to be 0 by default
            case_id = 0
        # checks whether or not the user has completed the web registration survey 
           if user.web_registration_data_completed = True:
        # for users who completed the web survey: we evaluate the choice they made for question 1
        # key: linear scale: 1=most pro-war to 5=most anti-war
              if user.web_registration_data(question_1) = “1”: 
                    case_id = 1
              elif user.web_registration_data(question_1) = “2”: 
                    case_id = 2
              elif user.web_registration_data(question_1) = “3”: 
                    case_id = 3
              elif user.web_registration_data(question_1) = “4”: 
                    case_id = 4
              elif user.web_registration_data(question_1) = “5”: 
                    case_id = 5
        return case_id

    def user_state_trajectory(self, user_data):
        """Returns an array tracking the user's nervousness for each combatant across the 3 conflicts. each element of
        the array corresponds to the nervousness that the user had towards the combatants for the given conflict --
        e.g.: first element corresponds to the first conflict. this can be used at the end to determine the user's final
        user_state_trajectory (and hence, which epilogue to provide).

        Note:
            The array should be populated with elements using the following key:
            “B” = User was nervous towards BOTH combatants in this conflict.
            “N” = User was nervous towards NEITHER combatant in this conflict.
            “1” = User was nervous towards ONE combatant in this conflict.
        """
        return user.Bias_Per_Conflict

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
                                     combatant
        """
        (combatant_1, combatant_2) = conflict.combatants
        combatant_1_bias = nervous_toward_combatant_score(combatant_1, user_id)
        combatant_2_bias = nervous_toward_combatant_score(combatant_2, user_id)
        if combatant_1_bias > combatant_2_bias:
            return combatant_1
        return combatant_2

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
        new_state = self.nervous_toward_combatant(combatant_name, user_id)
        tmp = prev_state
        self.prev_states["user_id"] = new_state
        if new_state < prev_state:
            return tmp + 1./15
        elif new_state > prev_state:
            return max(0, tmp - 1./15)
        return new_state
