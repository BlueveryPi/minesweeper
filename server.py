import asyncio, socket

async def handle_client(client):
    loop = asyncio.get_event_loop()
    request=''
    while request != 'quit':
        request = (await loop.sock_recv(client, 1024)).decode('utf8')
        print('Received: ', request)
        await loop.sock_sendall(client, request.encode('utf8'))
    client.close()

async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 65432))
    server.listen(8)
    server.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        client, _ = await loop.sock_accept(server)
        loop.create_task(handle_client(client))

        '''''
        while 1:
            message=str(input())
            if message != '':
                await loop.sock_sendall(client, message.encode('utf8'))
            else:
                message=str(input())
                '''

asyncio.run(run_server())