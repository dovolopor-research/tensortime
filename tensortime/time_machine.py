from pathlib import Path
from time import ctime
from shutil import copy
from shutil import copytree


class TimeMachine(object):
    def __init__(self, backup_dir: str = None, exp_dir: str = None, exp_suffix: str = None) -> None:
        if backup_dir is None:
            backup_dir = "tensortime"
        self.backup_path = Path(backup_dir)

        if exp_dir is None:
            if exp_suffix is None:
                exp_suffix = input(">> tensortime: 输入实验备注 ")

            if len(exp_suffix):
                self.exp_path = self.backup_path / (ctime().replace(" ", "_") + f"-{exp_suffix}")
            else:
                self.exp_path = self.backup_path / ctime().replace(" ", "_")
        else:
            self.exp_path = self.backup_path / exp_dir

        self.project_path = Path(".")
        self.ignore_path = Path(".ttignore")
        self.ignore_list = [backup_dir]
        self.add_list = []

    def backup(self, ignore: list = None, add: list = None) -> None:
        self.__check_path()
        if add is not None:
            self.add_list = add
            self.__move_file_by_add()
        else:
            self.__check_ignore(ignore)
            self.__move_file_by_ignore()

    def __check_path(self) -> None:
        if not self.backup_path.exists():
            self.backup_path.mkdir()
            print(f">> tensortime: 创建备份文件夹 {self.backup_path.name}")

        if not self.exp_path.exists():
            self.exp_path.mkdir()
            print(f">> tensortime: 创建实验文件夹 {self.exp_path.name}")

    def __check_ignore(self, ignore: list) -> None:
        if ignore is not None:
            self.ignore_list += ignore

        if self.ignore_path.exists():
            with open(self.ignore_path, "r") as f_ttig:
                ttig_list = []
                for ig_item in f_ttig.readlines():
                    ig_item = ig_item.strip()
                    if len(ig_item) and ig_item[0] != "#":
                        ttig_list.append(ig_item)
                self.ignore_list += ttig_list

    def __move_file_by_ignore(self) -> None:
        for exp_file in self.project_path.glob("*"):
            if str(exp_file) not in set(self.ignore_list):
                origin_path = self.project_path / exp_file
                target_path = self.exp_path / exp_file
                if origin_path.is_file():
                    copy(origin_path, target_path)
                    print(f">> tensortime: 备份文件 {exp_file}")
                elif origin_path.is_dir():
                    copytree(origin_path, target_path)
                    print(f">> tensortime: 备份文件夹 {exp_file}")
                else:
                    print(f"!! tensortime: 未找到 {exp_file}")
            else:
                print(f">> tensortime: 忽略 {exp_file}")

        print(f">> tensortime: 成功备份到 {self.exp_path}")

    def __move_file_by_add(self) -> None:
        for exp_file in self.add_list:
            origin_path = self.project_path / exp_file
            target_path = self.exp_path / exp_file
            if origin_path.is_file():
                copy(origin_path, target_path)
                print(f">> tensortime: 备份文件 {exp_file}")
            elif origin_path.is_dir():
                copytree(origin_path, target_path)
                print(f">> tensortime: 备份文件夹 {exp_file}")
            else:
                print(f"!! tensortime: 未找到 {origin_path}")

        print(f">> tensortime: 成功备份到 {self.exp_path}")
