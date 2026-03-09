from src.engine.operations.distribution_functions_operations.distribution_base import BaseDistributionFunctionsOperator

class CalculatePoissonDistributionPMF(BaseDistributionFunctionsOperator):

    @staticmethod
    def calculate(input_list):
        return 