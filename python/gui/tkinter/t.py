import time

import ttkbootstrap as ttk
from queue import Queue
from threading import Thread
import asyncio


def start():
    asyncio.gather(working())
    p.start()
    listen()


async def working():
    await asyncio.sleep(2)
    global workdone
    workdone = True


def listen():
    if workdone:
        p.stop()
    app.after(50, listen)


if __name__ == '__main__':
    workdone = False
    app = ttk.Window()
    q = Queue()
    p = ttk.Progressbar(
        master=app,
        maximum=10,
        bootstyle='success',
        mode='indeterminate',
    )
    p.pack(fill='x', expand=True)

    start_btn = ttk.Button(
        master=app,
        text='START',
        command=start
    )
    start_btn.pack(fill='x', pady=10)

    app.mainloop()
