from src.engine.operations.hypothesis_tests_operations.hypothesis_tests_base import BaseHypothesisTestOperator

class TestPairedSampleTTest(BaseHypothesisTestOperator):

    @staticmethod
    def calculate(input_list):
        return 