import os

from iterwrap import IterateWrapper, iterate_wrapper


def _perform_operation(_, item: int, vars):
    from time import sleep

    global _tmp
    print(vars)
    sleep(1)
    if item == 0:
        if _tmp:
            _tmp = False
            raise ValueError("here")


def _test_fn():
    data = list(range(10))
    l = [0, 1]  # noqa: E741
    iterate_wrapper(
        _perform_operation,
        data,
        "output.txt",
        num_workers=3,
        envs=[{"id": str(i)} for i in range(3)],
        vars_factory=lambda: {"a": l + [os.environ["id"]]},
    )


def _test_wrapper():
    from time import sleep

    for i in IterateWrapper(range(10)):
        sleep(1)


if __name__ == "__main__":
    _tmp = True
    _test_fn()
