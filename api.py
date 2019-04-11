from flask import Flask, request, render_template, send_file
from datetime import date
from datetime import timedelta
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from docx import Document
import os


def getMonth(m):
    if m==1:
        return "January"
    elif m==2:
        return "February"
    elif m==3:
        return "March"
    elif m==4:
        return "April"
    elif m==5:
        return "May"
    elif m==6:
        return "June"
    elif m==7:
        return "July"
    elif m==8:
        return "August"
    elif m==9:
        return "September"
    elif m==10:
        return "October"
    elif m==11:
        return "November"
    elif m==12:
        return "December"
    else:
        return "Month Not Found"

def getWeekDay(d):
    if d==0:
        return "Monday"
    elif d==1:
        return "Tuesday"
    elif d==2:
        return "Wednesday"
    elif d==3:
        return "Thursday"
    elif d==4:
        return "Friday"
    elif d==5:
        return "Saturday"
    elif d==6:
        return "Sunday"
    else:
        return "Weekday Not Found"

def formatDate(old):

    new=[]
    for i in range(len(old)):
        s=str(getMonth(old[i].month))+" " + str(old[i].day)+", " +str(old[i].year)+"\n("+str(getWeekDay(old[i].weekday()))+")"
        new.append(s)
    return new


def computeCalender(start):

    #Define the time deltas for the dates
    tds=[timedelta(days=0),timedelta(days=3),timedelta(days=4),
    timedelta(days=10),timedelta(days=12),timedelta(days=15),
    timedelta(days=20),timedelta(days=25), timedelta(days=27),
    timedelta(days=30),timedelta(days=31),timedelta(days=32),
    timedelta(days=33),timedelta(days=38),timedelta(days=39),
    timedelta(days=41),timedelta(days=44),timedelta(days=46),
    timedelta(days=50),timedelta(days=51),timedelta(days=54),
    timedelta(days=56),timedelta(days=59),timedelta(days=61),
    timedelta(days=66),timedelta(days=70),timedelta(days=75),
    timedelta(days=106),timedelta(days=111),timedelta(days=113) ]

    #Define the date to be written
    data=["LD to file Trial Briefs (if ordered by the Court) Trial briefs for civil cases are optional unless ordered by the Court.  When so ordered, they shall be submitted to the Court and opposing counsel no later than the court day preceding the date set for trial, unless the Court orders submission at an earlier date. Trial briefs shall set forth the issues to be tried and any significant evidentiary problems which are likely to be presented. (L.R. 2.2.06)",
    "Master Trial Calendar Call – 1:30 P.M., Department 2. Counsel must be prepared to advise the Court of all relevant trial data at that time. (L.R. 2.2.02.(a).)  Jury deposits are to be made as provided in Code of Civil Procedure §§ 631 et seq. (L.R. 2.2.02.(b).) All proposed jury instructions, motions in limine, witness lists, exhibit lists and trial briefs (if so ordered by the Court) shall be filed no later than 12 noon the day of the Trial Calendar Call/Master Calendar. (L.R. 2.2.02(e).) ",
    "LD to file Motions in Limine – All in limine motions must be in writing. Each motion shall be limited to a single subject and the motions shall be numbered consecutively. Responses shall address only the subject of the motion and shall be numbered the same as the motions. (L.R. 2.2.02 (d).) Must be filed by Noon. (See L.R. 2.2.02(e).) ",
    "LD to file Jury Instructions – Each party must file proposed jury instructions no later than 12 noon the day of the Trial Calendar Call/Master Calendar. Such instructions must comply with California Rule of Court 2.1055. (L.R. 2.2.02 (c).) Must be filed by Noon. ",
    "LD to file Exhibit Lists Must be filed by Noon. (See L.R. 2.2.02(e).)",
    "LD to file Exhibit Lists Must be filed by Noon. (See L.R. 2.2.02(e).)",
    "LD to serve CCP section 998 offer by HAND.  (10 days before trial.)",
    "LD to notice parties to appear for trial without documents by HAND (10 days before trial)",
    "LD for Discovery Motions on Experts to be heard.  (10 days before initial trial date, CCP § 2024.030.)  Note: Before any law and motion or default matter is set, the hearing date must be cleared with the Clerk's Office by calling (831) 420-2204. (L.R. 2.4.01(a).)  Therefore, while this might be the last actual day to have this motion heard, whether such a motion may be heard on this date is dependent upon the Clerk’s Office scheduling and the Court’s availability.  ",
    "LD to serve CCP Section 998 offer by FEDEX (overnight).  (10 days before trial + 2 court days for overnight mail.)",
    "LD to serve CCP Section 998 offer by MAIL.  (10 days before trial + 5 for mailing.) ",
    "LD to notice parties to appear for trial without documents by MAIL.  (10 days before trial + 5 for mailing; CCP § 1987.) ",
    "Expert Discovery Cut-Off (15 days before trial; CCP §2024.030.) ",
    "LD for Discovery Motions (Non-Expert) to be Heard.  (15 days before initial trial date; CCP § 2024.020.)  Note: Before any law and motion or default matter is set, the hearing date must be cleared with the Clerk's Office by calling (831) 420-2204. (L.R. 2.4.01(a).)  Therefore, while this might be the last actual day to have this motion heard, whether such a motion may be heard on this date is dependent upon the Clerk’s Office scheduling and the Court’s availability.  ",
    "LD to notice parties to appear at trial with documents by HAND.  (CCP § 1987; 20 days before trial.)  ",
    "LD to notice parties to appear at trial with documents by MAIL.  (CCP §1987; 20 days before trial + 5 for mailing.)",
    "Jury Fees due.  (May not exceed $150 for each party; 25 days before initial trial date; CCP § 631.) Note: This seems to conflict with L.R. 2.2.02.(b) which allows for the deposit of Jury fees as of the date of Trial Master Calendar Call (October 18, 2018).  Therefore, if Jury Fees have yet to be deposited, then we should conservatively plan for this deadline as the dead line to deposit Jury Fees.",
    "LD to serve notice of expert deposition by HAND.  (10 days before expert discovery cut-off; CCP § 2025.270.)",
    "LD to serve notice of expert deposition by EXPRESS MAIL (10 days before expert discovery cut-off + 2 court days for overnight mail; CCP § 2025.270.)",
    "Consider submitting written stipulation providing for admission of exhibits at trial, or stipulation as to all matters as appropriate, reserving objections as to relevance and Evid. Code 352 considerations.  (There is no rule relating to this practice.  This is simply an internal tickler to remind our office to begin considering these issues.)",
    "Begin to Consider Personally Serving Non-Parties with Subpoenas to Appear at Trial Code of Civil Procedure § 1987(a) provides that a subpoena to appear at a civil trial shall be served on a non-party “so as to allow the witness a reasonable time for preparation and travel to the place of attendance.”  Given that a “reasonable time” is not a bright-line standard, this deadline is included as an internal tickler.",
    "LD to have MSJ heard.  (30 days before date of trial.) Note: Before any law and motion or default matter is set, the hearing date must be cleared with the Clerk's Office by calling (831) 420-2204. (L.R. 2.4.01(a).)  Therefore, while this might be the last actual day to have this motion heard, whether such a motion may be heard on this date is dependent upon the Clerk’s Office scheduling and the Court’s availability.",
    "Discovery Cut-Off. (30 days before trial; CCP § 2024.020.)",
    "Deadline to hear have Motion to Bifurcate heard (Either no later than thirty days before trial or the day of the pretrial conference [there is no pretrial conference in this matter at this time; CCP § 598) ",
    "LD to submit supplemental expert witness list/report containing the name and address of any experts who will express an opinion on a subject to be covered by an expert designated by an adverse party to the exchange, if the party supplementing an expert witness list has not previously retained an expert to testify on that subject.  (CCP § 2034.280; within 20 days after exchange of expert witness information.)",
    "LD to file/serve notice of expert discovery motion by MAIL.  (16 court days + 5 days for mailing before last day for expert discovery to be heard; CCP § 1005.)  ",
    "LD to file/serve notice of expert discovery motion by MAIL.  (16 court days + 5 days for mailing before last day for expert discovery to be heard; CCP § 1005.)  ",
    "LD to file/serve notice of discovery motion by HAND (re non-expert discovery).  (16 court days before LD for non-expert discovery motions to be heard; CCP § 1005.)",
    "LD to notice deposition of nonparty without documents (or party with or without documents) by HAND.  (10 days before discovery cut-off; CCP § 2025.270.)",
    "LD to file/serve notice of discovery motion by MAIL (re non-expert discovery).  (16 court days before LD for non-expert discovery motions to be heard + 5 for mailing; CCP § 1005.) ",
    "LD to serve notice of non-expert deposition by MAIL.  (10 days before discovery cut-off + 5 for mailing; CCP § 2025.270.)",
    "LD to notice deposition of nonparty without documents (or party with or without documents) by MAIL.  (10 days before discovery cut-off + 5 for mailing; CCP § 2025.270.)",
    "LD to notice deposition of nonparty (with subpoena) with consumer documents by HAND.  (20 days before discovery cut-off; CCP § 2025.270.) ",
    "LD to exchange expert information.  (50 days before trial/20 days after service of the demand; CCP § 2034.230.) ",
    "LD to notice deposition of nonparty (with subpoena) with consumer documents by MAIL.  (25 days before discovery cut-off; CCP § 2025.270.)  ",
    "LD to notice deposition of nonparty (with subpoena) with consumer documents by MAIL.  (25 days before discovery cut-off; CCP § 2025.270.)",
    "LD to file and serve Motion to Bifurcate by MAIL.  (16 court days before last day to have Motion heard + 5 for mailing.) ",
    "LD to serve written discovery by HAND.  (30 days before discovery cut-off date; CCP §§ 2024.010, 2024.020.)",
    "LD to serve written discovery by MAIL (35 days before discovery cut-off date; CCP §§ 2024.010, 2024.020.)",
    "LD to demand exchange of expert witness information by HAND.  (70 days before trial date; CCP § 2034.220.)",
    "LD to demand exchange of expert witness information by MAIL.  (70 days before trial date + 5 days for mailing; CCP § 2034.220.)  ",
    "LD to serve notice of summary judgment by HAND.  (75 days before hearing date, i.e., last date to have MSJ heard; CCP § 437c(a).) ",
    "LD to serve notice of summary judgment by FEDEX (overnight) or FAX (w/ prior agreement).  (75 days before hearing date, i.e., last date to have MSJ heard + 2 court days for express/fax service; CCP § 437c(a).) ",
    "LD to serve notice of summary judgment by MAIL.  (75 days before hearing date, i.e., last date to have MSJ heard + 5 days for mailing; CCP § 437c(a).) "]

    #Get holidays from the lacourt
    #Get the raw HTML
    sock=urllib.request.urlopen('http://www.lacourt.org/holiday/ui/index.aspx')
    htmlsource=sock.read()
    sock.close()
    #Parse the HTML to get all holidays
    soup = BeautifulSoup(htmlsource, "html.parser")
    table=soup.find_all('table',attrs={'class':'commontable'})
    table=soup.find_all('td',attrs={'width':'35%'})
    #Convert all holidays dates to strings
    temp=[]
    for t in table:
        temp.append(t.string)
    table=temp
    #Create holiday datetime dictionary
    holidays={}
    month=["January","February","March","April","May","June","July","August","September","October","November","December"]
    l=''
    s=''
    for i in range(len(table)):
        if i%3==0:
            #weekday
            pass
        elif i%3==1:
            #date
            l=table[i].replace(",","")
            l=l.split(" ")
            l=date(int(l[2]),month.index(l[0])+1,int(l[1]))
        else:
            #text
            s=table[i]
        if i%3==0 and i!=0:
            holidays.update({l:s})
    
    #Begin scheduling dates
    dates={}

    #schedule everything based on timedelta vector
    i=0
    for td in tds:
        #calculate date based on start date
        curr=start-td
        #account for holidays and weekends
        while curr in holidays:
            data[i]+="(This deadline actually falls on a Holiday, "+str(getMonth(curr.month))+" "+str(curr.day)+", "+str(curr.year)+".)"
            curr-=timedelta(days=1)
        if (curr).weekday()==5:
            data[i]+="(This deadline actually falls on Saturday, "+str(getMonth(curr.month))+" "+str(curr.day)+", "+str(curr.year)+".)"
            curr-=timedelta(days=1)
        elif (curr).weekday()==6:
            data[i]+="(This deadline actually falls on Sunday, "+str(getMonth(curr.month))+" "+str(curr.day)+", "+str(curr.year)+".)"
            curr-=timedelta(days=2)
        dates.update({curr:data[i]})
        i+=1


    #combine dates and holidays
    dates.update(holidays)
    #convert dictionary to dataframe
    df=pd.DataFrame({"Dates":list(dates.keys()),'Info':list(dates.values())})
    df['Formated Dates']=formatDate(df['Dates'])
    #sort them
    df = df.sort_values('Dates')
    #convert columns to lists
    dates=df['Formated Dates'].tolist()
    info=df['Info'].tolist()

    #open template document
    document=Document('PythonDocxTemplate.docx')
    #define table and table style
    table=document.add_table(rows=len(df),cols=2)
    table.style = 'S1'
    #populate table
    for i in range(len(df)):
        cell=table.cell(i,0)
        cell.text=str(dates[i])
        cell=table.cell(i,1)
        cell.text=str(info[i])
    #save document
    document.save('Output.docx')


app = Flask(__name__)
# EX
# /Calender?date=03/12/2000
@app.route('/Calender')
def Calender():
    #Check if the incoming request is a POST request
    if request.method == 'POST':
        return "Invalid Request"
    #Attempt to get the date argument
    date_string = request.args.get('date')
    # If there was no date argument
    if date_string == None:
        return "No Date Argument"
    # Make sure the date arg isn't empty
    if date_string == '':
        return "Date Argument Empty"
    # Make sure a date was given
    date_string = date_string.split('/')
    if len(date_string) != 3:
        return "Invalid Date Format"
    # Make sure all items are numbers
    for token in date_string:
        if not token.isdigit():
            return "Invalid Date"
    #Convert all the strings to ints
    date_string = [int(x) for x in date_string]
    try:
        #Create the start date and catch any value error
        start_date = date(date_string[2], date_string[0], date_string[1])
    except ValueError:
        return "Invalid Date"
    #Create the return doc
    computeCalender(start_date)
    path = os.path.join(os.getcwd(), 'Output.docx')
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='4000')