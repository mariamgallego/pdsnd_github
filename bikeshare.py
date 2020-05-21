import pandas as pd
import numpy as np
import time

CITY_DATA = {'chicago':'chicago.csv',
             'washington':'washington.csv',
             'new_york':'new_york_city.csv'}
""" Defining dictionary key as city names and values as respective csv file's to
access them according to the user input """

## PART I: Defining the metrics for the project (city, month, day) and loading data


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Welcome!! Let's explore some US bikeshare data ")
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    print("Which city would you like to filter the data by? You can choose beteen New York, Chicago or Washington.\n")

    city = input() ###This option gets the input from the user
    city_name = city.lower().replace(' ','_') ### Previously, the input was case sensitive, but after this it is not
    while city_name not in CITY_DATA:
        print("Sorry, I didn't understand that. Make sure you are spelling it correctly. Which city's data would you like to filter by?")

    print("\nYou can filter the data by month, day, both or none\n \nPlease indicate: month, day, both or none\n")
    
    time_filter = ['month','day','both','none']
    
    time_selection = input()
    
    selection = time_selection.lower() ### Here we are also making sure this input is not case sensitive
    while selection not in time_filter:
        print("Sorry, I didn't understand that. Would you like to add a time filter?")
    
    
    # TO DO: get user input for month (all, january, february, ... , june)
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if selection == 'month':
        print("\nWhich month would you like to filter the data by? The options are: January, February, March, April, May or June.\n") 
        
        month = input()
        month = month.lower()
        week_days = 'all' 
        
        
    elif selection == 'day':
        print("\nWhich day would you like to filter the data by? The options are: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday.\n")
        week_days = input()
        month = 'all'  
        
        
    elif selection == 'both':
        print("\nWhich month would you like to filter the data by? The options are: January, February, March, April, May or June.\n")
        month = input()
        month = month.lower()
        print("\nWhich day would you like to filter the data by? The options are: Monday, Tuesday, Wednesday, Thursady, Friday, Saturday or Sunday.\n")
        week_days = input()
        
        
    else:
        month = 'all'
        week_days = 'all' ### This will run when the user decides not to apply a time filter and specifies the selection 'none' 
        
    print('-'*40)
    return city_name,month,week_days

def load_data(city,month,day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['week_days'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        months = ['january','february','march','april','may','june']
        
    # Use the index of the months list to get the corresponding int
        month = months.index(month)+1 # to get the proper index of the month as the equivalent to the ordinal month. In which January= 1, February= 2 etc. We need to sum 1 to the index as currently January= 0 and February= 1
        
     # filter by month to create the new dataframe
        df = df[df['month'] == month]
        
        
    # filter by day of week if applicable
    if day != 'all':
        
    # filter by day of week to create the new dataframe
        df = df[df['week_days'] == day.title()]

    print('-'*40)
    return df

## PART II: Defining Statistics

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    common_month = df['month'].mode()[0]
    print('The Most Common Month of the year is:', common_month)


    # TO DO: display the most common day of week

    common_day = df['week_days'].mode()[0]
    print('The Most Common Day of the Week is:', common_day)

    # TO DO: display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The Most Common Hour of the Day is:', common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    start_station = df['Start Station'].value_counts().idxmax()
    print('The Station that is Most Commonly used as a Start point is:', start_station)


    # TO DO: display most commonly used end station

    end_station = df['End Station'].value_counts().idxmax()
    print('\nThe Station that is Most Commonly used as an End point is:', end_station)


    # TO DO: display most frequent combination of start station and end station trip

    combined_stations = df.groupby(['Start Station', 'End Station']).count()
    print('\nThe Most common Combination of Stations for a trip are: As the Start Station', start_station, " & ", "As the End Station", end_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    total_travel_time = sum(df['Trip Duration'])
    #I want to show the time in days and months to make it more understandable. In order to get the total travel time in these formats, we need to divide the total_travel_time value by 86400, to get the figure in days (since those are the number of seconds in a day) and by 2628002.88, to get the figure in months (since those are the number of seconds in a month) 
    print('The Total travel time is:', total_travel_time/86400, " Days", "or", total_travel_time/2628002.88, " Months")


    # TO DO: display mean travel time

    avg_travel_time = df['Trip Duration'].mean()
    #Same as above, I want to get the average time not in seconds, in this case I want to represent it in minutes. Therefore in order to get the avg time in minutes we need to divide the avg_travel_time value by 60. 
    print('The Average Time Spent per Trip is:',  avg_travel_time/60, " Minutes")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    user_types = df['User Type'].value_counts()
    #print(user_types)
    print('These are the Different User Types:\n', user_types)

    # TO DO: Display counts of gender
    #In this case, considering the fact that the dataset from Washington does not have the variables for Gender and Birth Year we need to make sure that the code doesn't break when they ask for it. To avoid this from happening, we need to create a message that will let them know that this piece of data is not available 

    try:
      gender_types = df['Gender'].value_counts()
      print('\nThe Number of Users by Gender are:\n', gender_types)
    except KeyError:
      print("\nSorry, the Number of Users by Gender are not available for this filtering.")

    # TO DO: Display earliest, most recent, and most common year of birth

    try:
      earliest_birth_year = df['Birth Year'].min()
      print('\nThe Earliest Birth Year of our Users is:', earliest_birth_year)
    except KeyError:
      print("\nSorry, the Earliest Birth Year of our Users is not available for this filtering.")

    try:
      most_recent_birth_year = df['Birth Year'].max()
      print('\nMost Recent Year:', most_recent_birth_year)
    except KeyError:
      print("\nSorry, the Most Recent Birth Year of our Users is not available for this filtering.")

    try:
      most_common_birth_year = df['Birth Year'].value_counts().idxmax()
      print('\nMost Common Year:', most_common_birth_year)
    except KeyError:
      print("\nSorry, the Most Recent Birth Year of our Users is not available for this filtering.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

## PART III: Defining User Interaction

def main():
    while True:
        city,month,day = get_filters()
        df = load_data(city,month,day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        print("Would you like see five rows of data ?? Enter yes or no ")
        display_data = input()
        display_data = display_data.lower()

        i = 5
        while display_data == 'yes':
            """ To display few rows of data for user view """
            print(df[:i])
            print("Would you like to see five more rows of data ?? Enter yes or no ")
            i *= 2
            display_data = input()
            display_data = display_data.lower()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



def main():
    while True:
        city,month,day = get_filters()
        df = load_data(city,month,day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

## PART IV: Optional Data Shown
###Next we are going to give the option to the user of seeing 5 rows of raw data. They can keep on seeing new rows until they select no. In which they would have the option to restart the whole filtering process again.
        
        print("\nYou have the option to see five rows of unfiltered data. Would you like to see them? Please, select yes or no\n ")
        display_data = input()
        display_data = display_data.lower()

        i = 5 #Number of rows to be displayed, it can be changed to as many as desired.
        while display_data == 'yes':
            print(df[:i])
            print("You can see five MORE rows of unfiltered data. Would you like to see them? Please, select yes or no")
            i *= 2
            display_data = input()
            display_data = display_data.lower()

        restart = input('\nNow, you can restart the whole data filtering process. Would you like fo this? Please, select yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
