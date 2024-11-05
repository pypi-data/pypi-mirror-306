from abc import abstractmethod, ABCMeta, ABC


class AIRPABase_Session(metaclass=ABCMeta):
    @abstractmethod
    def exec(
        self,
        params: dict,
        job_id: str = None,
        timeout_start: int = 30,
        timeout_processing: int = 0,
    ) -> dict:
        raise NotImplementedError("my_method is not implemented")
