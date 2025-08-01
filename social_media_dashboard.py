import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

st.set_page_config(page_title="Engagement Dashboard")
st.title("📊 Social Media Engagement Dashboard")

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

# Layout grid: gunakan kolom 2 untuk visualisasi berdampingan
col1, col2 = st.columns(2)

# 1. Bar Chart: Rata-rata engagement per platform
with col1:
    st.markdown("### 1. Avg Engagement per Platform")
    avg_engagement = filtered_df.groupby("platform")[['likes', 'comments', 'shares']].mean().reset_index()
    fig1, ax1 = plt.subplots(figsize=(4, 3))
    avg_engagement.plot(kind='bar', x='platform', ax=ax1, width=0.6)
    ax1.set_ylabel("Avg Count")
    ax1.set_title("")
    ax1.legend(loc="upper right", fontsize=6)
    plt.xticks(rotation=0, fontsize=8)
    plt.yticks(fontsize=8)
    st.pyplot(fig1)

# 2. Pie Chart: Distribusi post_type
with col2:
    st.markdown("### 2. Post Type Distribution")
    post_type_counts = filtered_df['post_type'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(3.8, 3.8))
    ax2.pie(
        post_type_counts,
        labels=post_type_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 7}
    )
    ax2.set_title("")
    st.pyplot(fig2)

# 3. Line Chart: Total Engagement Over Time (Monthly)
st.markdown("### 3. Monthly Engagement Trend")
engagement_over_time = filtered_df.groupby("month")[['likes', 'comments', 'shares']].sum().reset_index()
fig3, ax3 = plt.subplots(figsize=(6.5, 3.2))
for col in ['likes', 'comments', 'shares']:
    ax3.plot(engagement_over_time['month'], engagement_over_time[col], label=col, linewidth=2)
ax3.set_xlabel("Month", fontsize=9)
ax3.set_ylabel("Count", fontsize=9)
ax3.legend(fontsize=7)
plt.xticks(rotation=45, fontsize=7)
plt.yticks(fontsize=7)
st.pyplot(fig3)

# 4. Box Plot: Engagement by Sentiment
st.markdown("### 4. Engagement by Sentiment")
fig4, ax4 = plt.subplots(1, 3, figsize=(9, 3))
sns.boxplot(data=filtered_df, x='sentiment_score', y='likes', ax=ax4[0])
ax4[0].set_title("Likes", fontsize=9)
sns.boxplot(data=filtered_df, x='sentiment_score', y='comments', ax=ax4[1])
ax4[1].set_title("Comments", fontsize=9)
sns.boxplot(data=filtered_df, x='sentiment_score', y='shares', ax=ax4[2])
ax4[2].set_title("Shares", fontsize=9)
for axis in ax4:
    axis.tick_params(labelsize=7)
    axis.set_xlabel("")
    axis.set_ylabel("")
st.pyplot(fig4)

# 5. Heatmap: Engagement by Day and Hour
st.markdown("### 5. Post Frequency: Day vs Hour")
heat_data = filtered_df.groupby(['post_day', 'hour']).size().unstack().fillna(0)
fig5, ax5 = plt.subplots(figsize=(7, 3.5))
sns.heatmap(heat_data, cmap="YlGnBu", annot=True, fmt=".0f", ax=ax5, cbar=False, annot_kws={"size": 7})
ax5.set_title("")
ax5.set_xlabel("Hour", fontsize=8)
ax5.set_ylabel("Day", fontsize=8)
plt.xticks(fontsize=7)
plt.yticks(fontsize=7)
st.pyplot(fig5)
