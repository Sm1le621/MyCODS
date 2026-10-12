import asyncio
import httpx

async def  download(query, current_page):
    with open("Chit", "r") as f:
        data = f.read()
        print(data)
    header = {'Authorization':'mTW9uLxjOlpSjibmpgyh0lamqCzELczYYzbWNvj4Q4CfD3eBIzqHhxV3'}
    params = {'query':query, 'per_page':1, 'page':current_page}
    url = f"https://api.pexels.com/v1/search"

async def main():
    query = input("Seach: ")
    page_count = int(input("Count page: "))
    list_tusk = list()
    current_page = 0
    while current_page < page_count:
        current_page += 1
        tusk = asyncio.create_task(download(query, current_page))
        list_tusk.append(tusk)
        await download(query, current_page)
    await asyncio.gather(*list_tusk, return_exceptions=True)
    print("done!")
asyncio.run(main())

"""
async def my_sleep():
    print("start")
    await asyncio.sleep(2)
    print("end")

async def main():
    print("Sleep now!")
    await my_sleep()
    print("ok, wake up!")

asyncio.run(main())"""

