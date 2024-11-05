# next.py

An async library to interact with the https://next.avanpost20.ru API.

You can join the support server [here](https://app.avanpost20.ru/invite/Testers) and find the library's documentation [here](https://nextpy.readthedocs.io/en/latest/).

## Installing

You can use `pip` to install next.py. It differs slightly depending on what OS/Distro you use.

On Windows
```
py -m pip install -U next.py # -U to update
```

On macOS and Linux
```
python3 -m pip install -U next.py
```

## Example

More examples can be found in the [examples folder](https://github.com/avanpost200/next.py/blob/master/examples).

```py
import next
import asyncio

class Client(next.Client):
    async def on_message(self, message: next.Message):
        if message.content == "hello":
            await message.channel.send("hi how are you")

async def main():
    async with next.utils.client_session() as session:
        client = Client(session, "BOT TOKEN HERE")
        await client.start()

asyncio.run(main())
```
