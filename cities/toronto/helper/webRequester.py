from aiohttp import ClientSession
from tasksManager import getMeetingDetailsTasks, getLegislationDetailsTask
from globalStates import meetingDetailsHTML, legislationDetailsHTML
import asyncio

async def fetchCouncilMeetings():
    async with ClientSession() as session:
        async with session.get("https://secure.toronto.ca/council/#/highlights") as response:
            html = await response.text()
    return html

async def fetchMeetingDetails():
    async with ClientSession() as session:
        tasks = getMeetingDetailsTasks(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            html = await response.text()
            meetingDetailsHTML.append(html)


async def fetchLegislationDetails():
    async with ClientSession() as session:
        tasks = getLegislationDetailsTask(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            html = await response.text()
            legislationDetailsHTML.append(html)