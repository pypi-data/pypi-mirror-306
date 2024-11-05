# utils.py
#
# Copyright (c) 2024 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from dataclasses import dataclass

from django.apps import apps
from django.core.files.storage import Storage, default_storage
from django.db.models import FileField


@dataclass
class DirectoryTree:
    """This dataclass is used as Storage backends in Django are not
    guaranteed to support os.walk type functionality.
    """

    path: str
    files: list[str]
    children: list["DirectoryTree"]

    def add_child(self, child_name: str, storage: Storage = default_storage) -> None:
        child_path = (
            f"{self.path}/{child_name}" if self.path not in ["", "/"] else child_name
        )
        child = DirectoryTree(path=child_path, files=[], children=[])
        directories, files = storage.listdir(child_path)
        child.files = files
        for directory in directories:
            child.add_child(directory, storage=storage)
        self.children.append(child)

    def get_file_paths(self) -> list[str]:
        file_paths = [
            f"{self.path}/{file}" if file != "" else file for file in self.files
        ]
        for child in self.children:
            file_paths += child.get_file_paths()
        return file_paths

    def get_empty_child_directories(self) -> list[str]:
        if len(self.children) == 0:
            return []
        empty_directories = []
        for child in self.children:
            if not child.files and not child.children:
                empty_directories.append(child.path)
            else:
                empty_directories += child.get_empty_child_directories()
        return empty_directories


def get_all_file_fields() -> list[tuple[str, str, str]]:
    file_fields = []
    for app, model_dict in apps.all_models.items():
        if model_dict:
            for model_name, model in model_dict.items():
                for field in model._meta.fields:
                    if isinstance(field, FileField):
                        file_fields.append((app, model_name, field.name))
    return file_fields


def get_referenced_file_paths(fields: list[tuple[str, str, str]]) -> list[str]:
    filepaths = []
    for model_spec in fields:
        app_label = model_spec[0]
        model_name = model_spec[1]
        field_name = model_spec[2]
        model = apps.get_model(app_label=app_label, model_name=model_name)
        filepaths += model.objects.filter(
            **{f"{field_name}__isnull": False}
        ).values_list(field_name, flat=True)
    return filepaths


def get_media_paths(storage_backend: Storage = default_storage) -> list[str]:
    dirs, files = storage_backend.listdir(".")
    dir_tree = DirectoryTree(path="", files=files, children=[])
    for directory in dirs:
        dir_tree.add_child(directory, storage=storage_backend)
    return dir_tree.get_file_paths()


def get_unreferenced_media_paths(
    storage_backend: Storage = default_storage,
) -> list[str]:
    media_paths = get_media_paths(storage_backend=storage_backend)
    return [
        path
        for path in media_paths
        if path not in get_referenced_file_paths(get_all_file_fields())
    ]


def get_empty_media_directories(
    storage_backend: Storage = default_storage,
) -> list[str]:
    dirs, files = storage_backend.listdir(".")
    dir_tree = DirectoryTree(path="", files=files, children=[])
    for directory in dirs:
        dir_tree.add_child(directory, storage=storage_backend)
    return dir_tree.get_empty_child_directories()
