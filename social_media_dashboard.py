import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Page
st.set_page_config(page_title="Engagement Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("social_media_engagement1.csv")
    return df

df = load_data()

# Sidebar: platform filter
st.sidebar.header("Filter")
platforms = st.sidebar.multiselect(
    "Select Platform(s):", 
    options=df["platform"].unique(), 
    default=df["platform"].unique()
)
filtered_df = df[df["platform"].isin(platforms)]

# Title
st.markdown("<h4 style='text-align: center;'>Social Media Engagement Dashboard</h4>", unsafe_allow_html=True)

# Visualization 1: Total Engagement per Platform
st.markdown("#### Total Engagement per Platform")
engagement_sum = filtered_df.groupby("platform")[['likes', 'comments', 'shares']].sum().reset_index()
engagement_melted = engagement_sum.melt(id_vars='platform', var_name='Type', value_name='Count')

fig1, ax1 = plt.subplots(figsize=(5.5, 2.5))
sns.barplot(data=engagement_melted, y='platform', x='Count', hue='Type', palette='pastel', ax=ax1)
ax1.xaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)
ax1.tick_params(labelsize=7)
ax1.set_xlabel("")
ax1.set_ylabel("")
ax1.legend(title="", fontsize=7, loc="best", frameon=False)
sns.despine()
fig1.tight_layout()
st.pyplot(fig1)

# Columns: Monthly Trend + Platform Share
col1, col2 = st.columns(2)

# Visualization 2: Monthly Trend
with col1:
    st.markdown("#### Monthly Engagement Trend")
    filtered_df['post_month'] = pd.to_datetime(filtered_df['post_date']).dt.to_period('M').astype(str)
    monthly = filtered_df.groupby('post_month')[['likes', 'comments', 'shares']].sum().reset_index()

    fig2, ax2 = plt.subplots(figsize=(5.5, 2.5))
    for col in ['likes', 'comments', 'shares']:
        ax2.plot(monthly['post_month'], monthly[col], label=col, linewidth=2)
    ax2.set_xticks(ax2.get_xticks()[::2])
    ax2.tick_params(labelsize=7)
    ax2.legend(fontsize=7)
    fig2.tight_layout()
    st.pyplot(fig2)

# Visualization 3: Platform Share
with col2:
    st.markdown("#### Platform Share")
    platform_share = filtered_df['platform'].value_counts()
    fig3, ax3 = plt.subplots(figsize=(5.5, 2.5))
    ax3.pie(platform_share, labels=platform_share.index, autopct='%1.1f%%',
            startangle=140, colors=sns.color_palette("pastel"))
    ax3.set_title("", fontsize=10)
    st.pyplot(fig3)

# Visualization 4: Heatmap
st.markdown("#### Post Frequency: Day vs Hour")
filtered_df['post_hour'] = pd.to_datetime(filtered_df['post_time']).dt.hour
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
heat_data = pd.crosstab(filtered_df['post_day'], filtered_df['post_hour']).reindex(day_order)

fig4, ax4 = plt.subplots(figsize=(6, 3))
sns.heatmap(heat_data, cmap="Blues", linewidths=0.3, annot=True, fmt='d', cbar=False)
ax4.set_xlabel("Hour", fontsize=8)
ax4.set_ylabel("Day", fontsize=8)
ax4.tick_params(labelsize=7)
st.pyplot(fig4)

# Visualization 5: Comment Distribution by Day
st.markdown("#### Comment Distribution by Day")
fig5, ax5 = plt.subplots(figsize=(6, 3))
sns.stripplot(data=filtered_df, x='post_day', y='comments', order=day_order,
              jitter=True, size=3, palette='Set2', ax=ax5)
ax5.set_xlabel("")
ax5.set_ylabel("Comments", fontsize=8)
ax5.tick_params(labelsize=7)
fig5.tight_layout()
st.pyplot(fig5)
