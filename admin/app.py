from src.web import create_app
from pathlib import Path


static_folder = Path(__file__).parent.absolute().joinpath("src/web/public")

app = create_app( static_folder=static_folder)
# env='production',
def main():
    app.run()

if __name__ == "__main__":
    main()