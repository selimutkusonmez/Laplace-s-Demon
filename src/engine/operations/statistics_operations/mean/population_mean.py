from src.engine.operations.statistics_operations.statistics_base import BaseStatisticsOperator

class CalculatePopulationMean(BaseStatisticsOperator):

    @staticmethod
    def calculate(input_list):
        population_sum = input_list[0]
        population_size = input_list[1]
        population_mean = population_sum / population_size
        return population_mean