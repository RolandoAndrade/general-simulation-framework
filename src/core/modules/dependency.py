from typing import TypeVar, Callable

R = TypeVar('R')
A = TypeVar('A')
Depends = Callable[[R], A]

B = TypeVar('B')


def map_(d: Depends[R, A], f: Callable[[A], B]) -> Depends[R, B]:
    def depends(r: R) -> B:
        return f(d(r))

    return depends
