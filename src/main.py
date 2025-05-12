# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/hi_{name}")
def print_hi(name: str):
    # Use a breakpoint in the code line below to debug your script.
    return (f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
