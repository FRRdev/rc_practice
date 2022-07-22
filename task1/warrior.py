import inspect
import sys
import functools


def __check_health(func):
    """ Life check after taking damage
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        health_left = func(*args, **kwargs)
        current_warrior_object = args[0]
        current_warrior_object_name = current_warrior_object.__class__.__name__
        if health_left <= 0:
            print(f'{current_warrior_object_name} was killed!')
            sys.exit()
        if health_left > current_warrior_object.max_health:
            current_warrior_object.health = current_warrior_object.max_health
        print(f'{current_warrior_object_name} has {current_warrior_object.health} hp\n')

    return wrapper


def __trace_info(func):
    """ Trace info about function
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        frame = inspect.currentframe()
        current_warrior_name = frame.f_locals['self'].__class__.__name__
        print(f'{current_warrior_name} => {func.__name__}')
        return func(self, *args, **kwargs)

    return wrapper


def class_decorator(cls):
    """
    The main decorator for the class that
    adds a health check and information output
    """
    for parent in cls.mro():
        for name, method in parent.__dict__.items():
            if not name.startswith('__') and \
                    not isinstance(getattr(cls, name), property):
                setattr(cls, name, __check_health(__trace_info(method)))
    return cls


class BaseWarrior:
    def __init__(self, health):
        self._max_health = health
        self._health = health

    def eat_apple(self):
        self._health += 5
        return self._health

    def eat_mushroom(self):
        self._health += 10
        return self._health

    def get_damaged(self):
        self._health -= 10
        return self._health

    @property
    def max_health(self):
        return self._max_health

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, health):
        self._health = health


@class_decorator
class Wizard(BaseWarrior):
    def __init__(self, health=100):
        super().__init__(health)

    def get_damaged(self):
        self.health -= 20
        return self.health


@class_decorator
class Paladin(BaseWarrior):
    def __init__(self, health=200):
        super().__init__(health)


class MyFieldManager:
    """ The Manager signaling the beginning and end of the battle
    """

    def __init__(self, first_warrior: BaseWarrior, second_warrior: BaseWarrior):
        self.first_warrior = first_warrior
        self.second_warrior = second_warrior

    def __enter__(self):
        print(
            f'The battle between '
            f'{self.first_warrior.__class__.__name__}'
            f'({self.first_warrior.health}hp) '
            f'and {self.second_warrior.__class__.__name__}'
            f'({self.second_warrior.health}hp)\n'
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('End of a battle!')


if __name__ == '__main__':
    w = Wizard()
    p = Paladin()
    with MyFieldManager(w, p) as field:
        w.get_damaged()
        w.eat_mushroom()
        w.eat_mushroom()
        p.get_damaged()
        p.get_damaged()
        p.eat_apple()
