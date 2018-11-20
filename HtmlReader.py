

from bs4 import BeautifulSoup
import glob

class HtmlReader:

    def __init__(self):
        self.file = './htmlFilesv2/OTReport_166a63095fc16625.html'

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

        #wtf
        row = tbody.contents[2].contents[0].contents[0].contents[0].contents[0]

        print(row.contents[2].contents)
        summary = {
            "date": row.contents[1].contents[0].text,
            "time": row.contents[2].contents[0].text,
            "coach":row.contents[3].contents[0].text
        }

        return summary


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





    def read_all(self, directory):

        files = glob.glob(directory)

        for i,fh in enumerate(files):

            file_handle = open(fh)

            soup = BeautifulSoup(file_handle, 'html.parser')

            summary_table = soup.find('tbody', attrs={'class': 'summary-table'})

            this_class = self.get_this_class_data(summary_table)
            summary    = self.get_summary(soup)
            cardio     = self.get_cardio(soup)



            event = {
                **this_class,
                **summary,
                **cardio
            }

            #print(event)
            file_handle.close()


