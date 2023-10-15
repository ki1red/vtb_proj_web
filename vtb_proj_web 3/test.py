from modules.database import Database
from modules import utils
import asyncio


async def main():
    time = "17:59"
    for atm in range(1, 10):
        data = await utils.workload_atm(atm)
        print(f"Банкомат {atm} {time} загруженность", data)


if __name__ == "__main__":
    asyncio.run(main())
