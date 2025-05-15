import logging
from pathlib import Path

from hail.development import AbstractDevelopment
from hail.result import AbstractResultGraph, AbstractResultKPI, AbstractResultMap
from hail.generate import import_all_classes_from_folder


RESULT_CLASSES = [AbstractResultGraph, AbstractResultKPI, AbstractResultMap]
CONFIG = Path(__file__).parent.parent / "config"


def test_initiation_fields_against_totals():
    abs_dev_classes = import_all_classes_from_folder(CONFIG, AbstractDevelopment)
    logging.debug(
        f"Found {len(abs_dev_classes)} AbstractDevelopments in the config folder."
    )

    abs_res_classes = []
    for cls in RESULT_CLASSES:
        abs_res_classes += import_all_classes_from_folder(CONFIG, cls)

    logging.debug(f"Found {len(abs_res_classes)} AbstractResults in the config folder.")

    classes = abs_res_classes + abs_dev_classes

    for cls in classes:
        try:
            cls()
        except TypeError as e:
            missing_methods = e.__str__().split("methods")[-1]

            assert False, f"Class {cls.__name__} is missing {missing_methods}"
