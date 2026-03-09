from abc import abstractmethod,ABC

class BaseStatisticsOperator(ABC):

    @staticmethod
    @abstractmethod
    def calculate(input_list : list) -> float:
        pass