import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Engagement Dashboard")
st.markdown("## 📊 Social Media Engagement Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("social_media_engagement1.csv")
    df['post_time'] = pd.to_datetime(df['post_time'], errors='coerce')
    df['hour'] = df['post_time'].dt.hour
    df['month'] = df['post_time'].dt.to_period("M").astype(str)
    df['post_day'] = df['post_time'].dt.day_name()
    return df

df = load_data()

# Sidebar filter
platforms = df['platform'].unique().tolist()
selected_platforms = st.sidebar.multiselect("Select Platform(s):", platforms, default=platforms)
filtered_df = df[df['platform'].isin(selected_platforms)]

# --- Visualisasi 1 ---
st.markdown("#### Total Engagement per Platform")
total_engagement = filtered_df.groupby("platform")[['likes', 'comments', 'shares']].sum().reset_index()
total_melted = pd.melt(
    total_engagement,
    id_vars='platform',
    value_vars=['likes', 'comments', 'shares'],
    var_name='Engagement Type',
    value_name='Count'
)
fig1, ax1 = plt.subplots(figsize=(6, 3.5))
sns.barplot(
    data=total_melted,
    y='platform',
    x='Count',
    hue='Engagement Type',
    palette='Set2',
    edgecolor='black'
)
ax1.set_xlabel("Total", fontsize=8)
ax1.set_ylabel("")
ax1.tick_params(labelsize=8)
ax1.legend(title="", fontsize=7)
st.pyplot(fig1)

# --- Visualisasi 2 & 3 berdampingan ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Post Type Distribution")
    post_type_counts = filtered_df['post_type'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(5, 3.5))
    ax2.pie(
        post_type_counts,
        labels=post_type_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 8}
    )
    st.pyplot(fig2)

with col2:
    st.markdown("#### Monthly Engagement Trend")
    monthly = filtered_df.groupby("month")[['likes', 'comments', 'shares']].sum().reset_index()
    fig3, ax3 = plt.subplots(figsize=(5, 3.5))
    for col in ['likes', 'comments', 'shares']:
        ax3.plot(monthly['month'], monthly[col], label=col, linewidth=2)
    ax3.set_xlabel("Month", fontsize=8)
    ax3.set_ylabel("Count", fontsize=8)
    ax3.legend(fontsize=7)
    ax3.tick_params(labelsize=7)
    plt.xticks(rotation=45, fontsize=7)
    st.pyplot(fig3)

# --- Visualisasi 4: Boxplot Sentiment ---
st.markdown("#### Engagement by Sentiment Score")
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

# --- Visualisasi 5: Heatmap Day vs Hour ---
st.markdown("#### Post Frequency: Day vs Hour")
heat_data = filtered_df.groupby(['post_day', 'hour']).size().unstack().fillna(0)
fig5, ax5 = plt.subplots(figsize=(7, 3.5))
sns.heatmap(heat_data, cmap="YlGnBu", annot=True, fmt=".0f", ax=ax5, cbar=False, annot_kws={"size": 7})
ax5.set_xlabel("Hour", fontsize=8)
ax5.set_ylabel("Day", fontsize=8)
plt.xticks(fontsize=7)
plt.yticks(fontsize=7)
st.pyplot(fig5)

#---
fig, ax = plt.subplots(figsize=(6, 3))
sns.stripplot(data=filtered_df, x='post_day', y='comments', order=day_order, jitter=True, size=3, palette='Set2')
ax.set_title("Comment Distribution by Day", fontsize=10)
ax.set_xlabel("")
ax.set_ylabel("Comments", fontsize=8)
st.pyplot(fig)
