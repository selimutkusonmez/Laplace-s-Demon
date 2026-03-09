from src.engine.operations.hypothesis_tests_operations.hypothesis_tests_base import BaseHypothesisTestOperator

class TestSingleSampleTTest(BaseHypothesisTestOperator):

    @staticmethod
    def calculate(input_list):
        return 