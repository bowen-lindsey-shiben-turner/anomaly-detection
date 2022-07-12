import acquire
import prepare
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os



#--------------------------Question_3_fuctions---------------------------------------------------------------

def explore_question3(df):
    '''
    This function creates a dataframe tailored to explore the following:
    
    Question 3:
    Are there students who, when active, hardly access the curriculum? 
    If so, what information do you have about these students?

    The function renames columns & drops records that are not associated with 
    active students.
    '''
    df3 = df.copy()
    df3 = df3.rename(columns={'program_id': 'program', 'name': 'cohort'})
    #rename columns just for preference
    df3 = df3.dropna()
    #drops nulls, records without sufficient data about student access
    df3['program_access'] = (df3.date_time >= df3.start_date) & (df3.date_time <= df3.end_date)
    # creates boolean column to weed out everything, but active students
    df3 = df3[(df3['program_access'] == True)]
    df3 = df3[(df3['cohort'] != 'staff')] 
    #creates df of active students that are not staff
    df3[['date_time', 'start_date', 'end_date', 'created_at', 'updated_at']] = df3[['date_time','start_date', 'end_date', 'created_at', 'updated_at']].apply(pd.to_datetime)
    #converts selected columns to datetime format
    df3 = df3.drop(columns=['cohort_id'])
    #drops unnecessary column
    df3['user_id'] = df3['user_id'].astype(object)
    df3['cohort_program'] = df3['program'] + '_' + df3['cohort']
    #dropping all cohorts that do no have a start date and end date within date_time
    df3.drop(df3[df3.cohort.isin(['easley', 'teddy', 'kalypso', 'florence', 'neptune',  'sequoia', 'oberon', 'luna', 'marco'])].index, inplace=True)
    df3['start_date'] = df3['start_date'].astype(str)
    df3['end_date'] = df3['end_date'].astype(str)
    df3['cohort_dates'] = df3['cohort_program'] + ': ' + df3['start_date'] + ' to ' + df3['end_date']
    df3['date_time_copy'] = df3['date_time']
    df3 = df3.set_index('date_time_copy').sort_index()
    df3['weekday_name'] = df3.index.day_name()
    df3['hour'] = df3.index.time
    df3['hour'] = df3['hour'].astype(str)
    df3['hour'] = df3['hour'].str[:-6]

    return df3

def q3_create_percentile_dfs(df3):
    '''
    This function creates 9 dataframes specific for question 3 exploration and prints 
    the number of dataframe records.
    
    4 dataframes for the following:
    Break the data down into quantiles (bottom 5% of access, bottom 25% of access, 
    middle 25-75% of access, and top 25% of access) for comparisons.

    5 dataframes do the following:
    With the 4 sub-populations and original df3, groupby user_id's last access date and 
    calculate the difference of the program end date to the user's last access date. 
    This will tell us when the sub-population's stopped accessing the curriculum during their program.
    '''

    df3['start_date'] = df3['start_date'].apply(pd.to_datetime)
    df3['end_date'] = df3['end_date'].apply(pd.to_datetime)
    counts = df3.user_id.value_counts()
    bottom_5 = df3[df3['user_id'].isin(counts[counts < 113].index)]
    bottom_25 = df3[df3['user_id'].isin(counts[counts < 625].index)]
    middle = df3[df3['user_id'].isin(counts[counts < 1328].index)]
    middle = df3[df3['user_id'].isin(counts[counts >= 625].index)]
    top_25 = df3[df3['user_id'].isin(counts[counts >= 1379].index)]

    bottom_5_users = bottom_5.groupby(bottom_5.user_id).max()
    bottom_5_users['last_day'] = bottom_5_users['end_date'] - bottom_5_users['date_time']
    bottom_5_users['last_day'] = bottom_5_users['last_day'].astype(str)
    bottom_5_users['last_day'] = bottom_5_users['last_day'].str[:-14]
    bottom_5_users['last_day'] = bottom_5_users['last_day'].astype(int)

    bottom_25_users = bottom_25.groupby(bottom_25.user_id).max()
    bottom_25_users['last_day'] = bottom_25_users['end_date'] - bottom_25_users['date_time']
    bottom_25_users['last_day'] = bottom_25_users['last_day'].astype(str)
    bottom_25_users['last_day'] = bottom_25_users['last_day'].str[:-14]
    bottom_25_users['last_day'] = bottom_25_users['last_day'].astype(int)

    top_25_users = top_25.groupby(top_25.user_id).max()
    top_25_users['last_day'] = top_25_users['end_date'] - top_25_users['date_time']
    top_25_users['last_day'] = top_25_users['last_day'].astype(str)
    top_25_users['last_day'] = top_25_users['last_day'].str[:-14]
    top_25_users['last_day'] = top_25_users['last_day'].astype(int)

    middle_users = middle.groupby(middle.user_id).max()
    middle_users['last_day'] = middle_users['end_date'] - middle_users['date_time']
    middle_users['last_day'] = middle_users['last_day'].astype(str)
    middle_users['last_day'] = middle_users['last_day'].str[:-14]
    middle_users['last_day'] = middle_users['last_day'].astype(int)

    all_users = df3.groupby(df3.user_id).max()
    all_users['last_day'] = all_users['end_date'] - all_users['date_time']
    all_users['last_day'] = all_users['last_day'].astype(str)
    all_users['last_day'] = all_users['last_day'].str[:-14]
    all_users['last_day'] = all_users['last_day'].astype(int)

    print('')
    print('All Access Records: {:,} records (between 1-4763 program access occurrences) '.format(len(df3)))
    print('Bottom 5% Access Records: {:,} records (less than 113 program access occurrences)'.format(len(bottom_5)))
    print('Bottom 25% Access Records: {:,} records (less than 625 program access occurrences)'.format(len(bottom_25)))
    print('Middle 25-75% Access Records: {:,} records (between 625-1380 program access occurrences)'.format(len(middle)))
    print('Top 25% Access Records: {:,} records (between 1380-4763 program access occurrences)'.format(len(top_25)))
    print('')
    print('------------------------------------------------')
    print('')
    print('All Access Records: {:,} records'.format(len(all_users)))
    print('Bottom 5% Users: {:,} records'.format(len(bottom_5_users)))
    print('Bottom 25% Users: {:,} records'.format(len(bottom_25_users)))
    print('Middle 25-75% Users: {:,} records'.format(len(middle_users)))
    print('Top 25% Users: {:,} records'.format(len(top_25_users)))
    print('')
    print('------------------------------------------------')

    return bottom_5, bottom_25, middle, top_25, all_users, middle_users, top_25_users, bottom_25_users, bottom_5_users

