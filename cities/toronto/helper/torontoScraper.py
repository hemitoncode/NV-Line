from bs4 import BeautifulSoup
from globalStates import meetings, legislationDetailsHTML, meetingDetailsHTML, bills, fileLocaters

def scrapeCouncilMeetings(html):
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find('table', id='ctl00_ContentPlaceHolder1_gridCalendar_ctl00')

    if table:
        for tr in table.find_all('tr')[1:]:
            cells = tr.find_all('td')
            if len(cells) < 7:
                continue

            committee = cells[0].get_text(strip=True)
            date = cells[1].get_text(strip=True)
            meetingTime = cells[3].get_text(strip=True)

            if meetingTime == "Deferred":
                continue

            meetingDetail = cells[6].find('a')
            if not meetingDetail:
                continue

            meetings.append({
                "date": date,
                "committee": committee,
                "meetingDetails": meetingDetail['href']
            })

            print("Date:", date)
            print("Committee:", committee)
            print("Meeting details:", meetingDetail['href'])

            # Ignore after 2 meetings
            if len(meetings) >= 4:
                break
