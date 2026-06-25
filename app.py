import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ============= PAGE CONFIG ============= #

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============= THEME STATE INITIALIZATION ============= #

if "theme" not in st.session_state:
    st.session_state.theme = "light"

# ============= DYNAMIC CSS - User Selectable Theme ============= #

def get_theme_colors(theme):
    """Returns color scheme based on selected theme"""
    if theme == "dark":
        return {
            'bg_primary': '#1a1a1a',
            'bg_secondary': '#0f0f0f',
            'bg_tertiary': '#2a2a2a',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'text_tertiary': '#888888',
            'border_color': '#404040',
            'border_light': '#2a2a2a',
            'card_background': '#252525',
            'header_bg_start': '#1ea853',
            'header_bg_end': '#0f7a4a',
        }
    else:  # light
        return {
            'bg_primary': '#ffffff',
            'bg_secondary': '#f5f5f5',
            'bg_tertiary': '#f9f9f9',
            'text_primary': '#000000',
            'text_secondary': '#667F7F',
            'text_tertiary': '#999999',
            'border_color': '#e0e0e0',
            'border_light': '#f0f0f0',
            'card_background': '#ffffff',
            'header_bg_start': '#25D366',
            'header_bg_end': '#128C7E',
        }

# Get current theme colors
current_colors = get_theme_colors(st.session_state.theme)

# Generate dynamic CSS
css_theme = f"""
<style>
    * {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    }}
    
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {current_colors['bg_primary']};
        color: {current_colors['text_primary']};
    }}
    
    [data-testid="stMainBlockContainer"] {{
        padding-top: 0;
        background: linear-gradient(135deg, {current_colors['bg_primary']} 0%, {current_colors['bg_secondary']} 100%);
    }}
    
    /* ========== SIDEBAR STYLING ========== */
    [data-testid="stSidebar"] {{
        background: {current_colors['bg_primary']} !important;
        border-right: 1px solid {current_colors['border_color']} !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
        background: {current_colors['bg_primary']} !important;
    }}
    
    [data-testid="stSidebar"] > div {{
        background: {current_colors['bg_primary']} !important;
    }}
    
    /* Sidebar Title */
    .sidebar-title {{
        font-size: 22px;
        font-weight: 700;
        color: {current_colors['text_primary']};
        margin: 1rem 0 1.5rem 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    
    /* Theme Toggle Container */
    .theme-toggle {{
        background: {current_colors['bg_tertiary']};
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border: 1px solid {current_colors['border_color']};
    }}
    
    .theme-toggle-label {{
        font-size: 12px;
        font-weight: 600;
        color: {current_colors['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        display: block;
    }}
    
    /* Sidebar Divider */
    [data-testid="stSidebar"] hr {{
        border: none !important;
        height: 1px !important;
        background: {current_colors['border_color']} !important;
        margin: 1.5rem 0 !important;
    }}
    
    /* File Uploader Styling */
    [data-testid="stFileUploader"] {{
        background: {current_colors['bg_tertiary']} !important;
        border: 2px dashed #25D366 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin: 1rem 0 1.5rem 0 !important;
    }}
    
    [data-testid="stFileUploader"] label {{
        font-weight: 600 !important;
        color: {current_colors['text_primary']} !important;
        font-size: 14px !important;
        margin-bottom: 10px !important;
    }}
    
    /* Selectbox Styling */
    [data-testid="stSelectbox"] {{
        margin: 1rem 0 1.5rem 0 !important;
    }}
    
    [data-testid="stSelectbox"] label {{
        font-weight: 600 !important;
        color: {current_colors['text_primary']} !important;
        font-size: 14px !important;
        margin-bottom: 8px !important;
    }}
    
    [data-testid="stSelectbox"] > div > div {{
        border: 1px solid {current_colors['border_color']} !important;
        border-radius: 10px !important;
        background: {current_colors['card_background']} !important;
    }}
    
    [data-testid="stSelectbox"] [role="combobox"] {{
        color: {current_colors['text_primary']} !important;
        font-weight: 500 !important;
        border: 1px solid {current_colors['border_color']} !important;
        border-radius: 10px !important;
        background: {current_colors['card_background']} !important;
    }}
    
    [data-testid="stSelectbox"] [role="combobox"]:focus-visible {{
        border-color: #25D366 !important;
        box-shadow: 0 0 0 3px rgba(37, 211, 102, 0.1) !important;
    }}
    
    /* ========== MAIN CONTENT ========== */
    
    /* Header Section */
    .header-container {{
        background: linear-gradient(135deg, {current_colors['header_bg_start']} 0%, {current_colors['header_bg_end']} 100%);
        padding: 2.5rem 2rem;
        border-radius: 0 0 20px 20px;
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 8px 24px rgba(37, 211, 102, 0.15);
    }}
    
    .header-container h1 {{
        margin: 0;
        font-size: 36px;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: white;
    }}
    
    .header-subtitle {{
        margin-top: 8px;
        font-size: 14px;
        opacity: 0.95;
        font-weight: 400;
        color: white;
    }}
    
    .user-info-badge {{
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 8px 16px;
        border-radius: 20px;
        margin-top: 1.5rem;
        font-size: 13px;
        font-weight: 500;
        backdrop-filter: blur(10px);
        color: white;
    }}
    
    /* Metric Cards */
    .metric-card {{
        background: {current_colors['card_background']};
        padding: 24px 20px;
        border-radius: 16px;
        border: 1px solid {current_colors['border_color']};
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(37, 211, 102, 0.1);
        border-color: #25D366;
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #25D366, #128C7E);
    }}
    
    .metric-card h3 {{
        color: {current_colors['text_secondary']};
        margin: 0 0 12px 0;
        font-size: 13px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .metric-card .metric-value {{
        color: #25D366;
        font-size: 40px;
        font-weight: 700;
        line-height: 1;
        margin: 0;
    }}
    
    .metric-card .metric-unit {{
        color: {current_colors['text_tertiary']};
        font-size: 12px;
        margin-top: 8px;
        font-weight: 400;
    }}
    
    /* Section Headers */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 12px;
        border-bottom: 2px solid {current_colors['border_color']};
    }}
    
    .section-header h2 {{
        margin: 0;
        font-size: 20px;
        font-weight: 700;
        color: {current_colors['text_primary']};
    }}
    
    .section-header .emoji {{
        font-size: 24px;
    }}
    
    /* Charts Container */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: {current_colors['card_background']};
        border: 1px solid {current_colors['border_color']};
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }}
    
    /* DataFrames */
    [data-testid="dataframe"] {{
        border: 1px solid {current_colors['border_color']} !important;
        border-radius: 12px !important;
        overflow: hidden;
    }}
    
    [data-testid="dataframe"] thead {{
        background: {current_colors['bg_tertiary']} !important;
    }}
    
    [data-testid="dataframe"] th {{
        color: {current_colors['text_primary']} !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        padding: 12px !important;
    }}
    
    [data-testid="dataframe"] td {{
        padding: 12px !important;
        border-bottom: 1px solid {current_colors['border_light']} !important;
        color: {current_colors['text_primary']} !important;
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, #25D366, #128C7E) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.2) !important;
        width: 100% !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(37, 211, 102, 0.3) !important;
    }}
    
    /* Divider */
    hr {{
        border: none !important;
        height: 1px !important;
        background: {current_colors['border_color']} !important;
        margin: 2rem 0 !important;
    }}
    
    /* Responsive */
    @media (max-width: 768px) {{
        .header-container h1 {{
            font-size: 28px;
        }}
        
        .metric-card .metric-value {{
            font-size: 32px;
        }}
    }}
</style>
"""

