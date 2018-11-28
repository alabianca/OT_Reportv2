

from bs4 import BeautifulSoup
import glob


def summary_v1(tbody):
    # wtf
    row = tbody.contents[2].contents[0].contents[0].contents[0].contents[0]

    # print(row.contents[2].contents)
    summary = {
        "date": row.contents[1].contents[0].text,
        "time": row.contents[2].contents[0].text,
        "coach": row.contents[3].contents[0].text,
        "template_version": 1
    }

    return summary

def summary_v2(tbody):
    summary = {}
    row = tbody.contents[2].contents[0].contents[0].contents[0].contents[0]

    summary["date"] = tbody.contents[0].contents[0].text
    summary["time"] = row.contents[1].contents[0].text
    summary["coach"] = row.contents[3].contents[0].text
    summary["template_version"] = 2

    return summary

def print_summary(total,errors):
    print("Parsed {} files".format(total))
    print("Successfully parsed {} files".format(total-errors))
    print("Errors: {}".format(errors))



class HtmlReader:

    def __init__(self):
        self.total = 0
        self.errors = 0

    def get_this_class_data(self, summary_table):

        row = summary_table.contents[0].contents #tr that contains the THIS CLASS data

        this_class = {
            "calories": row[1].text,
            "splat_pts": row[2].text,
            "steps": row[3].text
        }
        return this_class

    #get the coach name, date and time
    def get_summary(self, soup):
        block_table = soup.find('table', attrs={'class': 'bg-gradient-red-orange'})

        #find table that contains the data
        workout_summary_table = block_table.contents[0].contents[0].contents[1].contents[0]

        tbody = workout_summary_table.contents[0]


        v1_id = tbody.contents[0].contents[0].text

        # the OT_REPORT template has changed slightly over the past few months
        # the summary is in different places for each type of template

        if v1_id == 'STUDIO WORKOUT SUMMARY'.upper():
            return summary_v1(tbody)
        else:
            return summary_v2(tbody)






    def get_cardio(self, soup):
        block_table = soup.find('table', attrs={"class": "splats-bottom"}).contents[0].contents[0].contents[0].contents[0]
        tbody = block_table.contents[0]
        row = tbody.contents[0]
        column_with_cardio_info = row.contents[0]

        cardio_table = column_with_cardio_info.contents[0]
        tbody = cardio_table

        cardio = {
            "avg_heart_rate": tbody.contents[1].contents[0].contents[0].text,
            "peak_heart_rate": tbody.contents[3].contents[0].contents[0].contents[1].string
        }



        return cardio





    # reads all html files in a given directory and scrapes them
    # we return the aggregated data as a dictionary called 'event'
    # an event has the following keys: calories,splat_pts,steps,date,time,coach,template_version,avg_heart_rate,peak_heart_rate
    # these keys are currently found in 3 different sections
    #   1. this_class: the THIS CLASS row in the summary table
    #   2. summary: data about date, time and coach
    #   3. cardio: max and average heart rate data found in the tiles of the email template
    def read_all(self, directory):

        files = glob.glob(directory)
        self.total = len(files)
        events = []
        for i,fh in enumerate(files):

            file_handle = open(fh)

            soup = BeautifulSoup(file_handle, 'html.parser')

            summary_table = soup.find('tbody', attrs={'class': 'summary-table'})

            if(not summary_table):
                print("Could not parse {}".format(fh))
                print("Could not locate summary table")

                self.errors += 1
                continue

            this_class = self.get_this_class_data(summary_table)
            summary = self.get_summary(soup)
            cardio = self.get_cardio(soup)



            event = {
                **this_class,
                **summary,
                **cardio
            }
            events.append(event)
            file_handle.close()

        print_summary(self.total,self.errors)

        return events

