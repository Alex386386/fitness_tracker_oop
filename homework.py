LEN_STEP = 0.65
LEN_SWIM = 1.38
M_IN_KM = 1000


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Функция возвращающая строку со значениями."""

        return f'Тип тренировки: {self.training_type};' \
               f' Длительность: {self.duration:.3f} ч.;' \
               f' Дистанция: {self.distance:.3f} км;' \
               f' Ср. скорость: {self.speed:.3f} км/ч;' \
               f' Потрачено ккал: {self.calories:.3f}.'


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    LEN_SWIM = 1.38
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        medium_speed = self.get_distance() / self.duration
        return medium_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        r_coeff_cal_1 = 18
        r_coeff_cal_2 = 20
        hours_in_minutes = 60
        duration_in_minutes = self.duration * hours_in_minutes
        medium_speed = self.get_mean_speed()
        total_calories = (r_coeff_cal_1 * medium_speed - r_coeff_cal_2) * self.weight / M_IN_KM * duration_in_minutes
        return total_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration:  int,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        w_coeff_cal_1 = 0.035
        w_coeff_cal_2 = 0.029
        w_coeff_cal_3 = 2
        hours_in_minutes = 60
        dur_in_min = self.duration * hours_in_minutes
        m_speed = self.get_mean_speed()
        total_calories = (w_coeff_cal_1*self.weight+(m_speed**w_coeff_cal_3//self.height)*w_coeff_cal_2*self.height)*dur_in_min
        return total_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

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
        self.LEN_STEP = 1.38

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        medium_speed = self.length_pool * self.count_pool / M_IN_KM / self.duration
        return medium_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        swim_coeff_cal_1 = 1.1
        swim_coeff_cal_2 = 2
        total_calories = (self.get_mean_speed() + swim_coeff_cal_1) * swim_coeff_cal_2 * self.weight
        return total_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        action = data[0]
        duration = data[1]
        weight = data[2]
        length_pool = data[3]
        count_pool = data[4]
        training = Swimming(action, duration, weight, length_pool, count_pool)
        return training
    elif workout_type == 'RUN':
        action = data[0]
        duration = data[1]
        weight = data[2]
        training = Running(action, duration, weight)
        return training
    elif workout_type == 'WLK':
        action = data[0]
        duration = data[1]
        weight = data[2]
        height = data[3]
        training = SportsWalking(action, duration, weight, height)
        return training


def main(training: Training) -> None:
    """Главная функция. Обработка данных с трекера, и её вывод"""

    info = training.show_training_info()
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
