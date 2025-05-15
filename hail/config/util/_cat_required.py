from pathlib import Path


if __name__ == "__main__":
    to_add = """
        @staticmethod
        def min(var: "Var"):
            return var.Matrix(0)

        @staticmethod
        def max(var: "Var"):
            return var.Matrix(10)

        @staticmethod
        def default(var: "Var"):
            return var.Matrix(5)

        @staticmethod
        def sets_ETM_value(var: "Var"):
            raise NotImplementedError

        @staticmethod
        def aggregate(var: "Var"):
            raise NotImplementedError
    """

    # glob this __file__ parent for all *.py files not starting with _
    for p in Path(__file__).parent.glob("[!_]*.py"):

        # add the string to the end of the file and write it back
        skip = False
        if p.stem == "verduurzaming_bestaand_cv_ketels":
            skip = True
        if p.stem == "zon_op_dak_huishoudens":
            skip = True

        if skip:
            continue
        with open(p, "a") as f:
            f.write(to_add)
