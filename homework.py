from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Функция возвращающая строку со значениями."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    LEN_SWIM: float = 1.38
    M_IN_KM: int = 1000
    HOURS_IN_MINUTES: int = 60

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.duration_min = self.duration * self.HOURS_IN_MINUTES
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError  # В случае запуска функции произойдёт ошибка

    # так как в базовом классе метод get_spent_calories не определён,
    # ведь для каждого типо тренировки он свой,
    # и определён должен быть непосредственно в классе конкретной тренировки.

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    R_COEFF_CAL_1: int = 18
    R_COEFF_CAL_2: int = 20

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        medium_speed = self.get_mean_speed()
        result_medium_speed = self.R_COEFF_CAL_1 * medium_speed
        coeff_medium_speed = (result_medium_speed - self.R_COEFF_CAL_2)
        changed_weight = coeff_medium_speed * self.weight
        return changed_weight / self.M_IN_KM * self.duration_min


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    W_COEFF_CAL_1: float = 0.035
    W_COEFF_CAL_2: float = 0.029
    W_COEFF_CAL_3: int = 2

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        m_speed = self.get_mean_speed()
        result_speed = (m_speed ** self.W_COEFF_CAL_3 // self.height)
        coeff_weight = self.W_COEFF_CAL_1 * self.weight
        coeff_height = result_speed * self.W_COEFF_CAL_2 * self.height
        return (coeff_weight + coeff_height) * self.duration_min


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIM_COEFF_CAL_1: float = 1.1
    SWIM_COEFF_CAL_2: int = 2

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        pool_distance = self.length_pool * self.count_pool
        return pool_distance / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        swim_speed = (self.get_mean_speed() + self.SWIM_COEFF_CAL_1)
        return swim_speed * self.SWIM_COEFF_CAL_2 * self.weight


def read_package(workout_type_def: str, data_def: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_of_raining = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    return type_of_raining[workout_type_def](*data_def)


def main(training_def: Training) -> None:
    """Главная функция. Обработка данных с трекера, и их вывод."""
    info = training_def.show_training_info()
    info_text = info.get_message()
    print(info_text)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
