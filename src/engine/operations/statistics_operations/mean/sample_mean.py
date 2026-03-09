from src.engine.operations.statistics_operations.statistics_base import BaseStatisticsOperator

class CalculateSampleMean(BaseStatisticsOperator):

    @staticmethod
    def calculate(input_list):
        sample_sum = input_list[0]
        sample_sum = input_list[1]
        sample_mean = sample_sum / sample_sum
        return sample_mean