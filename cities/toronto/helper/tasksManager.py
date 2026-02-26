from globalStates import meetings, fileLocaters, bills
from helper.ai.aiUtils import runAIOnBill

def getMeetingDetailsTasks(session):
    tasks = []
    for meeting in meetings:
        tasks.append(session.get(f"https://secure.toronto.ca/council/#/committees/{meeting['meetingDetails']}", ssl=False))
    return tasks


def getLegislationDetailsTask(session):
    tasks = []
    for fileLocator in fileLocaters:
        tasks.append(session.get(f"https://secure.toronto.ca/council/agenda-item.do?item={fileLocator}", ssl=False))
    return tasks


def getAITasks():
    tasks = []
    for bill in bills:
        tasks.append(runAIOnBill(bill))
    return tasks
