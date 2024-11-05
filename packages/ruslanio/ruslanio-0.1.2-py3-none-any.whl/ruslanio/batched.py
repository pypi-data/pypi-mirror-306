import asyncio
from asyncio import Queue, Future


class batched:
    def __init__(self, func, batch_size=16, timeout=0.5):
        self.func = func
        self.batch_size = batch_size
        self.timeout = timeout
        self.input_q = Queue()
        self.output_q = Queue()
        asyncio.create_task(self._batching_worker())
        asyncio.create_task(self._waiter_worker())
        self.batch = []

    async def _batching_worker(self):
        while True:
            timed_out = False
            try:
                item = await asyncio.wait_for(self.input_q.get(), self.timeout)
                self.batch.append(item)
            except TimeoutError:
                timed_out = True

            if len(self.batch) >= self.batch_size or (len(self.batch) != 0 and timed_out):
                inputs = [pair[0] for pair in self.batch]
                futures = [pair[1] for pair in self.batch]
                asyncio.create_task(self._task(inputs, futures))
                self.batch = []

    async def _task(self, inputs, futures):
        results = await self.func(inputs)
        await self.output_q.put((results, futures))

    async def _waiter_worker(self):
        while True:
            futures: list[Future]
            results, futures = await self.output_q.get()
            for (result, future) in zip(results, futures):
                future.set_result(result)

    async def __call__(self, item):
        future = Future()
        await self.input_q.put((item, future))
        return await future


async def main():
    # Example usage
    async def my_batched_function(item_id_batch):
        await asyncio.sleep(1)
        print(f'called for {item_id_batch[0]}..{item_id_batch[-1]}')
        return [f'result_for_{item_id}' for item_id in item_id_batch]


    f = batched(my_batched_function, batch_size=10)

    all_item_ids = range(99)

    results = await asyncio.gather(*[f(item_id) for item_id in all_item_ids])
    print(results)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())