st.markdown(css_theme, unsafe_allow_html=True)

# ============= CHART STYLING FUNCTION ============= #

def style_chart_for_theme(ax, xlabel=None, ylabel=None, title=None):
    """Apply theme-aware styling to matplotlib charts"""
    chart_bg = '#ffffff' if st.session_state.theme == 'light' else '#252525'
    text_color = '#000000' if st.session_state.theme == 'light' else '#ffffff'
    grid_color = '#e0e0e0' if st.session_state.theme == 'light' else '#404040'
    
    ax.set_facecolor(chart_bg)
    ax.grid(True, alpha=0.1, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(grid_color)
    ax.spines['bottom'].set_color(grid_color)
    
    # Set text color for axis labels
    ax.tick_params(colors=text_color)
    
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11, fontweight='600', color=text_color)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11, fontweight='600', color=text_color)
    if title:
        ax.set_title(title, fontsize=13, fontweight='600', pad=15, color=text_color)

# ============= SIDEBAR ============= #

st.sidebar.markdown("""
<div class="sidebar-title">
    💬 WhatsApp Chat Analyzer
</div>
""", unsafe_allow_html=True)

# Theme Toggle
st.sidebar.markdown("""
<div class="theme-toggle">
    <label class="theme-toggle-label">🎨 Theme</label>
</div>
""", unsafe_allow_html=True)

theme_option = st.sidebar.radio(
    "Select Theme",
    options=["light", "dark"],
    format_func=lambda x: "☀️ Light" if x == "light" else "🌙 Dark",
    horizontal=True,
    label_visibility="collapsed"
)

