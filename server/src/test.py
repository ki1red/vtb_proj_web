from modules.database import Database
import asyncio


async def main():
    db = Database()
    data = await db.get_records_by_atm_id(7)
    print(data)


if __name__ == "__main__":
    asyncio.run(main())
