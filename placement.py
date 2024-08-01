import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

def load_data(file):
    return pd.read_excel(file)

def merge_data(beneficiaries_df, districts_df):
    return pd.merge(beneficiaries_df, districts_df, how='left', left_on='district_id', right_on='dist_id')

def calculate_age(df):
    df['dob'] = pd.to_datetime(df['dob'], errors='coerce')
    df['age'] = (pd.to_datetime('today') - df['dob']).dt.days // 365
    return df

def define_age_groups(df):
    def get_age_group(age):
        if age < 18:
            return 'Under 18'
        elif 18 <= age <= 24:
            return '18-24'
        elif 25 <= age <= 30:
            return '25-30'
        elif 30 <= age <= 35:
            return '30-35'
        else:
            return '35+'

    df['age_group'] = df['age'].apply(get_age_group)
    return df

# Streamlit app
st.title('Beneficiaries Data Analysis')

# Use threads to load data and perform calculations
with ThreadPoolExecutor() as executor:
    future_beneficiaries = executor.submit(load_data, 'beneficiries.xlsx')
    future_districts = executor.submit(load_data, 'districts.xlsx')
    
    beneficiaries_df = future_beneficiaries.result()
    districts_df = future_districts.result()

    # Replace 'M' with 'Male' in the gender column
    beneficiaries_df['gender'] = beneficiaries_df['gender'].replace('M', 'Male')

    future_merged = executor.submit(merge_data, beneficiaries_df, districts_df)
    merged_df = future_merged.result()

    future_age = executor.submit(calculate_age, merged_df)
    merged_df = future_age.result()

    future_age_groups = executor.submit(define_age_groups, merged_df)
    merged_df = future_age_groups.result()

# Display counts based on various columns
st.subheader('Counts by Gender')
st.write(merged_df['gender'].value_counts())

st.subheader('Counts by Caste')
st.write(merged_df['cast'].value_counts())

st.subheader('Counts by District')
st.write(merged_df['dist_name'].value_counts())

st.subheader('Counts by Religion')
st.write(merged_df['religion'].value_counts())

st.subheader('Counts by Qualification')
st.write(merged_df['qualification'].value_counts())

st.subheader('Counts by Age Group')
st.write(merged_df['age_group'].value_counts())

# Plotting the stacked bar chart for District and Qualification
st.subheader('Number of Students by District and Qualification')
district_qualification_counts = merged_df.groupby(['dist_name', 'qualification']).size().unstack().fillna(0)

# Sort by the total number of registrations per district in descending order
total_counts = district_qualification_counts.sum(axis=1).sort_values(ascending=False)
district_qualification_counts = district_qualification_counts.loc[total_counts.index]

fig, ax = plt.subplots(figsize=(10, 6))
district_qualification_counts.plot(kind='bar', stacked=True, ax=ax)
ax.set_title('Number of Students by District and Qualification (Descending)')
ax.set_xlabel('District')
ax.set_ylabel('Number of Students')
ax.legend(title='Qualification')

st.pyplot(fig)

# Display the count table
st.subheader('Count Table of Students by District and Qualification')
st.table(district_qualification_counts)

# Plotting the bar chart for District and Religion
st.subheader('Number of Students by District and Religion')
district_religion_counts = merged_df.groupby(['dist_name', 'religion']).size().unstack().fillna(0)

# Sort by the total number of registrations per district in descending order
total_counts_religion = district_religion_counts.sum(axis=1).sort_values(ascending=False)
district_religion_counts = district_religion_counts.loc[total_counts_religion.index]

fig_religion, ax_religion = plt.subplots(figsize=(12, 8))
district_religion_counts.plot(kind='bar', stacked=True, ax=ax_religion)
ax_religion.set_title('Number of Students by District and Religion (Descending)')
ax_religion.set_xlabel('District')
ax_religion.set_ylabel('Number of Students')
ax_religion.legend(title='Religion')

st.pyplot(fig_religion)

# Display the count table
st.subheader('Count Table of Students by District and Religion')
st.table(district_religion_counts)

# Plotting the bar chart for District and Gender
st.subheader('Number of Students by District and Gender')
district_gender_counts = merged_df.groupby(['dist_name', 'gender']).size().unstack().fillna(0)

# Sort by the total number of registrations per district in descending order
total_counts_gender = district_gender_counts.sum(axis=1).sort_values(ascending=False)
district_gender_counts = district_gender_counts.loc[total_counts_gender.index]

fig_gender, ax_gender = plt.subplots(figsize=(12, 8))
district_gender_counts.plot(kind='bar', stacked=True, ax=ax_gender)
ax_gender.set_title('Number of Students by District and Gender (Descending)')
ax_gender.set_xlabel('District')
ax_gender.set_ylabel('Number of Students')
ax_gender.legend(title='Gender')

st.pyplot(fig_gender)

# Display the count table
st.subheader('Count Table of Students by District and Gender')
st.table(district_gender_counts)

# Plotting the bar chart for District and Caste
st.subheader('Number of Students by District and Caste')

# Group by District and Caste, then count
district_caste_counts = merged_df.groupby(['dist_name', 'cast']).size().unstack().fillna(0)

# Sort by the total number of registrations per district in descending order
total_counts_caste = district_caste_counts.sum(axis=1).sort_values(ascending=False)
district_caste_counts = district_caste_counts.loc[total_counts_caste.index]

fig_caste, ax_caste = plt.subplots(figsize=(12, 8))
district_caste_counts.plot(kind='bar', stacked=True, ax=ax_caste)
ax_caste.set_title('Number of Students by District and Caste (Descending)')
ax_caste.set_xlabel('District')
ax_caste.set_ylabel('Number of Students')
ax_caste.legend(title='Caste')