def q3_plot_counts(bottom_5, bottom_25, middle, top_25):

    '''This function visualizes the average access counts of the four sub-populations'''

    top_25['hour'] = top_25['hour'] + ':00'
    middle['hour'] = middle['hour'] + ':00'
    bottom_25['hour'] =bottom_25['hour'] + ':00'
    bottom_5['hour'] =bottom_5['hour'] + ':00'
    plt.figure(figsize=(10,6))
    ax = (top_25['weekday_name'].value_counts() / top_25.user_id.nunique()).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).plot(label= "top_25%")
    (middle['weekday_name'].value_counts() / middle.user_id.nunique()).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).plot(ax=ax, label="middle_25-75%")
    (bottom_25['weekday_name'].value_counts() / bottom_25.user_id.nunique()).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).plot(ax=ax, label="bottom_ 25%")
    (bottom_5['weekday_name'].value_counts() / bottom_5.user_id.nunique()).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).plot(ax=ax, label="bottom_5%")
    plt.xlabel("Weekday", fontsize=14)
    plt.ylabel('Avg. User Access Counts (Program Duration)', fontsize=14)
    plt.title('Avg. Weekday Access Counts of Sub-Populations', fontsize=20)
    plt.axvline(x = 0, ymin = 0.1, ymax = 0.90, color = 'grey', linestyle='dotted', linewidth=3.5,
                label = 'Program/Weekday Start')
    plt.axvline(x = 4.2, ymin = 0.1, ymax = 0.90, color = 'black', linestyle='dotted', linewidth=3.5,
                label = 'Program/Weekday End')
    plt.legend()
    plt.show()

    plt.figure(figsize=(10,6))
    ax = (top_25['hour'].value_counts() / top_25.user_id.nunique()).reindex(['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '01:00', '02:00', '03:00', '04:00', '05:00']).plot(label= "top_25%")
    (middle['hour'].value_counts() / middle.user_id.nunique()).reindex(['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '01:00', '02:00', '03:00', '04:00', '05:00']).plot(ax=ax, label="middle_25-75%")
    (bottom_25['hour'].value_counts() / bottom_25.user_id.nunique()).reindex(['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '01:00', '02:00', '03:00', '04:00', '05:00']).plot(ax=ax, label="bottom_ 25%")
    (bottom_5['hour'].value_counts() / bottom_5.user_id.nunique()).reindex(['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '01:00', '02:00', '03:00', '04:00', '05:00']).plot(ax=ax, label="bottom_5%")
    plt.xlabel("Hour (24-hour)", fontsize=14)
    plt.ylabel('Average User Access Counts (Program Duration)', fontsize=14)
    plt.title('Average Hourly Access Counts of Sub-Populations', fontsize=20)
    plt.axvline(x = 2.8, ymin = 0.1, ymax = 0.90, color = 'grey', linestyle='dotted', linewidth=3.5,
                label = 'Daily Program Start')
    plt.axvline(x = 11.2, ymin = 0.1, ymax = 0.90, color = 'black', linestyle='dotted', linewidth=3.5,
                label = 'Daily Program End')
    plt.legend()
    plt.show()

def q3_plot_trends(top_25, middle, bottom_25, bottom_5):
    '''This function visualizes the average access trends of the four sub-populations'''

    plt.figure(figsize=(10,6))
    order=(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    ax = (top_25.weekday_name.value_counts(normalize=True, sort=False)*100).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).plot(label= "top_25%")
    (middle.weekday_name.value_counts(normalize=True, sort=False)*100).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).plot(ax=ax,label= 'middle_25-75%')
    (bottom_25.weekday_name.value_counts(normalize=True, sort=False)*100).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).plot(ax=ax, label= "bottom_25%")
    (bottom_5.weekday_name.value_counts(normalize=True, sort=False)*100).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).plot(ax=ax,label= 'bottom_5')
    plt.xlabel("Weekday", fontsize=14)
    plt.ylabel('Percentage of sub-population', fontsize=14)
    plt.title('Compare/Contrast Weekday Access Trends of Sub-Populations', fontsize=20)
    plt.axvline(x = 0, ymin = 0.1, ymax = 0.90, color = 'grey', linestyle='dotted', linewidth=3.5,
                label = 'Program/Weekday Start')
    plt.axvline(x = 4.2, ymin = 0.1, ymax = 0.90, color = 'black', linestyle='dotted', linewidth=3.5,
                label = 'Program/Weekday End')
    plt.legend()
    plt.show()

    plt.figure(figsize=(10,6))
    ax = (top_25['hour'].value_counts(normalize=True, sort=False)*100).reindex(['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '01:00', '02:00', '03:00', '04:00', '05:00']).plot(label= "top_25%")
    (middle['hour'].value_counts(normalize=True, sort=False)*100).reindex(['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '01:00', '02:00', '03:00', '04:00', '05:00']).plot(ax=ax, label="middle_25-75%")
    (bottom_25['hour'].value_counts(normalize=True, sort=False)*100).reindex(['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '01:00', '02:00', '03:00', '04:00', '05:00']).plot(ax=ax, label="bottom_ 25%")
    (bottom_5['hour'].value_counts(normalize=True, sort=False)*100).reindex(['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '01:00', '02:00', '03:00', '04:00', '05:00']).plot(ax=ax, label="bottom_5%")
    plt.xlabel("Hour (24-hour)", fontsize=14)
    plt.ylabel('Percentage of sub-population', fontsize=14)
    plt.title('Compare/Contrast Hourly Access Trends of Sub-Populations', fontsize=20)
    plt.axvline(x = 2.8, ymin = 0.1, ymax = 0.90, color = 'grey', linestyle='dotted', linewidth=3.5,
                label = 'Daily Program Start')
    plt.axvline(x = 11.2, ymin = 0.1, ymax = 0.90, color = 'black', linestyle='dotted', linewidth=3.5,
                label = 'Daily Program End')

    plt.legend()
    plt.show()

    
def q3_plot_hists(all_users, bottom_5_users, bottom_25_users, middle_users, top_25_users):

    '''This function visualizes the last day of curriculum access of users in sub-populations'''
    
    plt.figure(figsize=(7,6))

    sns.histplot(data= all_users, x='last_day', bins=[0,30,60,90,120,150, 180], color='red')
    plt.title('All Users', fontsize=20, y=1.03)
    plt.suptitle('Users by Access Amount & Last Access Day during Program', fontsize=25, fontweight='bold', y=1.08)
    plt.xlabel("# of Days- Last Access and Program End", fontsize=14)
    plt.ylabel('User Count', fontsize=14)


    fig, axes = plt.subplots(2, 2, figsize=(12,9))

    ax1 = sns.histplot(data= bottom_5_users, x='last_day', bins=[0,30,60,90,120,150, 180], color='blue', ax=axes[0,0])
    ax1.set_title('Bottom 5% of Users', fontsize=20)
    ax1.set_xlabel("# of Days- Last Access and Program End", fontsize=14)
    ax1.set_ylabel('User Count', fontsize=14)

    ax2 = sns.histplot(data= bottom_25_users, x='last_day', bins=[0,30,60,90,120,150, 180], color='green', ax=axes[0,1])
    ax2.set_title('Bottom 25% of Users', fontsize=20)
    ax2.set_xlabel("# of Days- Last Access and Program End", fontsize=14)
    ax2.set_ylabel('User Count', fontsize=14)

    ax3 = sns.histplot(data= middle_users, x='last_day', bins=[0,30,60,90,120,150, 180], color='orange', ax=axes[1,0])
    ax3.set_title('Middle 25-75% of Users', fontsize=20)
    ax3.set_xlabel("# of Days- Last Access and Program End", fontsize=14)
    ax3.set_ylabel('User Count', fontsize=14)

    ax4= sns.histplot(data= top_25_users, x='last_day', bins=[0,30,60,90,120,150, 180], color='purple', ax=axes[1,1])
    ax4.set_title('Top 25% of Users', fontsize=20)
    ax4.set_xlabel("# of Days- Last Access and Program End", fontsize=14)
    ax4.set_ylabel('User Count', fontsize=14)

    plt.subplots_adjust(left=0.1,
                        bottom=0.07, 
                        right=0.9, 
                        top= .9, 
                        wspace=0.2, 
                        hspace=0.4)


    plt.show()

#-------------------------------------------------------------------------------------------------------------