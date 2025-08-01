import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

st.set_page_config(layout="wide")
st.title("Social Media Engagement Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("social_media_engagement1.csv")
    df['post_time'] = pd.to_datetime(df['post_time'], errors='coerce')
    df['hour'] = df['post_time'].dt.hour
    df['month'] = df['post_time'].dt.to_period("M").astype(str)
    return df

df = load_data()

# Sidebar filter
platforms = df['platform'].unique().tolist()
selected_platforms = st.sidebar.multiselect("Select Platform(s):", platforms, default=platforms)

filtered_df = df[df['platform'].isin(selected_platforms)]

# 1. Bar Chart: Rata-rata engagement per platform
st.subheader("1. Average Engagement per Platform")
avg_engagement = filtered_df.groupby("platform")[['likes', 'comments', 'shares']].mean().reset_index()
fig1, ax1 = plt.subplots()
avg_engagement.plot(kind='bar', x='platform', ax=ax1)
ax1.set_ylabel("Average Count")
ax1.set_title("Average Likes, Comments, Shares per Platform")
st.pyplot(fig1)

# 2. Pie Chart: Distribusi post_type
st.subheader("2. Distribution of Post Type")
post_type_counts = filtered_df['post_type'].value_counts()
fig2, ax2 = plt.subplots()
ax2.pie(
    post_type_counts,
    labels=post_type_counts.index,
    autopct='%1.1f%%',
    startangle=90
)
ax2.set_title("Post Type Distribution")
st.pyplot(fig2)

# 3. Line Chart: Total Engagement Over Time (Monthly)
st.subheader("3. Engagement Trend Over Time")
engagement_over_time = filtered_df.groupby("month")[['likes', 'comments', 'shares']].sum().reset_index()
fig3, ax3 = plt.subplots()
for col in ['likes', 'comments', 'shares']:
    ax3.plot(engagement_over_time['month'], engagement_over_time[col], label=col)
ax3.set_title("Monthly Engagement Trend")
ax3.set_xlabel("Month")
ax3.set_ylabel("Count")
ax3.legend()
plt.xticks(rotation=45)
st.pyplot(fig3)

# 4. Box Plot: Engagement by Sentiment
st.subheader("4. Engagement by Sentiment")
fig4, ax4 = plt.subplots(1, 3, figsize=(15, 5))
sns.boxplot(data=filtered_df, x='sentiment_score', y='likes', ax=ax4[0])
ax4[0].set_title("Likes")
sns.boxplot(data=filtered_df, x='sentiment_score', y='comments', ax=ax4[1])
ax4[1].set_title("Comments")
sns.boxplot(data=filtered_df, x='sentiment_score', y='shares', ax=ax4[2])
ax4[2].set_title("Shares")
st.pyplot(fig4)

# 5. Heatmap: Engagement by Day and Hour
st.subheader("5. Posting Activity Heatmap (Day vs Hour)")
heat_data = filtered_df.groupby(['post_day', 'hour']).size().unstack().fillna(0)
fig5, ax5 = plt.subplots(figsize=(12, 6))
sns.heatmap(heat_data, cmap="YlGnBu", annot=True, fmt=".0f", ax=ax5)
ax5.set_title("Post Frequency by Day and Hour")
st.pyplot(fig5)
