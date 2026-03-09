from src.engine.operations.distribution_functions_operations.distribution_base import BaseDistributionFunctionsOperator

class CalculatePoissonDistributionCDF(BaseDistributionFunctionsOperator):

    @staticmethod
    def calculate(input_list):
        return 