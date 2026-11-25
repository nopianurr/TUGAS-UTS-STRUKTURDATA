import asyncio


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.condition = asyncio.Condition()

    async def enqueue(self, data):
        node = Node(data)

        async with self.condition:
            if self.rear is None:
                self.front = node
                self.rear = node
            else:
                self.rear.next = node
                self.rear = node

            self.condition.notify()

    async def dequeue(self):
        async with self.condition:
            while self.front is None:
                await self.condition.wait()

            data = self.front.data
            self.front = self.front.next

            if self.front is None:
                self.rear = None

            return data


class PythonQueue:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def enqueue(self, data):
        await self.queue.put(data)

    async def dequeue(self):
        return await self.queue.get()
