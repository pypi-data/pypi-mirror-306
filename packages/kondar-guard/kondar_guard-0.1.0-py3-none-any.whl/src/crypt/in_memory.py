import io
import json
from getpass import getpass
from pathlib import Path

import pyAesCrypt


class MemoryCrypter:
    def __init__(
        self,
        file_path: Path,
        password: str,
        buffer_size: int = 512 * 1024
    ):
        self.__file_path = file_path
        self.__password = password
        self.buffer_size = buffer_size

    @property
    def file_content(self) -> io.BytesIO:
        with open(self.__file_path, "rb") as file:
            return io.BytesIO(file.read())

    @property
    def sequence_bytes(self):
        return io.BytesIO()

    def encrypt_file(self):
        sequence_bytes = self.sequence_bytes
        pyAesCrypt.encryptStream(
            fIn=self.file_content,
            fOut=sequence_bytes,
            passw=self.__password,
            bufferSize=self.buffer_size
        )
        self.rewrite_file_and_flush(sequence_bytes)
        print("File successful encrypted!\n")

    def decrypt_file(self):
        sequence_bytes = self.sequence_bytes
        try:
            pyAesCrypt.decryptStream(
                fIn=self.file_content,
                fOut=sequence_bytes,
                passw=self.__password,
                bufferSize=self.buffer_size
            )
        except ValueError:
            password = getpass("Wrong password! Try again or type «q»\n>>> ")
            if password in ["q", "exit"]:
                return

            self.__password = password
            return self.decrypt_file()

        self.rewrite_file_and_flush(sequence_bytes)
        print("File successful decrypted!\n")

    def rewrite_file_and_flush(self, sequence_bytes):
        with open(self.__file_path, "wb") as file:
            file.seek(0)
            file.write(sequence_bytes.getvalue())
        self.sequence_bytes.flush()


class JsonMemoryCrypter(MemoryCrypter):
    # In progress

    def __init__(
        self,
        file_path: Path,
        password: str,
        buffer_size: int = 512 * 1024
    ):
        self.__file_path = file_path
        self.__password = password
        self.buffer_size = buffer_size
        super().__init__(file_path, password, buffer_size)

    def add_secret_pair(self, key, value):
        self.decrypt_file()

        with open(self.__file_path, "r+") as file:
            json_data = json.loads(file.read())
            json_data[key] = value
            file.seek(0)
            file.write(json.dumps(json_data, ensure_ascii=False, indent=4))

        self.encrypt_file()

    def remove_secret_pair(self, key):
        self.decrypt_file()

        with open(self.__file_path, "r+") as file:
            json_data = json.loads(file.read())
            del json_data[key]
            file.seek(0)
            file.write(json.dumps(json_data, ensure_ascii=False, indent=4))

        self.encrypt_file()
