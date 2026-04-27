from src.engine.operations.statistics_operations.statistics_base import BaseStatisticsOperator
import math

class CalculatePopulationStandardDeviation(BaseStatisticsOperator):

    @staticmethod
    def calculate(input_list : list):
        population_mean =input_list[0]
        population_size = input_list[1]
        population_data = input_list[2]
        population_standard_deviation = math.sqrt(sum((x - population_mean) ** 2 for x in population_data) / population_size)
        return population_standard_deviation
         