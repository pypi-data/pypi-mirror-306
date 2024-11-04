from src.config import STORAGE_DIR
from src.kondar import KondarGuard


def main():
    try:
        kondar = KondarGuard(STORAGE_DIR)
        kondar.run()

    except KeyboardInterrupt:
        print("Kondar guard was stopped. Goodbye!")


if __name__ == "__main__":
    main()
