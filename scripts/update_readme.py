#!/usr/bin/env python3
"""
██████╗  ██████╗ ██╗     ██║████████╗██╗  ██╗███████╗ ██████╗ ███╗   ██╗
██╔══██╗██╔═══██╗██║     ██║╚══██╔══╝██║  ██║██╔════╝██╔═══██╗████╗  ██║
██████╔╝██║   ██║██║     ██║   ██║   ███████║█████╗  ██║   ██║██╔██╗ ██║
██╔═══╝ ██║   ██║██║     ██║   ██║   ██╔══██║██╔══╝  ██║   ██║██║╚██╗██║
██║     ╚██████╔╝███████╗██║   ██║   ██║  ██║███████╗╚██████╔╝██║ ╚████║
╚═╝      ╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝

Politheon – AI-driven Policy Intelligence

═══════════════════════════════════════════════════════════════════════════

Dynamic README Updater

Updates the organization README.md based on current EST time.
Automatically rotates through 8 time-based themes every 3 hours.

═══════════════════════════════════════════════════════════════════════════
"""

import re
from datetime import datetime
import pytz

# Time themes configuration
TIME_THEMES = {
    "early_morning": {
        "start_hour": 3,
        "end_hour": 6,
        "emoji": "🌃",
        "badge_label": "NIGHT WATCH",
        "badge_text": "Policy_Never_Rests",
        "time_range": "3am-6am",
        "tagline": "Policy Never Rests",
        "header_desc": "While%20the%20Capitol%20Sleeps%2C%20We%20Watch",
        "bullets": "🏛️ Chambers dark, signals bright • 👁️ The Council monitors • 📡 Silent intelligence flows",
        "banner_colors": "0:0B1F35,50:1A2332,100:2C3E50",
        "badge_color": "0B1F35",
        "badge_label_color": "1A2332",
        "time_badge_color": "2C3E50",
        "divider1_colors": "0:0B1F35,50:1A2332,100:2C3E50",
        "divider2_colors": "0:2C3E50,50:1A2332,100:0B1F35",
        "footer_colors": "0:2C3E50,50:4A5F7F,100:0B1F35",
        "font_color": "D6A649",
        "stroke_color": "D6A649",
        "typing_phrases": [
            "Signals+Never+Sleep",
            "The+Council+Stands+Watch",
            "Monitoring+While+Others+Rest",
            "Policy+Intelligence%2C+24%2F7",
            "Early+Warnings+Before+Dawn",
            "Night+Shift%3A+Always+Active",
            "Tracking+Momentum+in+Darkness",
            "Silent+Vigilance+%7C+Loud+Impact"
        ]
    },
    "dawn": {
        "start_hour": 6,
        "end_hour": 9,
        "emoji": "🌅",
        "badge_label": "DAWN BRIEF",
        "badge_text": "First_Light_First_Insight",
        "time_range": "6am-9am",
        "tagline": "First Light, First Insight",
        "header_desc": "Intelligence%20Before%20Coffee",
        "bullets": "📊 Today's priorities surfaced • ⚖️ Signals ranked and ready • 🎯 Focus before the flood",
        "banner_colors": "0:2C3E50,50:0B1F35,100:D6A649",
        "badge_color": "D6A649",
        "badge_label_color": "0B1F35",
        "time_badge_color": "B8935E",
        "divider1_colors": "0:2C3E50,50:0B1F35,100:D6A649",
        "divider2_colors": "0:D6A649,50:0B1F35,100:2C3E50",
        "footer_colors": "0:0B1F35,50:2C3E50,100:4A5F7F",
        "font_color": "FFFFFF",
        "stroke_color": "0B1F35",
        "typing_phrases": [
            "Your+Daily+Intelligence+Brief",
            "Priorities+Surfaced+at+Dawn",
            "The+Council's+Morning+Report",
            "Insight+Before+Inbox",
            "Policy+Signals+%7C+Delivered+Daily",
            "Early+Detection+%7C+Clear+Direction",
            "Start+Sharp+%7C+Stay+Ahead",
            "Intelligence+That+Moves+You"
        ]
    },
    "morning_session": {
        "start_hour": 9,
        "end_hour": 12,
        "emoji": "🏛️",
        "badge_label": "SESSION ACTIVE",
        "badge_text": "Bills_in_Motion",
        "time_range": "9am-12pm",
        "tagline": "Bills in Motion, Agents Tracking",
        "header_desc": "The%20Capitol%20is%20in%20Session",
        "bullets": "📈 Committees convening • ⚡ Momentum accelerating • 🎯 The Council analyzes",
        "banner_colors": "0:0B1F35,50:2C3E50,100:4A5F7F",
        "badge_color": "4A5F7F",
        "badge_label_color": "0B1F35",
        "time_badge_color": "2C3E50",
        "divider1_colors": "0:0B1F35,50:2C3E50,100:4A5F7F",
        "divider2_colors": "0:4A5F7F,50:2C3E50,100:0B1F35",
        "footer_colors": "0:D6A649,50:B8935E,100:8B7355",
        "font_color": "FFFFFF",
        "stroke_color": "D6A649",
        "typing_phrases": [
            "The+Council+is+Active",
            "Tracking+Every+Introduction",
            "Real-Time+Legislative+Intelligence",
            "Momentum+Measured+%7C+Risks+Mapped",
            "From+Bill+Drop+to+Passage+Prediction",
            "Session+Watch+%7C+Agent+Powered",
            "Capitol+Activity+%7C+Decoded+Live",
            "Intelligence+at+the+Speed+of+Policy"
        ]
    },
    "midday_analysis": {
        "start_hour": 12,
        "end_hour": 15,
        "emoji": "📊",
        "badge_label": "PEAK ANALYSIS",
        "badge_text": "Strategy_Sharper",
        "time_range": "12pm-3pm",
        "tagline": "Signals Clear, Strategy Sharper",
        "header_desc": "Policy%20Intelligence%20at%20Full%20Speed",
        "bullets": "🎯 Patterns emerging • 💡 Stakeholders mapped • 📡 Discourse analyzed",
        "banner_colors": "0:4A5F7F,50:2C3E50,100:0B1F35",
        "badge_color": "4A5F7F",
        "badge_label_color": "0B1F35",
        "time_badge_color": "2C3E50",
        "divider1_colors": "0:4A5F7F,50:2C3E50,100:0B1F35",
        "divider2_colors": "0:0B1F35,50:2C3E50,100:4A5F7F",
        "footer_colors": "0:D6A649,50:B8935E,100:8B7355",
        "font_color": "FFFFFF",
        "stroke_color": "D6A649",
        "typing_phrases": [
            "Multi-Source+Intelligence+Flowing",
            "The+Council+Processes+%7C+You+Decide",
            "Lobbying+%2B+Legislation+%2B+Discourse",
            "Insight+Before+Noise",
            "From+Signal+to+Strategy",
            "Data+Floods+In+%7C+Clarity+Flows+Out",
            "Real-Time+%7C+Right+Time",
            "Policy+Moves+Fast+%7C+We+Move+Faster"
        ]
    },
    "afternoon_focus": {
        "start_hour": 15,
        "end_hour": 18,
        "emoji": "🎯",
        "badge_label": "ACTION HOURS",
        "badge_text": "Decisions_Enabled",
        "time_range": "3pm-6pm",
        "tagline": "Intelligence Delivered, Decisions Enabled",
        "header_desc": "Your%20Window%20to%20Act",
        "bullets": "📋 Priorities ranked • 🛡️ Risks flagged • ⚡ Opportunities surfaced",
        "banner_colors": "0:0B1F35,50:4A5F7F,100:D6A649",
        "badge_color": "D6A649",
        "badge_label_color": "0B1F35",
        "time_badge_color": "B8935E",
        "divider1_colors": "0:0B1F35,50:4A5F7F,100:D6A649",
        "divider2_colors": "0:D6A649,50:4A5F7F,100:0B1F35",
        "footer_colors": "0:0B1F35,50:2C3E50,100:4A5F7F",
        "font_color": "FFFFFF",
        "stroke_color": "0B1F35",
        "typing_phrases": [
            "From+Intelligence+to+Impact",
            "Today's+Signals+%7C+Tomorrow's+Edge",
            "The+Council+Advises+%7C+You+Lead",
            "Strategic+Clarity+in+Real-Time",
            "Act+Early+%7C+Act+Informed",
            "Policy+Intelligence+%7C+Decision+Ready",
            "Momentum+Tracked+%7C+Action+Enabled",
            "Confidence+in+a+Shifting+Landscape"
        ]
    },
    "evening_report": {
        "start_hour": 18,
        "end_hour": 21,
        "emoji": "🌆",
        "badge_label": "EVENING BRIEF",
        "badge_text": "Intelligence_Delivered",
        "time_range": "6pm-9pm",
        "tagline": "Signals Captured, Insights Delivered",
        "header_desc": "Today's%20Intelligence%2C%20Tomorrow's%20Advantage",
        "bullets": "📡 Day's momentum captured • 💼 Briefs generated • 🌅 Ready for tomorrow",
        "banner_colors": "0:D6A649,50:B8935E,100:8B7355",
        "badge_color": "D6A649",
        "badge_label_color": "0B1F35",
        "time_badge_color": "B8935E",
        "divider1_colors": "0:D6A649,50:B8935E,100:8B7355",
        "divider2_colors": "0:8B7355,50:B8935E,100:D6A649",
        "footer_colors": "0:D6A649,50:B8935E,100:8B7355",
        "font_color": "FFFFFF",
        "stroke_color": "0B1F35",
        "typing_phrases": [
            "The+Day's+Legislative+Landscape",
            "Signals+Gathered+%7C+Patterns+Revealed",
            "Evening+Intelligence+Summary",
            "What+Moved+Today+%7C+What+Moves+Next",
            "The+Council's+Daily+Report",
            "From+Morning+Watch+to+Evening+Wisdom",
            "Today's+Data+%7C+Tomorrow's+Strategy",
            "Intelligence+That+Compounds"
        ]
    },
    "night_monitoring": {
        "start_hour": 21,
        "end_hour": 24,
        "emoji": "🌙",
        "badge_label": "NIGHT WATCH",
        "badge_text": "Always_Monitoring",
        "time_range": "9pm-12am",
        "tagline": "The Council Watches, Always",
        "header_desc": "Policy%20Never%20Sleeps",
        "bullets": "👁️ Monitoring continues • 🛡️ Signals flow 24/7 • 📡 The Council never rests",
        "banner_colors": "0:0B1F35,50:2C3E50,100:1A2332",
        "badge_color": "2C3E50",
        "badge_label_color": "0B1F35",
        "time_badge_color": "1A2332",
        "divider1_colors": "0:0B1F35,50:2C3E50,100:1A2332",
        "divider2_colors": "0:1A2332,50:2C3E50,100:0B1F35",
        "footer_colors": "0:2C3E50,50:4A5F7F,100:0B1F35",
        "font_color": "D6A649",
        "stroke_color": "D6A649",
        "typing_phrases": [
            "While+You+Rest%2C+We+Monitor",
            "24%2F7+Policy+Intelligence",
            "The+Council+Never+Sleeps",
            "Night+Signals+%7C+Morning+Advantage",
            "Continuous+Vigilance+%7C+Constant+Value",
            "Policy+Moves+at+All+Hours",
            "Always+On+%7C+Always+Accurate",
            "Tomorrow's+Threats+Detected+Tonight"
        ]
    },
    "late_night": {
        "start_hour": 0,
        "end_hour": 3,
        "emoji": "🌌",
        "badge_label": "DEEP WATCH",
        "badge_text": "Silent_Sentinel",
        "time_range": "12am-3am",
        "tagline": "Silent Watch, Powerful Insight",
        "header_desc": "Deep%20in%20the%20Night%2C%20Signals%20Surface",
        "bullets": "✨ Quiet hours, active agents • 🔍 Patterns in the darkness • 🏛️ Capitol silent, data loud",
        "banner_colors": "0:000000,50:0B1F35,100:191970",
        "badge_color": "191970",
        "badge_label_color": "000000",
        "time_badge_color": "0B1F35",
        "divider1_colors": "0:000000,50:0B1F35,100:191970",
        "divider2_colors": "0:191970,50:0B1F35,100:000000",
        "footer_colors": "0:2C3E50,50:4A5F7F,100:0B1F35",
        "font_color": "D6A649",
        "stroke_color": "D6A649",
        "typing_phrases": [
            "The+Quiet+Hours+Tell+Stories",
            "Late+Night+Signals+%7C+Early+Warnings",
            "When+the+Capitol+Sleeps%2C+Data+Speaks",
            "Midnight+Intelligence+Operations",
            "The+Council+Processes+the+Day",
            "Silent+Analysis+%7C+Loud+Results",
            "Deep+Night+%7C+Deep+Intelligence",
            "Tomorrow+Begins+at+Midnight"
        ]
    }
}


