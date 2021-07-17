import asyncio 

port=65432

async def tcp_echo_client(message, loop, port): 
    reader, writer = await asyncio.open_connection('127.0.0.1', port) 
    while 1:
        message=str(input())
        if message != '':
            writer.write(message.encode())

            data = await reader.read(1024)
            print('Received: %r' % data.decode())

message = 'Hello World!' 
loop = asyncio.get_event_loop()

loop.run_until_complete(tcp_echo_client(message, loop, port))

loop.close()