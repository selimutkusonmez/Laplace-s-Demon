from abc import abstractmethod,ABC

class BaseHypothesisTestOperator(ABC):

    @staticmethod
    @abstractmethod
    def calculate(input_list : list) -> float:
        pass