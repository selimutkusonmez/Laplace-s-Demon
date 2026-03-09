from abc import abstractmethod,ABC

class BaseEstimationAndTheoryOperator(ABC):

    @staticmethod
    @abstractmethod
    def calculate(input_list : list) -> float:
        pass