def get_current_theme():
    """Get the theme based on current EST time"""
    est = pytz.timezone('America/New_York')
    now = datetime.now(est)
    current_hour = now.hour
    
    for theme_name, theme_data in TIME_THEMES.items():
        start = theme_data['start_hour']
        end = theme_data['end_hour']
        
        # Handle midnight wrap-around
        if start > end or end == 24:
            if current_hour >= start or current_hour < (end % 24):
                return theme_data
        else:
            if start <= current_hour < end:
                return theme_data
    
    # Default to late_night if no match (shouldn't happen)
    return TIME_THEMES['late_night']


def build_theme_section(theme):
    """Build the TIME_THEME section of the README"""
    banner_url = f"https://capsule-render.vercel.app/api?type=waving&color={theme['banner_colors']}&height=240&section=header&text=Politheon&fontSize=90&fontColor={theme['font_color']}&stroke={theme['stroke_color']}&strokeWidth=1&fontAlignY=38&desc={theme['header_desc']}&descSize=26&descAlignY=58&descAlign=50&animation=fadeIn"
    
    time_badge_url = f"https://img.shields.io/badge/{theme['emoji']}_{theme['badge_label']}-{theme['badge_text']}-{theme['badge_color']}?style=for-the-badge&labelColor={theme['badge_label_color']}"
    
    # Replace dashes with encoded version for badge URL
    time_range_encoded = theme['time_range'].replace('-', '--')
    time_range_badge_url = f"https://img.shields.io/badge/⏰_Time-{time_range_encoded}-{theme['time_badge_color']}?style=for-the-badge&labelColor={theme['badge_label_color']}"
    
    divider_url = f"https://capsule-render.vercel.app/api?type=rect&color={theme['banner_colors']}&height=3"
    
    section = f"""![Header Banner]({banner_url})

![Time Badge]({time_badge_url})
![Current Time]({time_range_badge_url})

<img width="300" src="{divider_url}" />

### *{theme['tagline']}*

{theme['bullets']}"""
    
    return section