if theme_option != st.session_state.theme:
    st.session_state.theme = theme_option
    st.rerun()

st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    "Upload your WhatsApp chat file",
    type=["txt"],
    help="Export your WhatsApp chat and upload here (without media)"
)

st.sidebar.markdown("---")

# ============= MAIN APP ============= #

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    
    # User List
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    
    selected_user = st.sidebar.selectbox(
        "Analyze conversation with",
        user_list,
        help="Select 'Overall' for group-wide statistics"
    )
    
    if st.sidebar.button("📊 Generate Report", use_container_width=True):
        # Fetch Stats
        num_messages, words, num_media_msg, num_links = helper.fetch_stats(selected_user, df)
        
        # ============= HEADER ============= #
        header_text = "Overall Statistics" if selected_user == "Overall" else f"Conversation with {selected_user}"
        st.markdown(f"""
        <div class="header-container">
            <h1>💬 Chat Analytics</h1>
            <div class="header-subtitle">Deep insights into your WhatsApp conversations</div>
            <div class="user-info-badge">Analyzing: {header_text}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # ============= TOP STATISTICS ============= #
        st.markdown('<div class="section-header"><span class="emoji">📊</span><h2>Key Metrics</h2></div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Messages</h3>
                <p class="metric-value">{num_messages:,}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Words Used</h3>
                <p class="metric-value">{words:,}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Media Shared</h3>
                <p class="metric-value">{num_media_msg:,}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Links Shared</h3>
                <p class="metric-value">{num_links:,}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # ============= MONTHLY TIMELINE ============= #
        st.markdown('<div class="section-header"><span class="emoji">📈</span><h2>Monthly Trend</h2></div>', unsafe_allow_html=True)
        
        timeline = helper.monthly_timeline(selected_user, df)
        
        with st.container(border=True):
            fig, ax = plt.subplots(figsize=(14, 4), facecolor='white')
            ax.plot(timeline['time'], timeline['message'], color='#25D366', linewidth=3, marker='o', markersize=6)
            ax.fill_between(range(len(timeline)), timeline['message'], alpha=0.1, color='#25D366')
            style_chart_for_theme(ax, ylabel='Messages')
            plt.xticks(rotation=45, ha='right', fontsize=10)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
        
        # ============= DAILY TIMELINE ============= #
        st.markdown('<div class="section-header"><span class="emoji">📅</span><h2>Daily Activity</h2></div>', unsafe_allow_html=True)
        
        daily_timeline = helper.daily_timeline(selected_user, df)
        
        with st.container(border=True):
            fig, ax = plt.subplots(figsize=(14, 5), facecolor='white')
            
            # Plot the data
            ax.plot(range(len(daily_timeline)), daily_timeline['message'], color='#128C7E', linewidth=2.5, alpha=0.8, marker='o', markersize=4)
            ax.fill_between(range(len(daily_timeline)), daily_timeline['message'], alpha=0.15, color='#128C7E')
            
            # Better x-axis handling - show every nth label to avoid crowding
            num_points = len(daily_timeline)
            step = max(1, num_points // 15)  # Show max 15 labels
            
            xtick_positions = range(0, num_points, step)
            xtick_labels = [str(daily_timeline['only_date'].iloc[i]) if i < len(daily_timeline) else '' for i in xtick_positions]
            
            ax.set_xticks(xtick_positions)
            ax.set_xticklabels(xtick_labels, rotation=45, ha='right', fontsize=9)
            
            style_chart_for_theme(ax, xlabel='Date', ylabel='Messages')
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
        
        # ============= ACTIVITY MAP ============= #
        st.markdown('<div class="section-header"><span class="emoji">🔥</span><h2>Activity Patterns</h2></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            with st.container(border=True):
                busy_day = helper.week_activity(selected_user, df)
                fig, ax = plt.subplots(figsize=(8, 5), facecolor='white')
                bars = ax.bar(busy_day.index, busy_day.values, color='#25D366', edgecolor=current_colors['border_color'], linewidth=1.5)
                style_chart_for_theme(ax, ylabel='Messages', title='Busiest Days of Week')
                plt.xticks(rotation=45, ha='right', fontsize=10)
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)
        
        with col2:
            with st.container(border=True):
                busy_month = helper.month_activity(selected_user, df)
                fig, ax = plt.subplots(figsize=(8, 5), facecolor='white')
                bars = ax.bar(busy_month.index, busy_month.values, color='#128C7E', edgecolor=current_colors['border_color'], linewidth=1.5)
                style_chart_for_theme(ax, ylabel='Messages', title='Busiest Months')
                plt.xticks(rotation=45, ha='right', fontsize=10)
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)
        
        # ============= MOST ACTIVE USERS ============= #
        if selected_user == 'Overall':
            st.markdown('<div class="section-header"><span class="emoji">👥</span><h2>Most Active Participants</h2></div>', unsafe_allow_html=True)
            
            x, new_df = helper.most_active_user(df)
            
            col1, col2 = st.columns([2, 1], gap="large")
            
            with col1:
                with st.container(border=True):
                    fig, ax = plt.subplots(figsize=(10, 5), facecolor='white')
                    bars = ax.bar(x.index, x.values, color='#25D366', edgecolor=current_colors['border_color'], linewidth=1.5, alpha=0.9)
                    style_chart_for_theme(ax, ylabel='Number of Messages')
                    plt.xticks(rotation=45, ha='right', fontsize=10)
                    plt.tight_layout()
                    st.pyplot(fig, use_container_width=True)
            
            with col2:
                with st.container(border=True):
                    st.markdown("**Leaderboard**")
                    st.dataframe(new_df, use_container_width=True, hide_index=True)
        
        # ============= WORD CLOUD ============= #
        st.markdown('<div class="section-header"><span class="emoji">☁️</span><h2>Word Cloud</h2></div>', unsafe_allow_html=True)
        
        wc = helper.create_wordcloud(selected_user, df)
        
        with st.container(border=True):
            fig, ax = plt.subplots(figsize=(14, 6), facecolor='white')
            ax.imshow(wc, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig, use_container_width=True)
        
        # ============= MOST COMMON WORDS ============= #
        st.markdown('<div class="section-header"><span class="emoji">📝</span><h2>Most Frequently Used Words</h2></div>', unsafe_allow_html=True)
        
        most_common_df = helper.most_common_words(selected_user, df)
        
        with st.container(border=True):
            fig, ax = plt.subplots(figsize=(10, 8), facecolor='white')
            colors = ['#25D366' if i % 2 == 0 else '#128C7E' for i in range(len(most_common_df))]
            ax.barh(most_common_df[0], most_common_df[1], color=colors, edgecolor=current_colors['border_color'], linewidth=1)
            ax.invert_yaxis()
            style_chart_for_theme(ax, xlabel='Frequency')
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
        
        # ============= EMOJI ANALYSIS ============= #
        st.markdown('<div class="section-header"><span class="emoji">😀</span><h2>Emoji Usage</h2></div>', unsafe_allow_html=True)
        
        emoji_df = helper.emoji_helper(selected_user, df)
        
        col1, col2 = st.columns([1, 1.2], gap="large")
        
        with col1:
            with st.container(border=True):
                st.markdown("**Top Emojis**")
                st.dataframe(emoji_df.head(10), use_container_width=True, hide_index=True)
        
        with col2:
            with st.container(border=True):
                fig, ax = plt.subplots(figsize=(8, 8), facecolor='white')
                colors_pie = ['#25D366', '#128C7E', '#075E54', '#34B7A6', '#20AA84']
                ax.pie(
                    emoji_df[1].head(),
                    labels=emoji_df[0].head(),
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=colors_pie,
                    textprops={'fontsize': 10, 'fontweight': '600'},
                    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
                )
                ax.set_facecolor('white')
                st.pyplot(fig, use_container_width=True)
        
        # Footer
        st.markdown("---")
        footer_color = current_colors['text_secondary']
        st.markdown(f"""
        <div style="text-align: center; color: {footer_color}; font-size: 12px; margin-top: 2rem;">
            <p>💬 WhatsApp Chat Analyzer • Designed with ❤️</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="header-container">
        <h1>💬 WhatsApp Chat Analyzer</h1>
        <div class="header-subtitle">Unlock insights into your WhatsApp conversations</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("📱")
    
    st.markdown("""
    ## Get Started
    
    Upload your WhatsApp chat export to begin analyzing your conversations.
    
    ### How to export your chat:
    
    1. **Open WhatsApp** on your phone
    2. **Select a chat** (individual or group)
    3. **Tap Options** (⋯) → **More** → **Export chat**
    4. **Choose "Without media"** for faster processing
    5. **Upload the file** using the sidebar
    
    ### What you'll discover:
    
    - 📊 **Message Statistics** - Total messages, words, media, and links
    - 📈 **Trends** - Monthly and daily messaging patterns
    - 🔥 **Peak Times** - Your most active days and months
    - 👥 **Top Contributors** - Most active participants
    - ☁️ **Word Cloud** - Visualize your most-used words
    - 😀 **Emoji Stats** - Your favorite emojis
    
    Ready to dive in? Upload a chat file to the left! 👈
    """, unsafe_allow_html=True)