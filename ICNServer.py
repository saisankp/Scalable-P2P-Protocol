import asyncio
import json

class ICNServer:
    def __init__(self, port):
        self.port = port
        self.nodes = {}

    async def handle_connection(self, reader, writer):
        address = writer.get_extra_info('peername')
        print(f"Node connected: {address}")

        # Inform all connected nodes about the new node
        for node_writer in self.nodes.values():
            try:
                node_writer.write(f"New node connected: {address}".encode())
                await node_writer.drain()
            except asyncio.CancelledError:
                pass

        self.nodes[address] = writer

        try:
            while True:
                data = await reader.read(100)
                if not data:
                    break

                message = data.decode()
                print(f"Received message from {address}: {message}")
                await self.process_message(address, message)

        except asyncio.CancelledError:
            pass
        finally:
            del self.nodes[address]

            # Inform all connected nodes about the disconnected node
            for node_writer in self.nodes.values():
                try:
                    node_writer.write(f"Node disconnected: {address}".encode())
                    await node_writer.drain()
                except asyncio.CancelledError:
                    pass

            print(f"Node disconnected: {address}")
            writer.close()
            await writer.wait_closed()

    async def process_message(self, sender_address, message):
        # Implement your message processing logic here
        # For example, broadcasting the message to all connected nodes
        for address, node_writer in self.nodes.items():
            if address != sender_address:
                try:
                    node_writer.write(message.encode())
                    await node_writer.drain()
                except asyncio.CancelledError:
                    pass

    async def run(self):
        server = await asyncio.start_server(
            self.handle_connection, '127.0.0.1', self.port)

        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    port = 8000  # Change this to the desired port
    icn_server = ICNServer(port)
    asyncio.run(icn_server.run())
