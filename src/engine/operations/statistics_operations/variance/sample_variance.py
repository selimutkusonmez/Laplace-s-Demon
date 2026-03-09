from src.engine.operations.statistics_operations.statistics_base import BaseStatisticsOperator

class CalculateSampleVariance(BaseStatisticsOperator):

    @staticmethod
    def calculate(input_list):
        return 