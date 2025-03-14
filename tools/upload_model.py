import json
import shutil
from pathlib import Path
from typing import Any

import click
from kaggle.api.kaggle_api_extended import KaggleApi

def copy_files_with_exts(source_dir: Path, dest_dir: Path, exts: list):
    """
    source_dir: Starting directory to search
    dest_dir: destination directory
    exts: list of target extensions (e.g. ['.txt', '.jpg'])
    """

    # search for paths matching the each extension in source_dir
    for ext in exts:
        for source_path in source_dir.rglob(f"*{ext}"):
            # calculate relative paths in dest_dir
            relative_path = source_path.relative_to(source_dir)
            dest_path = dest_dir / relative_path

            # create destination directory if it doesn't exist
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # copy files
            shutil.copy2(source_path, dest_path)
            print(f"Copied {source_path} to {dest_path}")


@click.command()
@click.option("--title", "-t", default="abf-model")
@click.option("--dir", "-d", type=Path, default="./output/experiments")
@click.option(
    "--extentions",
    "-e",
    type=list[str],
    default=["best_model.pt", ".hydra/*.yaml"],
)
@click.option("--user_name", "-u", default="alvaroborras")
@click.option("--new", "-n", is_flag=True)
def main(
    title: str,
    dir: Path,
    extentions: list[str] = [".pth", ".yaml"],
    user_name: str = "alvaroborras",
    new: bool = False,
):
    """ Specify extention, zip the files under dir, and upload them to kaggle.
        title (str): Title of the file to upload to kaggle
        dir (Path): Directory containing the files to be uploaded
        extensions (list[str], optional): extensions of files to upload.
        user_name (str, optional): kaggle user name.
        new (bool, optional): whether to upload as a new dataset.
    """
    tmp_dir = Path("./tmp")
    tmp_dir.mkdir(parents=True, exist_ok=True)

    # 拡張子が.pthのファイルをコピー
    copy_files_with_exts(dir, tmp_dir, extentions)

    # dataset-metadata.jsonを作成
    dataset_metadata: dict[str, Any] = {}
    dataset_metadata["id"] = f"{user_name}/{title}"
    dataset_metadata["licenses"] = [{"name": "CC0-1.0"}]
    dataset_metadata["title"] = title
    with open(tmp_dir / "dataset-metadata.json", "w") as f:
        json.dump(dataset_metadata, f, indent=4)

    # api認証
    api = KaggleApi()
    api.authenticate()

    if new:
        api.dataset_create_new(
            folder=tmp_dir,
            dir_mode="tar",
            convert_to_csv=False,
            public=False,
        )
    else:
        api.dataset_create_version(
            folder=tmp_dir,
            version_notes="",
            dir_mode="tar",
            convert_to_csv=False,
        )

    # delete tmp dir
    shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    main()
