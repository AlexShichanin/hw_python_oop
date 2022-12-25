class InfoMessage():
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float,
                 distance: int, speed: int, calories: int) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.averag_speed: float = self.get_distance() / self.duration
        return self.averag_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        ...

    def show_training_info(self):
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        self.result_calor: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                                     * super().get_mean_speed()
                                    + self.CALORIES_MEAN_SPEED_SHIFT)
                                    * self.weight
                                    / self.M_IN_KM
                                    * self.duration
                                    * self.MIN_IN_H)
        return self.result_calor


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                 / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight) * (self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    MEAN_SPEED_ADDITION: float = 1.1
    COMPLEX_MEAN_SPEED_MULTIPLIER: int = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        self.averag_speed: float = (self.length_pool * self.count_pool
                                    / self.M_IN_KM / self.duration)
        return self.averag_speed

    def get_spent_calories(self) -> float:
        self.total_calories = ((self.get_mean_speed()
                                + self.MEAN_SPEED_ADDITION)
                               * self.COMPLEX_MEAN_SPEED_MULTIPLIER
                               * self.weight * self.duration)
        return self.total_calories

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance


def read_package(workout_type: str, data: list):
    """Прочитать данные полученные от датчиков."""
    code_dict: dict = {'RUN': Running,
                       'WLK': SportsWalking,
                       'SWM': Swimming}

    if workout_type == 'RUN':
        run1 = code_dict['RUN'](*data)
        return run1
    elif workout_type == 'WLK':
        walk1 = code_dict['WLK'](*data)
        return walk1
    elif workout_type == 'SWM':
        swim1 = code_dict['SWM'](*data)
        return swim1


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [('SWM', [720, 1, 80, 25, 40]),
                ('RUN', [15000, 1, 75]),
                ('WLK', [9000, 1, 75, 180])]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        if read_package is not None:
            main(training)
