from abc import abstractmethod,ABC

class BaseProbabilityOperator(ABC):

    @staticmethod
    @abstractmethod
    def calculate(input_list : list) -> float:
        pass