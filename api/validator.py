from abc import ABC, abstractmethod
from database import Day, Week


class Rule(ABC):
    @abstractmethod
    def is_valid(self, day: Day, week: Week, previous_week: Week):
        pass
