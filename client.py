import asyncio


async def send_messages(writer):
    name = input("Enter your name: ")
    writer.write(name.encode() + b"\n")
    await writer.drain()

    while True:
        destination = input("Enter recipient name(s) separated by commas: ")
        message = input("Enter message: ")
        formatted_message = f"{destination}: {message}"
        writer.write(formatted_message.encode() + b"\n")
        await writer.drain()


async def receive_messages(reader):
    while True:
        message = await reader.readline()
        if not message:
            break
        print(message.decode().rstrip())


async def main():
    try:
        reader, writer = await asyncio.open_connection('10.10.100.136', 8080)
        print("Connected to the Rust server.")

        send_task = asyncio.create_task(send_messages(writer))
        receive_task = asyncio.create_task(receive_messages(reader))

        await asyncio.gather(send_task, receive_task)
    except (OSError, asyncio.TimeoutError):
        print("Connection to the server failed.")

if __name__ == "__main__":
    asyncio.run(main())
