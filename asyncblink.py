import uasyncio as asyncio

async def blink(led, period_ms):
    while True:
        led.on()
        await asyncio.sleep_ms(5)
        led.off()
        await asyncio.sleep_ms(period_ms)

async def main(led1, led2):
    asyncio.create_task(blink(led1, 700))
    asyncio.create_task(blink(led2, 400))
    await asyncio.sleep_ms(10_000)


# Running on a generic board
from machine import Pin
asyncio.run(main(Pin(1), Pin(2)))
