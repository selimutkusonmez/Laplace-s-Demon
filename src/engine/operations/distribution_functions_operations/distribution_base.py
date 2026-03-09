from abc import abstractmethod,ABC

class BaseDistributionFunctionsOperator(ABC):

    @staticmethod
    @abstractmethod
    def calculate(input_list : list) -> float:
        pass