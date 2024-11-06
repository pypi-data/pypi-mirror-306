import argparse
import datasets
from pathlib import Path

from .inference import full_pipe
from .training.train import train


def inference():
    args = get_inference_args()
    full_pipe.main(
        args.input_path,
        args.output_dir,
        args.spans_model,
        args.labels_model,
        args.verbose,
        args.dry,
    )




def get_inference_args():
    """
    handles the argument parsing, when inference is run from the commandline
    return:
        parsed commandline arguments
    """
    arg_par = argparse.ArgumentParser(description="This is Argument Component - Identification and Classification expanding Stab and Gurevychs work on argument mining, and their paper from 2017 in particular. The inference pipeline requires two models that can be trained with the command AC-IaC-train, which is installed alongside AC-IaC.", epilog="")
    arg_par.add_argument(
        "--input_path",
        "-i",
        # default=Path("./data/genres_original/"),
        type=Path,
        required=True,
        help="path to the data directory containing the "
        + "text files, or singular text file, to process."
        + "for a directory, it will recursively find all txt"
        + "files and rebuild the input structure in the output.",
    )
    arg_par.add_argument(
        "--output_dir",
        "-o",
        # default=Path("./data/lyrics_original/"),
        required=True,
        type=Path,
        help="path to the directory to save the output.",
    )
    arg_par.add_argument(
        "--spans_model",
        "-s",
        # default="Theoreticallyhugo/longformer-spans",
        type=str,
        help="model to use for finding the spans."
        + "either path to local model or path of huggingface repository"
        + 'in the format of "user/model". '
        + 'for testing you can try to use "Theoreticallyhugo/longformer-spans, "'
        + "but proper availability is not guaranteed",
    )
    arg_par.add_argument(
        "--labels_model",
        "-l",
        # default="Theoreticallyhugo/longformer-sep_tok",
        type=str,
        help="model to use for labeling the spans. "
        + "either path to local model or path of huggingface repository "
        + 'in the format of "user/model". '
        + 'for testing you can try to use "Theoreticallyhugo/longformer-sep_tok, "'
        + "but proper availability is not guaranteed",
    )
    arg_par.add_argument(
        "--verbose",
        "-v",
        default=False,
        const=True,
        nargs="?",
        help="set this flag to increase verbosity",
    )
    arg_par.add_argument(
        "--dry",
        "-d",
        default=False,
        const=True,
        nargs="?",
        help="set this flag to run without inference",
    )

    args = arg_par.parse_args()
    return args

def train_wrapper():
    print("welcome to the training")
    args = get_train_args()
    # only spans and sep_tok are required for the pipe to work
    model_names = [
        "spans",
        "sep_tok",
        "all",
    ]

    assert args.model in model_names

    if args.model == "all":
        models = model_names[:-1]
    else:
        models = [args.model]

    for model in models:
        # five-fold-cross-validation
        print("loading data")
        tests_ds = datasets.load_dataset(
            "Theoreticallyhugo/Stab-Gurevych-Essays",
            model,
            split=[f"train[{k}%:{k+20}%]" for k in range(0, 100, 20)],
            trust_remote_code=True,
        )
        trains_ds = datasets.load_dataset(
            "Theoreticallyhugo/Stab-Gurevych-Essays",
            model,
            split=[f"train[:{k}%]+train[{k+20}%:]" for k in range(0, 100, 20)],
            trust_remote_code=True,
        )

        for train_ds, test_ds, index in zip(
            trains_ds, tests_ds, range(len(tests_ds))
        ):
            train(
                model,
                args.seed,
                args.epochs,
                train_ds,
                test_ds,
                index,
                args.output_dir,
                args.push,
            )
            if not args.cross_validation:
                break

def get_train_args():
    """
    handles the argument parsing, when main.py is run from the commandline
    :return: the arguments parsed from the command line input
    """
    arg_par = argparse.ArgumentParser()
    arg_par.add_argument(
        "--model",
        "-m",
        default="all",
        type=str,
        help="model to train",
    )
    arg_par.add_argument(
        "--epochs",
        "-e",
        default=5,
        type=int,
        help="number of epochs to train",
    )
    arg_par.add_argument(
        "--seed",
        "-s",
        default=42,
        type=int,
        help="seed to run the model with",
    )
    arg_par.add_argument(
        "--output_dir",
        "-o",
        # default=Path("./data/lyrics_original/"),
        required=True,
        type=Path,
        help="path to the directory to save the model(s).",
    )
    arg_par.add_argument(
        "--push",
        "-p",
        default=True,
        type=str,
        nargs='?',
        const=False,
        help="add tag to DISABLE PUSHING. \n"
        + "Pushing is enabled per default, but requires to be logged in via huggingface-cli",
    )
    arg_par.add_argument(
        "--cross_validation",
        "-cv",
        default=False,
        type=bool,
        nargs="?",
        const=True,
        help="add tag to ENABLE CROSS-VALIDATION.\n"
        + "cross-validation is disabled per default",
    )

    args = arg_par.parse_args()
    return args

# def main():
#     args = full_pipe.get_args()
#     full_pipe.main(
#         args.input_path,
#         args.output_dir,
#         args.spans_model,
#         args.labels_model,
#         args.verbose,
#         args.dry,
#     )
#
# if __name__ == "__main__":
#     main()
