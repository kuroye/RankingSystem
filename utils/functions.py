


class Function:

#     R 是学校的平均评分，即所有用户对该电影的评分的平均值。

#     v 是该学校获得的投票数，也就是评分的数量。

#     m 是必要的最小投票数，学校的评分数必须达到这个数目才会在榜单中被公开显示。这个数字由 管理员 设定，以防止小样本的评分在榜单中占据优势。

#     C 是所有学校的平均评分的平均值。

#     weighted rating (WR) = (v ÷ (v+m)) × R + (m ÷ (v+m)) × C
    def bayes_theorem(self, school_info, C):

        R = self.calculate_average(school_info)['avg_score']
        v = len(school_info['user'])
        m = 1
        weighted_rating = (v / (v+m)) * R + (m / (v+m)) * C

        return round(weighted_rating, 2)

    def get_all_schools_avg(self, school_list):
        sum_of_shool_avg_score = 0
        for school in school_list:
            sum_of_shool_avg_score += school['avg_score'] 
        return sum_of_shool_avg_score / len(school_list)

    def calculate_average(self, school_info):

        user_scores = school_info['user']


        if len(user_scores) != 0:
            user_avg = sum(user_scores) / len(user_scores)
        else:
            # print("No user scores available to calculate average.")
            user_avg = 0  # You can assign any default value

       
        return {
            'school': school_info['school'],
            'user': school_info['user'],
            'avg_score': user_avg
        }

   
    #获取所有学校
    def get_school_list(self, SchoolModel, SchoolSerializer):
        model = SchoolModel.objects.all()
        serializer = SchoolSerializer(model, many=True)
        school_list = serializer.data

        return school_list

    #根据Serializer获得所有数据
    def get_all_survey(self, SurveyModel, SurveySerializer):
        model = SurveyModel.objects.all()
        serializer = SurveySerializer(model, many=True)
        survey_list = serializer.data

        return survey_list



    #获取单个卷子
    def get_a_survey(self, survey_list):
        
        for survey in survey_list:
            if survey["user"]==6:
                return survey

    #获取一个人的所有答案
    def get_responses_from_survey(self, survey):

        responses = survey.get("responses")

        return responses

    #获取单个答案
    def get_a_response(self, responses):

        for response in responses:
            return response

    #获取分数
    def get_score(self, response):

        return response['score']

    #获得问题
    def get_question(self, response):
        return response['question']
    
    #获取指标3
    def get_III(self, question):
        return question['indicator3']
    
    #获取占比
    def get_weight(self, obj):
        return obj['weight']

    #分数和占比相乘
    def multiply_weight(self, score, weight):
        return score*weight

    #相乘后的分数的合
    def sum_of_multiplied_score(self, score_list):
       return sum(score_list)


    #     # [1,2,3]
    #     # 1 = {1.A, 1.B}
    #     # 1.A = {1.Aa, 1.Ab}
    #     # 1.Aa = {Q1,Q2,Q3}


    def make_nested_dict(self, indicator_modules):
        """
        生成嵌套字典，从内到外分别为 indicator III, indicator II 和 indicator I。
        Args:
        indicators_list: 包含 indicator I 对象的列表。
        Returns:
        生成的嵌套字典。
        """

        calculation_dict = {}
        # 对于每个 indicator I，找到与其相关的所有 indicator II。
        for ind1 in indicator_modules["Ind1"].objects.all():
            
            calculation_dict[str(ind1.id)] = {}
            

            # 对于每个 indicator II，找到与其相关的所有 indicator III。
            for ind2 in indicator_modules["Ind2"].objects.filter(IndicatorI=ind1):
                
                calculation_dict[str(ind1.id)][str(ind2.id)] = {}
                # calculation_dict[str(ind1.id)][str(ind2.id)]["weight"] = ind2.weight

                # 对于每个 indicator III，将其添加到对应的嵌套字典中。
                for ind3 in indicator_modules["Ind3"].objects.filter(IndicatorII=ind2):
                    calculation_dict[str(ind1.id)][str(ind2.id)][str(ind3.id)] = {}
                    # calculation_dict[str(ind1.id)][str(ind2.id)][str(ind3.id)]["weight"] = ind3.weight

                    # 对于每个 Question，将其添加到对应的嵌套字典中。
                    for question in indicator_modules["Question"].objects.filter(indicatorIII=ind3):
                        calculation_dict[str(ind1.id)][str(ind2.id)][str(ind3.id)][str(question.id)] = {}
                        calculation_dict[str(ind1.id)][str(ind2.id)][str(ind3.id)][str(question.id)]["weight"] = question.weight
                        calculation_dict[str(ind1.id)][str(ind2.id)][str(ind3.id)][str(question.id)]["score"] = 0


        return calculation_dict



    
        
    # # 获得占比
    def get_weight(self, Model, id):

        model = Model.objects.filter(pk=id).first()

        return model.weight



    def add_score_to_nested_dict(self, calculation_dict, responses):

        
        for ind1 in calculation_dict:
            # print(ind1, "---")
            
            for ind2 in calculation_dict[ind1]:
                # print(ind2, "!!")
               

                for ind3 in calculation_dict[ind1][ind2]:
                    # print(ind3,"#")
                    for question in calculation_dict[ind1][ind2][ind3]:
                        # print(question)
                        for response in responses:
                            if str(response["question"]["question_id"]) == question:
                                calculation_dict[ind1][ind2][ind3][question]["score"] = response["score"]

        return calculation_dict


    def add_weight_to_nested_dict(self, calculation_dict, modules):

        for ind1 in calculation_dict:
            # print(ind1, "---")
            if ind1 != "weight":
                weight1 = self.get_weight(modules["Ind1"], int(ind1))
            
                if weight1:
                    calculation_dict[ind1]["weight"] = weight1 

            for ind2 in calculation_dict[ind1]:
                # print(ind2, "!!")

                
                if ind2 != "weight":
                    weight2 = self.get_weight(modules["Ind2"], int(ind2))

                    if weight2:
                        calculation_dict[ind1][ind2]["weight"] = weight2

                if isinstance(calculation_dict[ind1][ind2], dict):
                    for ind3 in calculation_dict[ind1][ind2]:

                        # print(ind3,"#")
            
                        if ind3 != "weight":
                            weight3 = self.get_weight(modules["Ind3"], int(ind3))

                            if weight3:
                                calculation_dict[ind1][ind2][ind3]["weight"] = weight3
                        
        
        return calculation_dict



        # calculate final score = IndicatorI + IndicatorI + IndicatorI
    def calculate_final_score(self, calculation_dict):
        
        
        """
        计算嵌套字典中所有得分加权后的最终得分

        :param calculation_dict: 嵌套字典，包含了题目和得分信息
        :return: 最终得分
        """
        total_score = 0  # 初始化最终得分为0
        for ind1 in calculation_dict:  # 遍历第一层字典
            if isinstance(calculation_dict[ind1], dict) and "weight" in calculation_dict[ind1]:
                    # 如果第一层字典的值是字典，并且包含权重信息，则获取该字典的权重
                    weight1 = calculation_dict[ind1]["weight"]
                    for ind2 in calculation_dict[ind1]:  # 遍历第二层字典
                        if isinstance(calculation_dict[ind1][ind2], dict) and "weight" in calculation_dict[ind1][ind2]:
                            # 如果第二层字典的值是字典，并且包含权重信息，则获取该字典的权重
                            weight2 = calculation_dict[ind1][ind2]["weight"]
                            for ind3 in calculation_dict[ind1][ind2]:  # 遍历第三层字典
                                if isinstance(calculation_dict[ind1][ind2][ind3], dict) and "weight" in calculation_dict[ind1][ind2][ind3]:
                                    # 如果第三层字典的值是字典，并且包含权重信息，则获取该字典的权重
                                    weight3 = calculation_dict[ind1][ind2][ind3]["weight"]
                                    for question in calculation_dict[ind1][ind2][ind3]:  # 遍历题目字典
                                        if isinstance(calculation_dict[ind1][ind2][ind3][question], dict) and "weight" in calculation_dict[ind1][ind2][ind3][question]:

                                            weight4 = calculation_dict[ind1][ind2][ind3][question]["weight"]
                                        if question != "weight":
                                            # 如果当前键不是权重，则获取该题目的得分并加权
                                            score = calculation_dict[ind1][ind2][ind3][question]["score"]
                                            weighted_score = score * weight1 * weight2 * weight3 * weight4
                                            total_score += weighted_score  # 将加权得分累加到最终得分中

        return total_score  # 返回最终得分