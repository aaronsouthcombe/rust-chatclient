import asyncio
import sys


async def send_messages(writer):
    while True:
        message = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        if not message:
            break
        writer.write(message.encode() + b"\n")
        await writer.drain()


async def receive_messages(reader):
    while True:
        message = await reader.readline()
        if not message:
            break
        print(message.decode().rstrip())


async def main():
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8080)
        print("Connected to the Rust server.")

        send_task = asyncio.create_task(send_messages(writer))
        receive_task = asyncio.create_task(receive_messages(reader))

        await asyncio.gather(send_task, receive_task)
    except (OSError, asyncio.TimeoutError):
        print("Connection to the server failed.")

if __name__ == "__main__":
    asyncio.run(main())