st.pyplot(fig_caste)

# Display the count table
st.subheader('Count Table of Students by District and Caste')
st.table(district_caste_counts)

# Plotting the bar chart for Religion and Gender
st.subheader('Number of Students by Religion and Gender')

# Group by Religion and Gender, then count
religion_gender_counts = merged_df.groupby(['religion', 'gender']).size().unstack().fillna(0)

# Sort by the total number of registrations per religion in descending order
total_counts_religion_gender = religion_gender_counts.sum(axis=1).sort_values(ascending=False)
religion_gender_counts = religion_gender_counts.loc[total_counts_religion_gender.index]

fig_religion_gender, ax_religion_gender = plt.subplots(figsize=(12, 8))
religion_gender_counts.plot(kind='bar', stacked=True, ax=ax_religion_gender)
ax_religion_gender.set_title('Number of Students by Religion and Gender (Descending)')
ax_religion_gender.set_xlabel('Religion')
ax_religion_gender.set_ylabel('Number of Students')
ax_religion_gender.legend(title='Gender')

st.pyplot(fig_religion_gender)

# Display the count table
st.subheader('Count Table of Students by Religion and Gender')
st.table(religion_gender_counts)

# Plotting the bar chart for Religion and Qualification
st.subheader('Number of Students by Religion and Qualification')

# Group by Religion and Qualification, then count
religion_qualification_counts = merged_df.groupby(['qualification', 'religion']).size().unstack().fillna(0)

# Sort by the total number of registrations per religion in descending order
total_counts_religion_qualification = religion_qualification_counts.sum(axis=1).sort_values(ascending=False)
religion_qualification_counts = religion_qualification_counts.loc[total_counts_religion_qualification.index]

fig_religion_qualification, ax_religion_qualification = plt.subplots(figsize=(12, 8))
religion_qualification_counts.plot(kind='bar', stacked=True, ax=ax_religion_qualification)
ax_religion_qualification.set_title('Number of Students by Religion and Qualification (Descending)')
ax_religion_qualification.set_xlabel('Qualificaton')
ax_religion_qualification.set_ylabel('Number of Students')
ax_religion_qualification.legend(title='religion')

st.pyplot(fig_religion_qualification)

# Display the count table
st.subheader('Count Table of Students by Religion and Qualification')
st.table(religion_qualification_counts)

# Plotting the bar chart for Gender and Qualification
st.subheader('Number of Students by Gender and Qualification')

# Group by Gender and Qualification, then count
gender_qualification_counts = merged_df.groupby(['qualification', 'gender']).size().unstack().fillna(0)

# Sort by the total number of registrations per gender in descending order
total_counts_gender_qualification = gender_qualification_counts.sum(axis=1).sort_values(ascending=False)
gender_qualification_counts = gender_qualification_counts.loc[total_counts_gender_qualification.index]

fig_gender_qualification, ax_gender_qualification = plt.subplots(figsize=(12, 8))
gender_qualification_counts.plot(kind='bar', stacked=True, ax=ax_gender_qualification)
ax_gender_qualification.set_title('Number of Students by Gender and Qualification (Descending)')
ax_gender_qualification.set_xlabel('qualification')
ax_gender_qualification.set_ylabel('Number of Students')
ax_gender_qualification.legend(title='gender')

st.pyplot(fig_gender_qualification)

# Display the count table
st.subheader('Count Table of Students by Gender and Qualification')
st.table(gender_qualification_counts)

# Plotting the bar chart for Gender and Caste
st.subheader('Number of Students by Gender and Caste')

# Group by Gender and Caste, then count
gender_caste_counts = merged_df.groupby(['cast', 'gender']).size().unstack().fillna(0)

# Sort by the total number of registrations per gender in descending order
total_counts_gender_caste = gender_caste_counts.sum(axis=1).sort_values(ascending=False)
gender_caste_counts = gender_caste_counts.loc[total_counts_gender_caste.index]

fig_gender_caste, ax_gender_caste = plt.subplots(figsize=(12, 8))
gender_caste_counts.plot(kind='bar', stacked=True, ax=ax_gender_caste)
ax_gender_caste.set_title('Number of Students by Gender and Caste (Descending)')
ax_gender_caste.set_xlabel('Caste')
ax_gender_caste.set_ylabel('Number of Students')
ax_gender_caste.legend(title='Gender')

st.pyplot(fig_gender_caste)

# Display the count table
st.subheader('Count Table of Students by Gender and Caste')
st.table(gender_caste_counts)

# Plotting the bar chart for Qualification and Caste
st.subheader('Number of Students by Qualification and Caste')

# Group by Qualification and Caste, then count
qualification_caste_counts = merged_df.groupby(['cast', 'qualification']).size().unstack().fillna(0)

# Sort by the total number of registrations per qualification in descending order
total_counts_qualification_caste = qualification_caste_counts.sum(axis=1).sort_values(ascending=False)
qualification_caste_counts = qualification_caste_counts.loc[total_counts_qualification_caste.index]

fig_qualification_caste, ax_qualification_caste = plt.subplots(figsize=(12, 8))
qualification_caste_counts.plot(kind='bar', stacked=True, ax=ax_qualification_caste)
ax_qualification_caste.set_title('Number of Students by Qualification and Caste (Descending)')
ax_qualification_caste.set_xlabel('Caste')
ax_qualification_caste.set_ylabel('Number of Students')
ax_qualification_caste.legend(title='Qualification')

st.pyplot(fig_qualification_caste)

# Display the count table
st.subheader('Count Table of Students by Qualification and Caste')
st.table(qualification_caste_counts)
