import os
import sys
from getpass import getpass
from pathlib import Path
from typing import Callable

from colorama import Fore, Style

from src.config import CRYPT_MODES, CryptModeCode
from src.crypt import MemoryCrypter


class KondarGuard:
    def __init__(
        self,
        storage_dir: Path
    ):
        self.__storage_dir = storage_dir
        self.prepare()

    def prepare(self) -> None:
        """ prepare program to working """

        if not os.path.exists(self.__storage_dir):
            os.mkdir(self.__storage_dir)

    @staticmethod
    def alarm(
        parent_func: Callable,
        text: str,
        clear_console: bool = True,
        kwargs: dict | None = None,
    ):
        """ clear console output and show message """

        if clear_console:
            os.system("export TERM=xterm && clear")

        print(Fore.RED + f"{text} \n", Style.RESET_ALL)

        return parent_func(**kwargs or {})

    def input_file_name(self) -> Path:
        tips = os.listdir(self.__storage_dir)
        path_or_filename = input(
            f"Move file to directory «{self.__storage_dir}» "
            f"(existed objects: {', '.join(tips) or 'not founded'}) "
            f"and enter file name with extension. "
            f"If you want work with fill in specific directory, "
            f"pass full path to needed file\n>>> ",
        ).strip()

        if Path(path_or_filename).is_absolute():
            return Path(path_or_filename)

        if path_or_filename in os.listdir(self.__storage_dir):
            return self.__storage_dir / path_or_filename

        return self.alarm(
            parent_func=self.input_file_name,
            text=f"File «{path_or_filename}» not existed in "
                 f"{self.__storage_dir} and path not is absolute. "
                 f"Try again... "
        )

    def input_password(self, with_matching: bool = False) -> str:
        password1 = getpass(prompt=f"{'-' * 24}\n"f"Enter password >>> ")
        if not with_matching:
            return password1

        password2 = getpass(prompt=f"{'-' * 24}\n"f"Retype password >>> ")
        if password1 != password2:
            return self.alarm(
                self.input_password, f"Passwords do not match",
                kwargs={"with_matching": with_matching}
            )

        return password1

    def ask_for_next_iteration(self):
        action = input(
            "[1] — next\n"
            "[2] — quit\n"
            ">>> "
        )
        if action in {"1", "2"}:
            return True if action == "1" else sys.exit(0)

        return self.alarm(self.ask_for_next_iteration, text=f"Incorrect argument")

    def run(self):
        raw_text = [f"[{k}] — {v.description}" for k, v in CRYPT_MODES.items()]
        textarea = "\n".join(raw_text)
        mode_number = input(f"{textarea}\n Enter action number >>> ")

        formatted_keys = list(CRYPT_MODES.keys())
        if mode_number not in formatted_keys:
            return self.alarm(self.run, f"Action number must have one of digits: {formatted_keys}")

        file_path = self.input_file_name()

        match CRYPT_MODES.get(mode_number).code:
            case CryptModeCode.ENCRYPT_IN_MEMORY:
                crypter = MemoryCrypter(file_path, self.input_password(with_matching=True))
                crypter.encrypt_file()

            case CryptModeCode.DECRYPT_IN_MEMORY:
                crypter = MemoryCrypter(file_path, self.input_password())
                crypter.decrypt_file()

        if self.ask_for_next_iteration():
            return self.run()
