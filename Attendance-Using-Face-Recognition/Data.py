import pandas as pd  # Gives functionality to make DataFrames and Excel Support
from openpyxl import load_workbook  # Used to update excel sheets to our requirements
import datetime  # Used to make datetime objects and get system time and date
import matplotlib.pyplot as plt  # Used to make bar graphs


def get_name(roll_number, division='SE CMPN A'):
    names = pd.read_excel("Class Information/"+division+".xlsx", index_col=0)
    return names.loc[roll_number, 'Name']


def mark_attendance(matched_ids, division='SE CMPN A', subject='OST', lecture_type='Theory', hour=2):
    path = "Attendance Sheets/" + division + "/" + subject + "/" + subject + " Attendance.xlsx"
    # Sets the path to the excel sheet for proper class and Subject

    date = datetime.datetime.now().strftime("%d-%m-%y")
    # Sets the date to current date

    # Total Present can be calculated by getting a count of unique ids
    total_present = len(set(matched_ids)) # To add the number of people who were marked present

    book = load_workbook(path)  # Loads the excel sheet to the book variable
    writer = pd.ExcelWriter(path)  # Creates a writer object
    writer.book = book
    attendance = pd.read_excel(path, index_col=0, sheet_name=lecture_type)
    # Reads the excel file to memory

    to_be_removed = book[lecture_type]  # Loads sheet into the variable
    book.remove(to_be_removed)  # Removes the existing sheet on which we have to update, for it to be added later

    if date not in attendance.columns:  # Lets us upload 2 or more images for the same date, same lecture
        attendance[date] = 'A'  # Makes a new column with current date initialised a 'A'

    attendance.loc[matched_ids, date] = 'P' # Marks present for all the Roll Numbers in matched ids

    attendance.loc['Total Present', date] = total_present
    attendance.loc['Hours', date] = hour
    attendance.to_excel(writer, sheet_name=lecture_type)  # Adds the updated sheet to the writer object
    writer.save()
    writer.close()
    # Saves and closes the writer object

def get_lecture_details(faculty_name='Prakash Parmar'):
    current_time = datetime.datetime.now().time()  # Makes a time object of current
    current_day = datetime.datetime.now().strftime("%A")
    # Currentday stores the name of current day. %A is the parameter to pass to strftime to get the day in string format

    '''
    Copy Paste the next line into the parameters list to pass time instead of taking the system time
    , hour=14, minute=44, day='Wednesday
    
    current_time = datetime.time(14, 44)
    current_day = day
    '''
    path = "Timetables/" + faculty_name + " Timetable.xlsx"  # Sets the path of the excel sheet timetable
    time_table = pd.read_excel(path, index_col=0)   # Reads the timetable

    for bound in time_table.index:  # Iterates over the bounds/lecture times stored in excel sheet as indices
        start = bound.split("-")[0]  # Takes the first half of the bound as start time
        start_time = datetime.time(hour=int(start.split(":")[0]), minute=int(start.split(":")[1]))
        #  Makes a start_time time object of the start time

        end = bound.split("-")[1]
        end_time = datetime.time(hour=int(end.split(":")[0]), minute=int(end.split(":")[1]))
        # Similarly makes an end_time time object of the end time

        try:
            if start_time < current_time < end_time:  # Checks if current system time is between the start and end time
                lecture = time_table.loc[bound, current_day]
                if lecture == "No Lecture":
                    return lecture, False
                else:
                    lecture = lecture.split("/")
                    date = datetime.datetime.now().strftime("%d-%m-%y")
                    lecture_details = {'subject': lecture[0], 'type': lecture[1], 'year_branch_div': lecture[2],
                                       'duration': lecture[3], 'time': lecture[4], 'date': date}
                    return lecture_details, True
        except:
            print("Non instructional day")
            return "Non Instructional Day", False
    return "No Lecture", False


def plot_bargraph(division='SE CMPN A', subject='OST', lecture_type='Theory'):
    path = "Attendance Sheets/" + division + "/" + subject + "/" + subject + " Attendance.xlsx"
    # Setting the path to the excel sheet

    attendance = pd.read_excel(path, sheet_name=lecture_type, index_col=0)
    # Reading the contents of excel file

    dates = list(attendance.columns)
    dates.remove("Name")
    # Making a list of dates

    total_present = [attendance.loc['Total Present', x] for x in dates]
    # Making a list of Total Present
    plt.figure("Line Plot")  # Sets the name of the screen in which graph is plotted
    plt.plot(dates, total_present)  # Plots a bar graph between dates and total present
    plt.xticks(rotation='vertical')  # Makes the x-axis labels vertical
    plt.title("Attendance of " + subject + " " + lecture_type)  # Sets and displays the title of the plot
    plt.xlabel("Dates")  # Sets and displays the x-axis label
    plt.ylabel("Total Present")  # Sets and displays y-axis label
    plt.subplots_adjust(bottom=0.200)  # Adjusts the position of the plot so that the x-axis title isnt cut
    plt.show()  # Finally, displays the plot


def compute_percentages(division='SE CMPN A', subject='OST', lecture_type='Theory'):
    path = "Attendance Sheets/" + division + "/" + subject + "/" + subject + " Attendance.xlsx"
    # path = r'''Attendance Sheets\SE CMPN A\CG\CG Attendance.xlsx'''
    attendance = pd.read_excel(path, index_col=0,  sheet_name=lecture_type) 
    # Reading the required excel sheet to memory

    roll_numbers = list(attendance.index)
    roll_numbers.remove("Hours")
    roll_numbers.remove("Total Present")
    # Makes a list of roll numbers present in the dataframe

    dates = list(attendance.columns)
    dates.remove("Name")
    # Makes a list of all dates present in the excel file

    attendance['Percentage'] = 0
    attendance['Total Hours Present'] = 0
    # Makes 2 new columns in the data frame to store Total Hours and percentage present of every student


    # To calculate total number of hours of lecture that have been conducted
    # attendance.drop('Name', axis=1, inplace=True)
    attendance.fillna(0, inplace=True) # To fill the empty values in hour series (Name)
    total_hours = attendance.loc['Hours'].apply(float).sum() # To find the sum of the hour series
    # attendance['Name'] = names

    # To calculate the percentage 
    for roll_number in roll_numbers:
        total_hours_present = 0  # To store number of hours the student was present for
        for date in dates:
            if attendance.loc[roll_number, date] == 'P':
                total_hours_present += int(attendance.loc['Hours', date])
        attendance.loc[roll_number, 'Total Hours Present'] = total_hours_present
        attendance.loc[roll_number, 'Percentage'] = round((total_hours_present/total_hours)*100, 2)

    attendance.loc['Hours', 'Total Hours Present'] = total_hours
    attendance.loc['Hours', 'Percentage'] = ' '
    attendance.loc['Total Present', 'Total Hours Present'] = ' '
    attendance.loc['Total Present', 'Percentage'] = ' '

    attendance.to_excel("Attendance.xlsx")
    return "Attendance.xlsx"


def faculty_login(username, password):
    faculty_details = pd.read_excel("Faculty Details.xlsx", index_col=0)
    if username not in faculty_details.index:
        return False, "Username not found"
    elif password != faculty_details.loc[username, 'Password']:
        return False, "Password is Incorrect"
    else:
        print("Username and Password match", username, faculty_details.loc[username, 'Password'])
        return True, faculty_details.loc[username, 'Name']