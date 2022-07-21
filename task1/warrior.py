import sys
import functools


def trace_action(cls):
    """ Tracing all the actions that occur in warrior class
    """

    class Wrapper:
        def __init__(self, *args):
            self.wrapped = cls(*args)

        def __getattr__(self, item):
            if hasattr(self.wrapped, item) and \
                    not isinstance(getattr(cls, item), property):
                print(f'{cls.__name__} => {item}')
            return getattr(self.wrapped, item)

    return Wrapper


def check_health(func):
    """ Life check after taking damage
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        health_left = func(*args, **kwargs)
        current_warrior_object = args[0]
        current_warrior_object_name = current_warrior_object.__class__.__name__
        print(f'{current_warrior_object_name} has {current_warrior_object.health} hp\n')
        if health_left <= 0:
            print(f'{current_warrior_object_name} was killed!')
            sys.exit()

    return wrapper


class BaseWarrior:
    def __init__(self, health):
        self._health = health

    def eat_apple(self):
        self._health += 5
        return self._health

    def eat_mushroom(self):
        self._health += 10
        return self._health

    @check_health
    def get_damaged(self):
        self._health -= 10
        return self._health

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, health):
        self._health = health


@trace_action
class Wizard(BaseWarrior):
    def __init__(self, health=100):
        super().__init__(health)

    @check_health
    def get_damaged(self):
        self.health -= 20
        return self.health


@trace_action
class Paladin(BaseWarrior):
    def __init__(self, health=200):
        super().__init__(health)


class MyFieldManager:
    """ The Manager signaling the beginning and end of the battle
    """

    def __init__(self, first_warrior, second_warrior):
        self.first_warrior = first_warrior
        self.second_warrior = second_warrior

    def __enter__(self):
        print(
            f'The battle between '
            f'{self.first_warrior.wrapped.__class__.__name__} '
            f'and {self.second_warrior.wrapped.__class__.__name__}\n'
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('End of a battle!')


if __name__ == '__main__':
    w = Wizard()
    p = Paladin()
    with MyFieldManager(w, p) as field:
        p.get_damaged()
        p.get_damaged()
        w.get_damaged()
        p.eat_mushroom()
        p.eat_mushroom()
        p.eat_mushroom()
        p.get_damaged()
