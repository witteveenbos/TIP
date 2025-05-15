if __name__ == "__main__":
    files = [
        "zon_op_dak_grootschalig",
        "utiliteiten_cv_ketels",
        "utiliteiten_all_electric",
        "utiliteiten_hybride",
        "utiliteiten_warmtenet",
        "verduurzaming_bestaand_all_electric",
        "verduurzaming_bestaand_hybride",
        "verduurzaming_bestaand_warmtenet",
        "verduurzaming_glastuibouw_geothermie",
        "besparing_door_isolatie_reductie_warmtevraag",
        "utiliteiten_besparing_energievraag",
        "verandering_persoonskilometers",
        "verandering_vrachtkilometers",
        "besparing_energievraag_verspreide_industrie",
    ]

    for file in files:
        # create a python file with the name
        with open(f"{file}.py", "w") as f:
            f.write(f"from .groups import group")
