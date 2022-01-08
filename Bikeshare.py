#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #getting user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please input a city: ')
        city = city.lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('invalid city, enter another city')
            

    #get user input for month (all, january, february, march, april, may, june)
    while True:
        month = input("Enter a month from the first six months of the year for a more specific result or 'all' for the whole months: ")
        month = month.lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Invalid, enter another month: ')
            

    #get user input for day of week (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)
    while True:
        day = input("Enter a day of the week or 'all' for all the days: ")
        day = day.lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday', 'sunday']:
            break
        else:
            print('Invalid! Enter the right day of the week: ')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    #loading data into the dataframe.
    df = pd.read_csv(CITY_DATA[city])
    
    
    #converting the Start Time to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    
    #creating new columns for month and weekday from Start Time.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    
    #filtering by month when needed.
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        #creating the new dataframe.
        df = df[df['month'] == month]
        

    #filtering by day of the week when needed.
    if day != 'all':
        
        #create the new dataframe.
        df = df[df['day_of_week'] == day.title()]
        
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    print('The most common month is: ',df['month'].mode()[0],'\n')

    #display the most common day of week
    print('The most common day of week is:',df['day_of_week'].mode()[0],'\n')

    #display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common start hour is:',df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    print('The most commonly used start station is:',df['Start Station'].mode()[0],'\n')

    #display most commonly used end station
    print('The most commonly used end station is:',df['End Station'].mode()[0],'\n')

    #display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] +''+df['End Station']
    print('The most frequent combination of start station and end station trip is:',df['combination'].mode()[0],'\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    print('The total travel time is:',df['Trip Duration'].sum(),'\n')

    #display mean travel time
    print('The mean travel time is:',df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print('The counts of user types are:',user_types,'\n')
    city = 'chicago', 'new york city', 'washington'
    try:
    #Display counts of gender
        gen_cnt = df.groupby(['Gender'])['Gender'].count()
        print('The counts of gender:',gen_cnt,'\n')
    except KeyError:
        print('city does not have gender column!!!') 
    #Display earliest, most recent, and most common year of birth
    try:
        mryb = sorted(df.groupby(['Birth Year'])['Birth Year'],reverse=True)[0][0]
        eyb = sorted(df.groupby(['Birth Year'])['Birth Year'])[0][0]
        mcyb = df['Birth Year'].mode()[0]
                            
        print('The earliest year of birth is:',eyb,'\n')
        print('The most recent year of birth is:',mryb,'\n')
        print('The most common year of birth is:',mcyb,'\n')
    except KeyError:
        print('The selected city does not have birth year as a column.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def see_raw_data(df):
    # getting input from the user on individual raw data.
    start_data = 0
    end_data = 5
    df_length = len(df.index)
    
    while start_data < df_length:
        view_data = input("\nWould you like to see the raw data? Type 'yes' or 'no'.\n")
        if view_data.lower() == 'yes':
            
            print("\nDisplaying raw data.\n")
            if end_data > df_length:
                end_data = df_length
            print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        see_raw_data(df)
        
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

