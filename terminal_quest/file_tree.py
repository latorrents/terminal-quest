# file_tree.py
#
# Crea en disco el mundo del juego a partir de los árboles de story/trees.
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

import filecmp
import os
import shutil
import stat

from terminal_quest.common import fake_home_dir, tq_file_system, get_story_file


class FileTree:
    KEY_PERMISSIONS = "permissions"
    KEY_NAME = "name"
    KEY_CHILDREN = "children"
    KEY_TYPE = "type"
    KEY_CONTENTS = "contents"
    KEY_CHALLENGES = "challenges"
    KEY_CHALLENGE = "challenge"
    KEY_STEP = "step"
    KEY_EXISTS = "exists"
    TYPE_DIR = "directory"
    TYPE_FILE = "file"
    DEFAULT_DIR_PERMISSIONS = 0o755
    DEFAULT_FILE_PERMISSIONS = 0o644

    def __init__(self, tree, end_dir):
        self.__tree = tree
        self.__end_dir = end_dir
        self.__create_dir(end_dir, 0o755)

    def parse_complete(self, challenge, step):
        self.__clear_old_tree()
        self.__parse(self.__tree, self.__end_dir, challenge, step)

    def create_item(self, item_type, path, permissions, contents_path):
        path = os.path.join(self.__end_dir, path)
        self.__create_item(item_type, path, permissions, {self.KEY_CONTENTS: contents_path})

    def __clear_old_tree(self):
        revert_to_default_permissions(self.__end_dir)
        delete_item(self.__end_dir)
        os.makedirs(self.__end_dir)

    def __parse(self, tree, path, challenge, step):
        if "name" not in tree:
            raise Exception("No name for component in tree")

        challenge_data = self.__specs_for_challenge(challenge, step, tree)
        if not self.__exists_in_current_challenge(challenge_data):
            return

        path = os.path.join(path, tree[self.KEY_NAME])
        item_type = self.__get_item_type(tree)
        permissions = self.__get_permissions(challenge_data, item_type)
        self.__create_item(item_type, path, permissions, tree)

        for child_tree in tree.get(self.KEY_CHILDREN, []):
            self.__parse(child_tree, path, challenge, step)

    def __create_item(self, item_type, path, permissions, tree):
        parent_dir = os.path.normpath(os.path.join(path, ".."))

        if not os.path.exists(parent_dir):
            self.__create_dir(parent_dir, 0o755)

        mode = os.stat(parent_dir).st_mode
        permissions_changed = self.__make_parent_writable(parent_dir, mode)

        if item_type == self.TYPE_DIR:
            self.__create_dir(path, permissions)
        elif item_type == self.TYPE_FILE:
            self.__create_file(path, permissions, self.__get_contents_path(tree))

        if permissions_changed:
            os.chmod(parent_dir, stat.S_IMODE(mode))

    def __exists_in_current_challenge(self, challenge_data):
        if self.KEY_CHALLENGE not in challenge_data and self.KEY_STEP not in challenge_data:
            return True
        return challenge_data.get(self.KEY_EXISTS, True)

    def __specs_for_challenge(self, challenge, step, tree):
        if self.KEY_CHALLENGES not in tree:
            return tree

        challenge_data = {}
        for challenge_dict in tree[self.KEY_CHALLENGES]:
            if self.KEY_CHALLENGE not in challenge_dict or self.KEY_STEP not in challenge_dict:
                raise Exception("missing challenge key in " + str(challenge_dict))
            poss_challenge = challenge_dict["challenge"]
            poss_step = challenge_dict["step"]
            if (poss_challenge <= challenge and poss_step <= step) or (poss_challenge < challenge):
                challenge_data = challenge_dict

        if self.KEY_PERMISSIONS in tree:
            challenge_data[self.KEY_PERMISSIONS] = tree[self.KEY_PERMISSIONS]

        return challenge_data

    @staticmethod
    def __create_dir(path, permissions):
        if os.path.exists(path) and not os.path.isdir(path):
            raise Exception("File " + path + " exists and should be a directory")
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            os.chmod(path, permissions)

    @staticmethod
    def __create_file(path, permissions, src_path):
        if os.path.isdir(path):
            raise Exception("File " + path + " exists and should be a file")
        if os.path.exists(path) and not filecmp.cmp(path, src_path, shallow=False):
            os.remove(path)

        shutil.copyfile(src_path, path)
        os.chmod(path, permissions)

    @staticmethod
    def __make_parent_writable(parent_dir, mode):
        if (mode & stat.S_IWUSR) and (mode & stat.S_IXUSR):
            return False
        os.chmod(parent_dir, 0o755)
        return True

    def __get_permissions(self, challenge_data, item_type):
        if self.KEY_PERMISSIONS in challenge_data:
            return challenge_data[self.KEY_PERMISSIONS]
        if item_type == self.TYPE_DIR:
            return self.DEFAULT_DIR_PERMISSIONS
        return self.DEFAULT_FILE_PERMISSIONS

    def __get_item_type(self, tree):
        if self.KEY_CHILDREN in tree or tree.get(self.KEY_TYPE) == self.TYPE_DIR:
            return self.TYPE_DIR
        return self.TYPE_FILE

    def __get_contents_path(self, tree):
        if self.KEY_CONTENTS not in tree:
            raise Exception("No contents associated with the file: " + tree["name"])
        return tree[self.KEY_CONTENTS]


def delete_item(path):
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    elif os.path.lexists(path):
        os.remove(path)


def revert_to_default_permissions(filesystem):
    if not os.path.isdir(filesystem):
        return
    os.chmod(filesystem, 0o755)
    for root, dirs, files in os.walk(filesystem):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o755)
        for f in files:
            os.chmod(os.path.join(root, f), 0o644)


def get_oct_permissions(path):
    return oct(os.stat(path).st_mode & 0o777)


def get_int_permissions(path):
    return int(os.stat(path).st_mode & 0o777)


def delete_items(items):
    for path in items or []:
        delete_item(path.replace('~', fake_home_dir, 1))


def modify_permissions(fake_path, permission):
    os.chmod(fake_path.replace('~', fake_home_dir, 1), permission)


def modify_file_tree(items):
    if not items:
        return

    file_tree = FileTree(None, tq_file_system)
    for f in items:
        if "path" not in f:
            raise Exception("Not all info available for item " + str(f))
        f.setdefault("type", "file")
        if f["type"] == "file" and "contents" not in f:
            f["contents"] = get_story_file(f["path"].split("/")[-1])

        if f["type"] == "directory":
            f["contents"] = ""
            f.setdefault("permissions", 0o755)
        else:
            f.setdefault("permissions", 0o644)

        file_tree.create_item(f["type"], f["path"], f["permissions"], f["contents"])
