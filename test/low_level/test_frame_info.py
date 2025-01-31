import inspect

from pyinstrument.low_level import stat_profile as stat_profile_c
from pyinstrument.low_level import stat_profile_python


class AClass:
    def get_frame_info_for_a_method(self, getter_function):
        frame = inspect.currentframe()
        assert frame
        return getter_function(frame)

    def get_frame_info_with_cell_variable(self, getter_function):
        frame = inspect.currentframe()
        assert frame

        def an_inner_function():
            # reference self to make it a cell variable
            if self:
                pass

        return getter_function(frame)

    @classmethod
    def get_frame_info_for_a_class_method(cls, getter_function):
        frame = inspect.currentframe()
        assert frame
        return getter_function(frame)


def test_frame_info():
    frame = inspect.currentframe()

    assert frame
    assert stat_profile_c.get_frame_info(frame) == stat_profile_python.get_frame_info(frame)


def test_frame_info_with_classes():
    instance = AClass()

    test_functions = [
        instance.get_frame_info_for_a_method,
        AClass.get_frame_info_for_a_class_method,
        instance.get_frame_info_with_cell_variable,
    ]

    for test_function in test_functions:
        assert test_function(stat_profile_c.get_frame_info) == test_function(
            stat_profile_python.get_frame_info
        )