def build_typing_animation(theme):
    """Build the typing animation section"""
    phrases = ";".join(theme['typing_phrases'])
    return f"[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Clash+Display&size=24&duration=3000&pause=1000&color=D6A649&center=true&vCenter=true&multiline=false&width=800&height=100&lines={phrases})](https://git.io/typing-svg)"


def build_footer(theme):
    """Build the footer wave"""
    return f"![Footer](https://capsule-render.vercel.app/api?type=waving&color={theme['footer_colors']}&height=120&section=footer)"


def update_readme():
    """Update the README.md file with current theme"""
    readme_path = "README.md"
    
    # Read current README
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {readme_path} not found!")
        return False
    
    # Get current theme
    theme = get_current_theme()
    print(f"Updating README with theme: {theme['badge_label']} ({theme['time_range']})")
    
    # Build new sections
    theme_section = build_theme_section(theme)
    typing_animation = build_typing_animation(theme)
    divider1 = f"![Divider](https://capsule-render.vercel.app/api?type=rect&color={theme['divider1_colors']}&height=3)"
    divider2 = f"![Divider](https://capsule-render.vercel.app/api?type=rect&color={theme['divider2_colors']}&height=3)"
    footer = build_footer(theme)
    
    # Replace TIME_THEME section
    theme_pattern = r'<!-- TIME_THEME_START -->.*?<!-- TIME_THEME_END -->'
    content = re.sub(theme_pattern, f"<!-- TIME_THEME_START -->\n\n{theme_section}\n\n<!-- TIME_THEME_END -->", content, flags=re.DOTALL)
    
    # Replace TYPING_ANIMATION section
    typing_pattern = r'<!-- TYPING_ANIMATION_START -->.*?<!-- TYPING_ANIMATION_END -->'
    content = re.sub(typing_pattern, f"<!-- TYPING_ANIMATION_START -->\n{typing_animation}\n<!-- TYPING_ANIMATION_END -->", content, flags=re.DOTALL)
    
    # Replace DIVIDER_1 section
    divider1_pattern = r'<!-- DIVIDER_1_START -->.*?<!-- DIVIDER_1_END -->'
    content = re.sub(divider1_pattern, f"<!-- DIVIDER_1_START -->\n{divider1}\n<!-- DIVIDER_1_END -->", content, flags=re.DOTALL)
    
    # Replace DIVIDER_2 section
    divider2_pattern = r'<!-- DIVIDER_2_START -->.*?<!-- DIVIDER_2_END -->'
    content = re.sub(divider2_pattern, f"<!-- DIVIDER_2_START -->\n{divider2}\n<!-- DIVIDER_2_END -->", content, flags=re.DOTALL)
    
    # Replace FOOTER_WAVE section
    footer_pattern = r'<!-- FOOTER_WAVE_START -->.*?<!-- FOOTER_WAVE_END -->'
    content = re.sub(footer_pattern, f"<!-- FOOTER_WAVE_START -->\n{footer}\n<!-- FOOTER_WAVE_END -->", content, flags=re.DOTALL)
    
    # Write updated README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("[SUCCESS] README.md updated successfully!")
    return True


if __name__ == "__main__":
    success = update_readme()
    exit(0 if success else 1)

