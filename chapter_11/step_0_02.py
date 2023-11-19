from pathlib import Path

OUTPUT_FOLDER = "output"

print(__file__)
print(__file__ + f"/{OUTPUT_FOLDER}")
print("/".join(__file__.split("/")[:-1]))
print("/".join(__file__.split("/")[:-1]) + f"/{OUTPUT_FOLDER}")

print(Path(__file__))
print(Path(__file__).parent)
print(Path(__file__).parent / OUTPUT_FOLDER)
