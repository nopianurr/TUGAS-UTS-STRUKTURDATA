import asyncio
import gc
import time
import tracemalloc
import statistics

from queue_implementation import LinkedQueue, PythonQueue


async def run_pipeline(queue, jumlah):
    async def producer():
        for i in range(jumlah):
            await queue.enqueue(i)

    async def consumer():
        for _ in range(jumlah):
            await queue.dequeue()

    await asyncio.gather(producer(), consumer())


async def ukur_waktu(queue_class, jumlah):
    hasil = []

    for _ in range(3):
        gc.collect()
        queue = queue_class()

        mulai = time.perf_counter()
        await run_pipeline(queue, jumlah)
        selesai = time.perf_counter()

        hasil.append(selesai - mulai)

    return statistics.median(hasil)


async def ukur_memori(queue_class, jumlah):
    hasil = []

    for _ in range(3):
        gc.collect()
        queue = queue_class()

        tracemalloc.start()
        try:
            await run_pipeline(queue, jumlah)
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()

        hasil.append(peak / 1024)

    return statistics.median(hasil)


async def pengujian():
    jumlah_data = [
        5, 25, 125, 625, 3125, 15625, 78125, 390625
    ]

    hasil = []

    print("\nMEMULAI PENGUJIAN QUEUE")
    print("=" * 65)

    for jumlah in jumlah_data:
        print(f"\nMenguji {jumlah:,} data...")

        waktu_linked = await ukur_waktu(LinkedQueue, jumlah)
        waktu_asyncio = await ukur_waktu(PythonQueue, jumlah)

        memori_linked = await ukur_memori(LinkedQueue, jumlah)
        memori_asyncio = await ukur_memori(PythonQueue, jumlah)

        hasil.append([
            jumlah,
            waktu_linked,
            waktu_asyncio,
            memori_linked,
            memori_asyncio
        ])

        print(f"Linked Queue  : {waktu_linked:.6f} detik")
        print(f"asyncio.Queue : {waktu_asyncio:.6f} detik")
        print(f"Memori Linked : {memori_linked:.2f} KB")
        print(f"Memori asyncio: {memori_asyncio:.2f} KB")

    return hasil
