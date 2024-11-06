"""Create the usage information string for the CLI."""

import json
import os
from pathlib import Path

from soil_moisture_prediction.input_data import depth_levels, soilgrid_keys, stream_dic
from soil_moisture_prediction.pydantic_models import InputParameters

work_dir = os.path.join("soil_moisture_prediction", "test_data")
with open(os.path.join(work_dir, "parameters.json"), "r") as f_handle:
    input_parameters_dic = json.loads(f_handle.read())

input_parameters = InputParameters(**input_parameters_dic)

information = """The cli-tool takes the path to a directory containing a JSON file with input parameters. The input files can be put in the same directory as the parameters file or must be given as an absolute path.

## Directory structure
This is an example of this directory structure:

```
soil_moisture_prediction/test_data/
{directory_tree}
```

## Input parameters
The parameters.json file in this example directory contains the following content:

```
$ cat soil_moisture_prediction/test_data/parameters.json
{parameter_content}
```

## Input data
There are two ways to provide predictor data. Either by providing a file path or by providing a specific key for one of the following predictor sources. If a key is used, the information in the parameters.json file must be 'null'. For each predictor key an external source is used to retrieve the data for the selected geometry.

If for ["predictors"][pred_key]["file_path"] and ["soil_moisture_data"] a file path is given, the file is assumed to be in the same directory as the parameters.json file.

The predictor keys are:

{predictor_keys}

So these are three possbile ways to provide the predictor data:

```
{example_file_name_predictor}
```

```
{example_path_predictor}
```

```
{example_stream_predictor}
```

The predictor file looks like this:
```
$ head -n {head_n} soil_moisture_prediction/test_data/predictor_data.csv
{predictor_data}
```

The predictor can have a head starting with a #. After the #, a json must be given with the same information as the parameters.json file. This is a redundant way of giving the parameters and is used for programmatic reading with out a parameters.json file.

The soil moisture data looks like this:
```
$ head -n {head_n} soil_moisture_prediction/test_data/soil_moisture_data.csv
{soil_moisture_data}
```

The soil moisture data can have a header with the column names.

## Pydantic model
This is a description of the input parameters model:
{pydantic_model_information}"""  # noqa

# Used for tree representation of directory structure:
space = "    "
branch = "│   "
tee = "├── "
last = "└── "

file_exeptions = [
    "predictor_4_nan_in_training.csv",
    "predictor_4_wrong_nan.csv",
    "predictor_1_no_deviation.csv",
    "predictor_1_to_many_columns.csv",
]
current_dir = os.path.dirname(os.path.abspath(__file__))
test_data_dir = os.path.join(current_dir, "test_data")

head_n = 5


def tree(dir_path: Path, prefix: str = ""):
    """Like gnu tree.

    Found at https://stackoverflow.com/questions/9727673
    """
    contents = sorted([o for o in dir_path.iterdir() if o.name not in file_exeptions])

    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir():  # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix + extension)


def build_predictor_keys():
    """Build the predictor keys string."""
    predictor_keys = ""
    print_depth_level = depth_levels[0]

    for key, StreamClass in stream_dic.items():
        if key.split("_")[0] in soilgrid_keys:
            depth_level = key.split("_")[1]
            if depth_level != print_depth_level:
                continue
            print_key = key.split("_")[0] + "_x-ycm"
        else:
            print_key = key

        stream = StreamClass(key, input_parameters)
        info = stream.info().replace(print_depth_level, "x-ycm")
        info = info.replace("\n", "\n   ")
        predictor_keys += f" * {print_key}: {info}\n"
    predictor_keys += f" * Available depth levels for SoilGrids data: {', '.join(depth_levels)}\n"  # noqa

    return predictor_keys


def compile_information():
    """Compile the information string."""
    directory_tree = "\n".join(list(tree(Path(test_data_dir))))

    with open(os.path.join(test_data_dir, "parameters.json"), "r") as f_handle:
        parameters = json.loads(f_handle.read())
        parameter_content = json.dumps(parameters, indent=2)

    predictors_file = {
        pred: pred_data
        for pred, pred_data in parameters["predictors"].items()
        if pred == "elevation"
    }

    # Some text formatting for the example predictor file
    example_predictor_template = '"predictors": {0},\n  ...\n}}'

    example_file_name_predictor = example_predictor_template.format(
        json.dumps(predictors_file, indent=2)[:-2]
    )

    predictors_file["elevation"]["file_path"] = ["/abs/path/to/predictor_1.csv"]

    predictor_keys = build_predictor_keys()

    example_path_predictor = example_predictor_template.format(
        json.dumps(predictors_file, indent=2)[:-2]
    )

    example_stream_predictor = example_predictor_template.format(
        {"elevation_bkg": None}
    )

    predictor_data = ""
    with open(os.path.join(test_data_dir, "predictor_1.csv"), "r") as f_handle:
        for _ in range(head_n):
            predictor_data += f_handle.readline()
    predictor_data = predictor_data[:-1]

    soil_moisture_data = ""
    with open(os.path.join(test_data_dir, "crn_soil-moisture.csv"), "r") as f_handle:
        for _ in range(head_n):
            soil_moisture_data += f_handle.readline()
    soil_moisture_data = soil_moisture_data[:-1]

    pydantic_model_information = ""
    for field_name, field in InputParameters.model_fields.items():
        pydantic_model_information += f"{field_name}:\n  {field.description}\n\n"
    pydantic_model_information = pydantic_model_information[:-2]

    return information.format(
        directory_tree=directory_tree,
        parameter_content=parameter_content,
        predictor_keys=predictor_keys,
        head_n=head_n,
        predictor_data=predictor_data,
        soil_moisture_data=soil_moisture_data,
        pydantic_model_information=pydantic_model_information,
        example_file_name_predictor=example_file_name_predictor,
        example_path_predictor=example_path_predictor,
        example_stream_predictor=example_stream_predictor,
    )


def read_usage_infromation():
    """Read the information from the usage_information.txt file."""
    with open("soil_moisture_prediction/usage_information.txt", "r") as f_handle:
        return f_handle.read()


if __name__ == "__main__":
    usage_information = compile_information()
    with open("README_template.md", "r") as f_handle:
        readme_template = f_handle.read()

    with open("README.md", "w") as f_handle:
        f_handle.write(
            readme_template.replace("usage_information_here", compile_information())
        )

    with open("soil_moisture_prediction/usage_information.txt", "w") as f_handle:
        f_handle.write(usage_information)

    print(usage_information)
