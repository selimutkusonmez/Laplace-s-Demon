from src.engine.operations.distribution_functions_operations.distribution_base import BaseDistributionFunctionsOperator

class CalculateLogNormalDistributionCDF(BaseDistributionFunctionsOperator):

    @staticmethod
    def calculate(input_list):
        return 