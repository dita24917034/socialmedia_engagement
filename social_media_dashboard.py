import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Styling
st.set_page_config(layout="wide")
st.markdown("#### Social Media Engagement Dashboard")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("social_media_engagement1.csv")
    return df

df = load_data()

# Sidebar filter
platforms = df['platform'].unique().tolist()
selected_platforms = st.sidebar.multiselect("Select Platform(s):", platforms, default=platforms)
filtered_df = df[df['platform'].isin(selected_platforms)]

# Extract month from post_time
filtered_df['post_month'] = pd.to_datetime(filtered_df['post_time'], errors='coerce').dt.to_period('M').astype(str)

# Visualisasi 1: Clustered Bar Chart (Total Engagement per Platform)
st.markdown("##### Total Engagement per Platform")
total_engagement = filtered_df.groupby("platform")[['likes', 'comments', 'shares']].sum().reset_index()
total_melted = total_engagement.melt(id_vars='platform', var_name='Engagement Type', value_name='Count')

fig1, ax1 = plt.subplots(figsize=(6, 2.8))
sns.barplot(data=total_melted, y='platform', x='Count', hue='Engagement Type', palette='pastel', ax=ax1, edgecolor='gray')
ax1.xaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.6)
ax1.set_xlabel("")
ax1.set_ylabel("")
ax1.legend(title="", fontsize=7)
ax1.tick_params(labelsize=7)
sns.despine()
fig1.tight_layout()
col1, col2 = st.columns([1, 1])
col1.pyplot(fig1)

# Visualisasi 2 & 3: Monthly Trend + Pie Chart
# Monthly trend
monthly_engagement = filtered_df.groupby(['post_month'])[['likes', 'comments', 'shares']].sum().reset_index()
fig2, ax2 = plt.subplots(figsize=(5.5, 2.5))
monthly_engagement.set_index('post_month').plot(ax=ax2, marker='o', linewidth=1.5)
ax2.set_xlabel("")
ax2.set_ylabel("")
ax2.set_title("Monthly Engagement Trend", fontsize=10)
ax2.tick_params(labelsize=7)
ax2.grid(True, linestyle="--", alpha=0.3)
fig2.tight_layout()

# Pie Chart
platform_share = filtered_df['platform'].value_counts()
fig3, ax3 = plt.subplots(figsize=(3.5, 3.5))
ax3.pie(platform_share, labels=platform_share.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
ax3.set_title("Platform Share", fontsize=10)

# Tampilkan berdampingan
col2.pyplot(fig2)
col2.pyplot(fig3)

# Visualisasi 4: Heatmap Post Frequency (day vs hour)
st.markdown("##### Post Frequency: Day vs Hour")
heatmap_data = filtered_df.copy()
heatmap_data['hour'] = pd.to_datetime(heatmap_data['post_time'], errors='coerce').dt.hour
pivot = heatmap_data.pivot_table(index='post_day', columns='hour', values='platform', aggfunc='count').fillna(0)
fig4, ax4 = plt.subplots(figsize=(7, 3))
sns.heatmap(pivot, cmap='YlGnBu', linewidths=0.5, ax=ax4)
ax4.set_title("Posting Activity Heatmap", fontsize=10)
ax4.set_xlabel("Hour of Day")
ax4.set_ylabel("Day of Week")
fig4.tight_layout()
st.pyplot(fig4)

# Visualisasi 5: Comment Distribution by Day (stripplot)
st.markdown("##### Comment Distribution by Day")
fig5, ax5 = plt.subplots(figsize=(6, 2.5))
sns.stripplot(data=filtered_df, x='post_day', y='comments', jitter=True, palette='pastel', ax=ax5)
ax5.set_xlabel("Post Day")
ax5.set_ylabel("Comments")
ax5.set_title("Comment Distribution by Day", fontsize=10)
fig5.tight_layout()
st.pyplot(fig5)
