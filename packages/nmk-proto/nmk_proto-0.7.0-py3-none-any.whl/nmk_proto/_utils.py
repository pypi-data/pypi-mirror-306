from pathlib import Path

from nmk.model.model import NmkModel


# Get proto source folder from config
def get_proto_folder(model: NmkModel) -> Path:
    return Path(model.config["protoFolder"].value)


# Get input files
def get_input_proto_files(model: NmkModel) -> list[Path]:
    return model.config["protoInputFiles"].value


# Get input sub-folders (all)
def get_input_all_sub_folders(model: NmkModel) -> list[Path]:
    return model.config["protoAllInputSubDirs"].value


# Get input sub-folders (unique occurrence filter)
def get_input_unique_sub_folders(model: NmkModel) -> list[Path]:
    return model.config["protoUniqueInputSubDirs"].value


# Get declared proto folders dependencies
def get_proto_deps(model: NmkModel) -> list[str]:
    return [Path(p) for p in model.config["protoDeps"].value]


# Get generated proto paths options
def get_proto_paths_options(model: NmkModel) -> list[str]:
    return model.config["protoPathOptions"].value
