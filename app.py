"""
AI Starter Kit for Small Businesses
A comprehensive AI consulting and implementation tool powered by Streamlit and OpenAI
"""

import streamlit as st
from openai import OpenAI
import json
import requests
from datetime import datetime

# ============================================================
# 🎨 YOUR BRANDING - CUSTOMIZE THIS SECTION
# ============================================================
BRAND_CONFIG = {
    # Your Information
    "consultant_name": "Rik Williams",
    "business_name": "AI Starter Kit",
    "tagline": "Your AI Consultant & Implementation Partner",
    # Contact & Links
    "email": "rikwilliams7676@gmail.com",
    "website": "https://yourwebsite.com",  # Update when ready
    # "calendar_link": "https://calendly.com/your-link",  Update when ready#
    "calendar_link": " https://calendly.com/rikwilliams7676/30min",
    # Course/Product Links (update when ready)
    "course_link": "https://udemy.com/your-course",
    "course_name": "Complete AI for Business Course",
    # Social Media (update when ready)
    "linkedin": "https://linkedin.com/in/yourprofile",
    "twitter": "",
    "youtube": "",
    # Lead Capture Settings - GOOGLE SHEETS METHOD
    "enable_lead_capture": True,
    "google_sheet_url": "https://script.google.com/macros/s/AKfycbwnQsC3BGx8KxaNc2JRH0r5INiaibS8Ydx6NECzglj7-b4W0vVviBwERDK_YSgEb7OW/exec",
    # Customization
    "show_powered_by": True,
}
# ============================================================
#
# 📋 GOOGLE SHEETS LEAD CAPTURE SETUP INSTRUCTIONS:
#
# 1. Go to: https://sheets.google.com and create a new spreadsheet
# 2. Name it "AI Starter Kit Leads"
# 3. Add headers in Row 1: timestamp | email | name | context | assessment
# 4. Click: Extensions > Apps Script
# 5. Delete any code there and paste this:
#
#    function doPost(e) {
#      var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
#      var data = JSON.parse(e.postData.contents);
#      sheet.appendRow([
#        new Date(),
#        data.email,
#        data.name,
#        data.context,
#        data.assessment
#      ]);
#      return ContentService.createTextOutput(JSON.stringify({success: true}))
#        .setMimeType(ContentService.MimeType.JSON);
#    }
#
# 6. Click: Deploy > New deployment
# 7. Select type: Web app
# 8. Set "Who has access" to: Anyone
# 9. Click Deploy and authorize when prompted
# 10. Copy the Web app URL and paste it above in "google_sheet_url"
#
# ============================================================

# Page Configuration
st.set_page_config(
    page_title=f"{BRAND_CONFIG['business_name']} - AI for Small Business",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    /* Main theme */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #e2e8f0 !important;
    }
    
    /* Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #6366f1;
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    /* Use case cards */
    .use-case-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        transition: all 0.2s ease;
    }
    
    .use-case-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .badge-easy {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
    }
    
    .badge-medium {
        background: rgba(245, 158, 11, 0.2);
        color: #fbbf24;
    }
    
    .badge-info {
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .chat-assistant {
        background: rgba(99, 102, 241, 0.15);
        border-left: 3px solid #6366f1;
    }
    
    .chat-user {
        background: rgba(30, 41, 59, 0.6);
        border-left: 3px solid #94a3b8;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 8px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95);
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Lead capture form */
    .lead-form {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border: 2px solid rgba(99, 102, 241, 0.4);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .lead-form h3 {
        margin-bottom: 0.5rem;
    }
    
    /* Footer */
    .custom-footer {
        background: rgba(15, 23, 42, 0.8);
        border-top: 1px solid rgba(99, 102, 241, 0.2);
        padding: 1.5rem;
        margin-top: 3rem;
        border-radius: 12px;
        text-align: center;
    }
    
    .footer-links a {
        color: #a5b4fc;
        text-decoration: none;
        margin: 0 0.5rem;
    }
    
    .footer-links a:hover {
        color: #c7d2fe;
    }
    
    /* CTA Button */
    .cta-button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem;
    }
    
    .cta-button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS FOR BRANDING & LEAD CAPTURE
# ============================================================


def render_lead_capture_form(context="assessment"):
    """Render email capture form using Google Sheets"""
    if not BRAND_CONFIG.get("enable_lead_capture", True):
        return

    google_sheet_url = BRAND_CONFIG.get("google_sheet_url", "")

    # Don't show if not configured
    if not google_sheet_url:
        st.markdown("---")
        st.warning(
            "💡 Lead capture not configured. Add your Google Sheet URL to BRAND_CONFIG."
        )
        return

    st.markdown("---")

    # Different messaging based on context
    if context == "assessment":
        title = "📧 Get Your Personalized AI Roadmap"
        subtitle = "Enter your email to receive your assessment results and personalized AI implementation recommendations."
    elif context == "use_case":
        title = "📧 Get Implementation Templates"
        subtitle = "Enter your email to receive all templates and checklists for this use case."
    else:
        title = "📧 Stay Updated"
        subtitle = "Get weekly AI tips and strategies for small business."

    st.markdown(
        f"""
    <div class="lead-form">
        <h3>{title}</h3>
        <p>{subtitle}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Check if already submitted in this session
    if st.session_state.get(f"lead_submitted_{context}"):
        st.success(
            f"✅ Thanks! We've saved your information. We'll be in touch at {st.session_state.get('lead_email', 'your email')}"
        )
        return

    # Form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        lead_email = st.text_input(
            "Your Email", placeholder="you@company.com", key=f"email_{context}"
        )
        lead_name = st.text_input(
            "Your Name (optional)", placeholder="Your name", key=f"name_{context}"
        )

        if st.button(
            "📩 Send My Results", use_container_width=True, key=f"submit_{context}"
        ):
            if lead_email and "@" in lead_email and "." in lead_email:
                # Build assessment summary if available
                assessment_summary = "Not completed"
                if (
                    st.session_state.get("assessment_complete")
                    and context == "assessment"
                ):
                    try:
                        results = get_assessment_results()
                        assessment_summary = f"Level: {results['level']['name']}, Score: {results['avg_score']:.1f}/4, Recommendations: {', '.join(results['recommendations'])}"
                    except:
                        assessment_summary = "Completed"

                # Show loading
                with st.spinner("📤 Saving your information..."):
                    try:
                        form_data = {
                            "email": lead_email,
                            "name": lead_name or "Not provided",
                            "context": context,
                            "assessment": assessment_summary,
                        }

                        # Send to Google Sheets
                        response = requests.post(
                            google_sheet_url,
                            json=form_data,
                            headers={"Content-Type": "application/json"},
                            timeout=10,
                        )

                        if response.status_code == 200:
                            st.session_state[f"lead_submitted_{context}"] = True
                            st.session_state["lead_email"] = lead_email
                            st.balloons()
                            st.success(
                                f"✅ Thanks {lead_name or ''}! We've saved your information and will be in touch at {lead_email}"
                            )
                        else:
                            st.error(
                                f"❌ Something went wrong (Status: {response.status_code})"
                            )
                            st.info(
                                f"📧 Please email us directly: **{BRAND_CONFIG.get('email', '')}**"
                            )

                    except requests.exceptions.Timeout:
                        st.error("⏱️ Request timed out. Please try again.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.info(
                            f"📧 Please email us directly: **{BRAND_CONFIG.get('email', '')}**"
                        )
            else:
                st.error("⚠️ Please enter a valid email address")


def render_footer():
    """Render branded footer with CTA"""
    st.markdown("---")

    # Build footer content
    consultant_name = BRAND_CONFIG.get("consultant_name", "Your Name")
    business_name = BRAND_CONFIG.get("business_name", "AI Starter Kit")
    calendar_link = BRAND_CONFIG.get("calendar_link", "")
    course_link = BRAND_CONFIG.get("course_link", "")
    course_name = BRAND_CONFIG.get("course_name", "")
    website = BRAND_CONFIG.get("website", "")
    linkedin = BRAND_CONFIG.get("linkedin", "")
    email = BRAND_CONFIG.get("email", "")

    # Check if any CTA links are configured (not placeholder values)
    has_calendar = calendar_link and calendar_link != "https://calendly.com/your-link"
    has_course = course_link and course_link != "https://udemy.com/your-course"
    has_website = website and website != "https://yourwebsite.com"
    has_linkedin = linkedin and linkedin != "https://linkedin.com/in/yourprofile"
    has_email = email and email != "your-email@example.com"
    has_name = consultant_name and consultant_name != "Your Name"

    # Only show CTA section if at least one link is configured
    if has_calendar or has_course or has_website:
        st.markdown("### 🚀 Ready to Implement AI in Your Business?")

        col1, col2, col3 = st.columns(3)

        with col1:
            if has_calendar:
                st.link_button(
                    "📞 Book a Free Consultation",
                    calendar_link,
                    use_container_width=True,
                )

        with col2:
            if has_course:
                st.link_button(
                    "📚 Take My Course", course_link, use_container_width=True
                )

        with col3:
            if has_website:
                st.link_button("🌐 Visit Website", website, use_container_width=True)

        st.markdown("---")

    # Footer info - build links separately
    footer_links = []
    if has_website:
        footer_links.append(f"[🌐 Website]({website})")
    if has_linkedin:
        footer_links.append(f"[💼 LinkedIn]({linkedin})")

    # Display footer
    if has_name:
        st.markdown(f"**Built by {consultant_name}**")

    if footer_links:
        st.markdown(" • ".join(footer_links))

    # Call to action with email
    if has_email:
        st.markdown("---")
        st.markdown("### 💬 Need Help Implementing AI?")
        st.markdown(
            "Get in touch for personalized guidance on bringing AI to your business."
        )
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"📧 **Email:** `{email}`")

    st.caption(f"{business_name} © {datetime.now().year} • Powered by AI")


def render_sidebar_cta():
    """Add CTA to sidebar"""
    calendar_link = BRAND_CONFIG.get("calendar_link", "")
    course_link = BRAND_CONFIG.get("course_link", "")
    consultant_name = BRAND_CONFIG.get("consultant_name", "")

    has_calendar = calendar_link and calendar_link != "https://calendly.com/your-link"
    has_course = course_link and course_link != "https://udemy.com/your-course"
    has_name = consultant_name and consultant_name != "Your Name"

    # Only show if at least one link is configured
    if has_calendar or has_course or has_name:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 💼 Need Help?")

        if has_calendar:
            st.sidebar.markdown(f"[📞 Book a Free Call]({calendar_link})")

        if has_course:
            st.sidebar.markdown(f"[📚 Take My Course]({course_link})")

        if has_name:
            st.sidebar.caption(f"Built by {consultant_name}")


# ============================================================

# Initialize session state
if "assessment_answers" not in st.session_state:
    st.session_state.assessment_answers = {}
if "assessment_complete" not in st.session_state:
    st.session_state.assessment_complete = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "generated_content" not in st.session_state:
    st.session_state.generated_content = ""
if "generated_prompt" not in st.session_state:
    st.session_state.generated_prompt = ""
if "checklist_state" not in st.session_state:
    st.session_state.checklist_state = {}
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"
if "pending_message" not in st.session_state:
    st.session_state.pending_message = None
if "selected_use_case" not in st.session_state:
    st.session_state.selected_use_case = None


# Navigation helper function
def navigate_to(page_name):
    st.session_state.current_page = page_name


# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    api_key = st.secrets.get("OPENAI_API_KEY", None)
    if api_key:
        return OpenAI(api_key=api_key)
    return None


# Data: Assessment Questions
ASSESSMENT_QUESTIONS = [
    {
        "id": "business_type",
        "category": "Business Profile",
        "question": "What type of business do you run?",
        "options": {
            "retail": "Retail / E-commerce",
            "services": "Professional Services",
            "restaurant": "Restaurant / Hospitality",
            "healthcare": "Healthcare / Wellness",
            "tech": "Tech / SaaS",
            "other": "Other",
        },
    },
    {
        "id": "tech_comfort",
        "category": "Technology Readiness",
        "question": "How comfortable is your team with adopting new technology?",
        "options": {
            1: "We struggle with new tools",
            2: "We adapt slowly but eventually",
            3: "We embrace new technology",
            4: "We actively seek innovations",
        },
    },
    {
        "id": "data_quality",
        "category": "Data Infrastructure",
        "question": "How would you describe your current data situation?",
        "options": {
            1: "Scattered across spreadsheets",
            2: "Basic CRM/database in place",
            3: "Well-organized digital records",
            4: "Integrated systems with analytics",
        },
    },
    {
        "id": "budget",
        "category": "Investment Capacity",
        "question": "What's your monthly budget for AI tools?",
        "options": {
            1: "Under $100/month",
            2: "$100-500/month",
            3: "$500-2000/month",
            4: "$2000+/month",
        },
    },
    {
        "id": "pain_points",
        "category": "Business Needs",
        "question": "What's your biggest operational challenge?",
        "options": {
            "customer_service": "Customer Support",
            "content": "Content Creation",
            "admin": "Administrative Tasks",
            "sales": "Sales & Lead Generation",
        },
    },
    {
        "id": "team_size",
        "category": "Organization",
        "question": "How many employees do you have?",
        "options": {
            1: "Solo or 1-2 people",
            2: "3-10 employees",
            3: "11-50 employees",
            4: "50+ employees",
        },
    },
]

# Data: AI Use Cases with FULL Implementation Guides
USE_CASES = [
    {
        "id": "chatbot",
        "title": "Customer Service Chatbot",
        "icon": "💬",
        "category": "Customer Experience",
        "difficulty": "Easy",
        "time": "1-2 days",
        "cost": "$0-50/mo",
        "roi": "Save 20+ hrs/week",
        "description": "Deploy an AI chatbot to handle FAQs, appointment booking, and basic customer inquiries 24/7.",
        "best_for": ["Retail", "Services", "Healthcare", "Hospitality"],
        "tools": [
            {
                "name": "Tidio",
                "cost": "Free-$29/mo",
                "url": "https://tidio.com",
                "rec": True,
            },
            {
                "name": "Intercom Fin",
                "cost": "$0.99/resolution",
                "url": "https://intercom.com",
                "rec": False,
            },
            {
                "name": "ChatBot.com",
                "cost": "$52/mo",
                "url": "https://chatbot.com",
                "rec": False,
            },
        ],
        "steps": [
            {
                "title": "Gather Your FAQs",
                "time": "2 hours",
                "desc": "Compile your top 50 customer questions",
                "how_to": """**What to do:**
1. Check your email inbox for common customer questions
2. Ask your team: "What do customers always ask?"
3. Review social media comments and messages
4. Check Google reviews for repeated themes

**Create a spreadsheet with columns:**
- Question
- Best Answer
- Category (Shipping, Returns, Hours, Products, etc.)

**Example FAQs to include:**
- What are your hours?
- Do you offer refunds?
- How long does shipping take?
- Do you have [product] in stock?
- How do I book an appointment?""",
                "template": """FAQ COLLECTION TEMPLATE
=======================
Business: [Your Business Name]
Date: [Today's Date]

CATEGORY: Store Information
Q: What are your hours?
A: We're open Monday-Friday 9am-6pm, Saturday 10am-4pm, closed Sunday.

Q: Where are you located?
A: [Your address + parking info + landmarks]

CATEGORY: Products/Services
Q: [Common product question]
A: [Your answer]

CATEGORY: Shipping/Delivery
Q: How long does shipping take?
A: [Your shipping times]

CATEGORY: Returns/Refunds
Q: What's your return policy?
A: [Your policy]

[Add 40+ more Q&As organized by category]""",
            },
            {
                "title": "Choose & Sign Up for Platform",
                "time": "30 mins",
                "desc": "Sign up for Tidio (recommended for beginners)",
                "how_to": """**Recommended: Start with Tidio (Free tier)**

**Step-by-step signup:**
1. Go to https://tidio.com
2. Click "Get Started Free"
3. Enter your email and create password
4. Enter your website URL
5. Choose your business type
6. Skip the templates for now (we'll customize)

**Why Tidio?**
- Free tier includes AI chatbot
- No coding required
- Works on any website
- Easy to customize
- Good analytics

**Alternative options:**
- Already use Shopify? → Try Shopify Inbox (free)
- Have budget? → Intercom Fin is more powerful
- WordPress? → Tidio has a plugin""",
                "template": None,
            },
            {
                "title": "Configure Your Bot",
                "time": "2 hours",
                "desc": "Add your FAQs and customize responses",
                "how_to": """**In Tidio, follow these steps:**

**1. Set up Welcome Message (5 mins)**
- Go to Chatbots → Create new
- Choose "Welcome new visitors"
- Customize: "Hi! 👋 Welcome to [Business Name]. How can I help you today?"
- Add quick reply buttons: "Hours & Location", "Products", "Contact Us"

**2. Add FAQ Responses (1 hour)**
- Go to Chatbots → Create new → "Answer questions"
- For each FAQ:
  - Add trigger phrases (different ways customers ask)
  - Add your answer
  - Example triggers for hours: "hours", "open", "when do you open", "closing time"

**3. Set Up Human Handoff (15 mins)**
- Create a response for complex questions:
- "I'd be happy to connect you with our team! Please leave your email and we'll respond within 24 hours."
- Enable email notifications for yourself

**4. Customize Appearance (15 mins)**
- Go to Settings → Appearance
- Choose your brand colors
- Upload your logo
- Set chat position (bottom right is standard)""",
                "template": """CHATBOT FLOW TEMPLATE
=====================

WELCOME MESSAGE:
"Hi there! 👋 Welcome to [Business Name]. I'm here to help!

What can I assist you with today?"

[Button: Hours & Location]
[Button: Products/Services]  
[Button: Speak to Human]

---
HOURS RESPONSE:
Triggers: hours, open, when open, what time, schedule, closing

Response: "We're open:
📅 Monday-Friday: 9am - 6pm
📅 Saturday: 10am - 4pm  
📅 Sunday: Closed

📍 [Your Address]

Anything else I can help with?"

---
HUMAN HANDOFF:
Triggers: speak to human, real person, agent, help, complicated

Response: "I'd be happy to connect you with our team! 

Please share your email and a brief message, and we'll get back to you within [X hours].

[Email input field]
[Message input field]"

---
FALLBACK (when bot doesn't understand):
"I'm not sure I understood that. Would you like to:

[Button: See FAQs]
[Button: Contact our team]"
""",
            },
            {
                "title": "Install on Your Website",
                "time": "15 mins",
                "desc": "Add the chat widget to your site",
                "how_to": """**The installation depends on your website platform:**

**Shopify:**
1. In Tidio, go to Settings → Installation → Shopify
2. Click "Add to Shopify"
3. Authorize the app
4. Done! Widget appears automatically

**WordPress:**
1. In WordPress admin, go to Plugins → Add New
2. Search "Tidio"
3. Install and activate
4. Click "Connect" and log into your Tidio account

**Wix:**
1. In Tidio, go to Settings → Installation → Wix
2. Click "Add to Wix"
3. Follow the prompts

**Any other website (HTML):**
1. In Tidio, go to Settings → Installation → JavaScript
2. Copy the code snippet
3. Paste it before </body> tag on every page
4. Or add to your site's footer template

**Code looks like this:**
```html
<script src="//code.tidio.co/YOUR_UNIQUE_CODE.js" async></script>
```

**After installing:**
1. Open your website in a new browser tab
2. You should see the chat widget in the corner
3. Click it and test a conversation!""",
                "template": None,
            },
            {
                "title": "Test & Refine",
                "time": "1 hour",
                "desc": "Test conversations and improve responses",
                "how_to": """**Testing Checklist:**

✅ Test as a customer (use incognito browser):
- Does the welcome message appear?
- Click each quick reply button - do they work?
- Ask a FAQ in different ways - does it answer correctly?
- Ask something random - does it offer human handoff?

✅ Test on mobile:
- Does the widget look good on phone?
- Is text readable?
- Can you easily type and send messages?

✅ Test human handoff:
- Trigger the handoff
- Did you receive the notification email?
- Can you respond to the customer?

**Common fixes:**
- Bot not understanding → Add more trigger phrases
- Wrong answers → Check for conflicting triggers
- Widget too intrusive → Adjust timing (show after 10 seconds)

**After going live:**
- Check analytics weekly
- Look for unanswered questions
- Add new FAQs based on real conversations
- Update answers seasonally (hours, promotions)""",
                "template": """WEEKLY CHATBOT REVIEW CHECKLIST
================================
Date: ___________

METRICS:
□ Total conversations this week: _____
□ Bot handled automatically: _____% 
□ Handed off to human: _____%
□ Most asked question: _____________

IMPROVEMENTS NEEDED:
□ Questions bot couldn't answer:
  1. _________________ → Add FAQ
  2. _________________ → Add FAQ
  
□ Update needed for:
  - [ ] Hours/seasonal changes
  - [ ] New products/services
  - [ ] Promotions/sales
  - [ ] Policies

NEXT ACTIONS:
1. _______________________
2. _______________________""",
            },
        ],
    },
    {
        "id": "content",
        "title": "AI Content Assistant",
        "icon": "✍️",
        "category": "Marketing",
        "difficulty": "Easy",
        "time": "1 day",
        "cost": "$20-100/mo",
        "roi": "Save 15+ hrs/week",
        "description": "Use AI to draft social media posts, email newsletters, product descriptions, and marketing copy.",
        "best_for": [
            "E-commerce",
            "Professional Services",
            "Restaurants",
            "Real Estate",
        ],
        "tools": [
            {
                "name": "ChatGPT Plus",
                "cost": "$20/mo",
                "url": "https://chat.openai.com",
                "rec": True,
            },
            {
                "name": "Claude Pro",
                "cost": "$20/mo",
                "url": "https://claude.ai",
                "rec": False,
            },
            {
                "name": "Jasper",
                "cost": "$49/mo",
                "url": "https://jasper.ai",
                "rec": False,
            },
        ],
        "steps": [
            {
                "title": "Define Your Brand Voice",
                "time": "1 hour",
                "desc": "Document your tone, style, and key messages",
                "how_to": """**Create a Brand Voice Document:**

Answer these questions:
1. If your brand was a person, how would they speak?
2. What 3-5 adjectives describe your tone? (e.g., friendly, professional, witty)
3. What words do you ALWAYS use? (e.g., "clients" vs "customers")
4. What words do you NEVER use? (e.g., "cheap" vs "affordable")
5. What's your unique value proposition in one sentence?

**Tone Examples:**
- Professional & Trustworthy: Law firm, financial advisor
- Friendly & Casual: Coffee shop, pet store
- Luxurious & Exclusive: High-end boutique, spa
- Fun & Playful: Kids' store, entertainment

**This becomes your "AI Style Guide" that you'll paste into every prompt.**""",
                "template": """BRAND VOICE GUIDE
=================
Business: [Your Business Name]
Industry: [Your Industry]
Target Audience: [Who you serve]

TONE ADJECTIVES:
1. [e.g., Friendly]
2. [e.g., Professional]
3. [e.g., Helpful]

VOICE PERSONALITY:
"We sound like a [knowledgeable friend/trusted expert/fun neighbor] who [helps people with X]."

ALWAYS USE:
- [Word/phrase]: e.g., "clients" not "customers"
- [Word/phrase]: e.g., "investment" not "cost"
- [Word/phrase]: e.g., "your" and "you" (speak directly)

NEVER USE:
- [Word/phrase]: e.g., "cheap"
- [Word/phrase]: e.g., "just"
- [Word/phrase]: e.g., industry jargon

KEY MESSAGES (always reinforce):
1. [Your main differentiator]
2. [Your core value]
3. [Your call-to-action]

EMOJI USAGE: [None / Minimal / Moderate / Frequent]

SAMPLE SENTENCE IN OUR VOICE:
"[Write one example sentence that perfectly captures your brand voice]"
""",
            },
            {
                "title": "Create Prompt Templates",
                "time": "2 hours",
                "desc": "Build reusable prompts for each content type",
                "how_to": """**Create a prompt template for each content type you need:**

The formula: Context + Task + Format + Constraints

**For each template:**
1. Start with your brand voice (paste your guide)
2. Specify exactly what you want
3. Define the format (length, structure)
4. Give an example if possible

**Save these in a document so you can copy-paste and fill in the blanks.**

**Pro tips:**
- Be specific about length: "Write exactly 3 sentences" or "150-200 words"
- Specify the platform: "for Instagram" vs "for LinkedIn"
- Include your call-to-action: "End with CTA to visit our website"
- Ask for multiple options: "Give me 3 variations\"""",
                "template": """CONTENT PROMPT TEMPLATES
========================

📱 SOCIAL MEDIA POST
--------------------
Act as a social media manager for [Business Name], a [industry] business.

Brand voice: [Paste your brand voice summary]

Write a [platform] post about [topic/promotion/announcement].

Requirements:
- Tone: [friendly/professional/etc.]
- Length: [character count or sentence count]
- Include: [hashtags/emoji/call-to-action]
- Goal: [engagement/sales/awareness]

Give me 3 variations.


📧 EMAIL NEWSLETTER
-------------------
Write an email for [Business Name]'s newsletter subscribers.

Brand voice: [Paste your brand voice summary]

Topic: [This week's topic/promotion]
Goal: [Inform/sell/engage]

Include:
- Subject line (give 3 options)
- Preview text
- Opening hook
- Main content (150-200 words)
- Call-to-action button text
- P.S. line

Audience: [Describe your subscribers]


🛍️ PRODUCT DESCRIPTION
----------------------
Write a product description for [Product Name].

Brand voice: [Paste your brand voice summary]

Product details:
- What it is: [Description]
- Key features: [Feature 1, Feature 2, Feature 3]
- Price: [Price]
- Target customer: [Who buys this]

Format:
- Headline (attention-grabbing)
- Short description (2-3 sentences)
- Bullet points (5 key benefits)
- Closing with CTA


📝 BLOG POST OUTLINE
--------------------
Create a blog post outline for [Business Name].

Topic: [Blog topic]
Target keyword: [SEO keyword]
Target audience: [Who will read this]

Include:
- SEO-optimized title (give 3 options)
- Meta description (155 characters)
- Introduction hook
- 5-7 main sections with subpoints
- Conclusion with CTA
- Suggested word count per section
""",
            },
            {
                "title": "Set Up Your Workflow",
                "time": "1 hour",
                "desc": "Establish a content review and approval process",
                "how_to": """**Create a simple content workflow:**

**STEP 1: Plan (Weekly - 30 mins)**
- Decide what content you need this week
- Check your content calendar
- Note any promotions, holidays, events

**STEP 2: Generate (15 mins per piece)**
- Open ChatGPT/Claude
- Paste your brand voice guide
- Use your prompt template
- Request 3 variations

**STEP 3: Review & Edit (10 mins per piece)**
- Read AI output critically
- Fact-check any claims
- Adjust to sound more "you"
- Check for awkward phrasing

**STEP 4: Approve & Schedule**
- Final proofread
- Add to scheduling tool (Buffer, Later, Hootsuite)
- Or post directly

**Quality Checklist:**
✅ Sounds like our brand voice?
✅ Accurate information?
✅ No AI-sounding phrases? (e.g., "In conclusion", "It's important to note")
✅ Clear call-to-action?
✅ Appropriate for platform?""",
                "template": """CONTENT REVIEW CHECKLIST
========================

Content Type: _______________
Platform: _______________
Date to Post: _______________

PRE-PUBLISH CHECKS:

Voice & Tone:
□ Matches our brand voice guide
□ Sounds natural, not robotic
□ Appropriate for target audience

Accuracy:
□ All facts verified
□ Prices/dates correct
□ Links tested and working

Platform Requirements:
□ Character count appropriate
□ Image specs correct
□ Hashtags relevant (not too many)

Quality:
□ Proofread for typos
□ Removed AI-ish phrases
□ Clear call-to-action included

APPROVED BY: _____________
DATE: _____________
""",
            },
            {
                "title": "Train Your Team",
                "time": "2 hours",
                "desc": "Show your team how to use AI content tools effectively",
                "how_to": """**Team Training Session Agenda:**

**Part 1: Introduction (15 mins)**
- Why we're using AI for content
- What AI is good at (first drafts, ideas, variations)
- What AI is NOT good at (facts, your unique voice, strategy)

**Part 2: Live Demo (30 mins)**
- Show how to access ChatGPT/Claude
- Demo using a prompt template
- Show how to refine and iterate
- Show what "bad AI content" looks like vs "good"

**Part 3: Hands-On Practice (45 mins)**
- Give everyone the prompt templates
- Each person creates one piece of content
- Review together and give feedback

**Part 4: Q&A and Guidelines (30 mins)**
- Answer questions
- Review do's and don'ts
- Share access to brand voice guide and templates

**Key Rules to Establish:**
1. Always start with brand voice guide
2. Never publish AI content without human review
3. Always fact-check statistics and claims
4. Edit to add your personal touch
5. Don't mention we use AI (it's a tool, not the author)""",
                "template": """AI CONTENT GUIDELINES FOR TEAM
==============================

✅ DO:
- Use AI for first drafts and brainstorming
- Always paste brand voice guide first
- Request multiple variations
- Edit heavily - make it yours
- Use specific, detailed prompts

❌ DON'T:
- Publish without human review
- Trust statistics or facts from AI (verify!)
- Use generic, vague prompts
- Leave in AI-sounding phrases
- Mention "AI-generated" to customers

AI-SOUNDING PHRASES TO REMOVE:
- "In conclusion..."
- "It's worth noting that..."
- "In today's fast-paced world..."
- "Look no further!"
- "Are you tired of...?"
- "[Topic] is a game-changer"

PROMPT TEMPLATES LOCATION:
[Link to your shared document]

BRAND VOICE GUIDE LOCATION:
[Link to your shared document]

QUESTIONS? Contact: [Name/Email]
""",
            },
            {
                "title": "Create Content Calendar",
                "time": "1 hour",
                "desc": "Plan and batch your content creation",
                "how_to": """**Set up a simple content calendar:**

**Option 1: Google Sheets (Free)**
Create columns:
- Date
- Platform  
- Content Type
- Topic/Theme
- Status (Idea/Drafted/Reviewed/Scheduled/Posted)
- Link to content

**Option 2: Notion (Free)**
- More visual
- Can add images
- Better for teams

**Option 3: Trello (Free)**
- Card-based
- Good for visual workflow

**Content Batching Strategy:**
1. Pick one day per week for content creation
2. Generate all content for the upcoming week
3. Schedule everything in advance
4. Spend other days just on engagement

**Monthly Content Mix:**
- 40% Value/Educational
- 30% Promotional
- 20% Engagement/Fun
- 10% Behind-the-scenes""",
                "template": """MONTHLY CONTENT CALENDAR
========================
Month: _____________
Business: _____________

CONTENT MIX TARGETS:
- Educational posts: 8-10
- Promotional posts: 6-8
- Engagement posts: 4-5
- Behind-scenes: 2-3

WEEKLY THEME IDEAS:
Week 1: [Theme/Focus]
Week 2: [Theme/Focus]  
Week 3: [Theme/Focus]
Week 4: [Theme/Focus]

KEY DATES THIS MONTH:
- [Holiday/Event]: Post idea
- [Sale/Promotion]: Post idea
- [Industry event]: Post idea

PLATFORM POSTING SCHEDULE:
Instagram: [X posts/week]
Facebook: [X posts/week]
LinkedIn: [X posts/week]
Email: [X emails/month]

CONTENT CREATION DAY: Every [Day]
BATCH SIZE: [X] posts per session
""",
            },
        ],
    },
    {
        "id": "email",
        "title": "Smart Email Marketing",
        "icon": "📧",
        "category": "Marketing",
        "difficulty": "Medium",
        "time": "1 week",
        "cost": "$50-200/mo",
        "roi": "30% better open rates",
        "description": "AI-powered email personalization, subject line optimization, and automated campaigns.",
        "best_for": ["E-commerce", "SaaS", "Professional Services", "Retail"],
        "tools": [
            {
                "name": "Mailchimp",
                "cost": "$13-350/mo",
                "url": "https://mailchimp.com",
                "rec": True,
            },
            {
                "name": "Klaviyo",
                "cost": "$45-700/mo",
                "url": "https://klaviyo.com",
                "rec": False,
            },
            {
                "name": "ActiveCampaign",
                "cost": "$29-149/mo",
                "url": "https://activecampaign.com",
                "rec": False,
            },
        ],
        "steps": [
            {
                "title": "Audit Current Email Performance",
                "time": "2 hours",
                "desc": "Review your existing campaigns and metrics",
                "how_to": """**Pull these metrics from your email platform:**

1. **Overall List Health:**
   - Total subscribers
   - Growth rate (new subscribers/month)
   - Unsubscribe rate
   - List age

2. **Campaign Performance (last 3 months):**
   - Average open rate (industry avg: 15-25%)
   - Average click rate (industry avg: 2-5%)
   - Best performing email (what made it work?)
   - Worst performing email (what went wrong?)

3. **Revenue (if e-commerce):**
   - Revenue from email
   - Revenue per email sent
   - Top converting emails

**Questions to answer:**
- What subject lines worked best?
- What time/day gets best opens?
- Which CTAs got most clicks?
- What content do subscribers engage with?""",
                "template": """EMAIL AUDIT TEMPLATE
====================
Date: _____________
Platform: _____________

LIST HEALTH:
- Total subscribers: _______
- Monthly growth: +_______ / -_______
- Unsubscribe rate: _______%
- Inactive (no opens in 90 days): _______%

LAST 3 MONTHS PERFORMANCE:
                    Ours    Industry Avg
Open Rate:         ____%    15-25%
Click Rate:        ____%    2-5%
Unsubscribe Rate:  ____%    <0.5%

TOP 3 PERFORMING EMAILS:
1. Subject: _____________
   Open: ____% | Click: ____%
   Why it worked: _____________

2. Subject: _____________
   Open: ____% | Click: ____%
   Why it worked: _____________

3. Subject: _____________
   Open: ____% | Click: ____%
   Why it worked: _____________

AREAS TO IMPROVE:
□ Subject lines
□ Send timing
□ Content relevance
□ List segmentation
□ Call-to-action clarity
""",
            },
            {
                "title": "Segment Your Audience",
                "time": "3 hours",
                "desc": "Create customer segments for targeted messaging",
                "how_to": """**Why segment?** Targeted emails get 14% higher open rates and 100% more clicks than generic blasts.

**Essential Segments to Create:**

**1. By Engagement:**
- Active (opened email in last 30 days)
- Lapsed (no opens in 30-90 days)  
- Inactive (no opens in 90+ days)

**2. By Customer Status:**
- New subscribers (joined in last 30 days)
- Customers (made a purchase)
- VIP customers (multiple purchases or high value)
- Non-purchasers (subscribed but never bought)

**3. By Interest/Behavior:**
- Product category interest (clicked on specific products)
- Content preference (what topics they engage with)

**How to create in Mailchimp:**
1. Go to Audience → Segments
2. Click "Create Segment"
3. Set conditions (e.g., "Campaign activity → opened → any campaign in last 30 days")
4. Save segment

**Start with these 4 basic segments:**
1. New subscribers (welcome series)
2. Active customers (promotional content)
3. Lapsed (re-engagement campaign)
4. VIPs (exclusive offers)""",
                "template": """SEGMENT PLANNING TEMPLATE
=========================

SEGMENT 1: New Subscribers
Criteria: Subscribed within last 30 days
Size: _______ subscribers
Content strategy: Welcome series, introduce brand
Email frequency: 3-4 emails over 2 weeks

SEGMENT 2: Active Engaged
Criteria: Opened email in last 30 days
Size: _______ subscribers  
Content strategy: Regular promotions, new content
Email frequency: 1-2x per week

SEGMENT 3: Customers
Criteria: Made at least 1 purchase
Size: _______ subscribers
Content strategy: Product updates, loyalty rewards, upsells
Email frequency: 1-2x per week

SEGMENT 4: VIP Customers
Criteria: [3+ purchases OR $500+ spent]
Size: _______ subscribers
Content strategy: Exclusive early access, special discounts
Email frequency: 1x per week + special occasions

SEGMENT 5: At-Risk (Lapsed)
Criteria: No opens in 60-90 days
Size: _______ subscribers
Content strategy: Re-engagement campaign, "We miss you"
Email frequency: 3 emails over 2 weeks, then remove if no response
""",
            },
            {
                "title": "Set Up Email Automations",
                "time": "4 hours",
                "desc": "Build automated email flows that run 24/7",
                "how_to": """**Must-Have Automation Flows:**

**1. Welcome Series (3-5 emails over 2 weeks)**
- Email 1 (Immediately): Welcome + what to expect
- Email 2 (Day 2): Your story/mission + best content
- Email 3 (Day 4): Product/service highlight
- Email 4 (Day 7): Social proof/testimonials
- Email 5 (Day 14): Special offer for new subscribers

**2. Abandoned Cart (E-commerce)**
- Email 1 (1 hour after): "You left something behind"
- Email 2 (24 hours): Add social proof
- Email 3 (72 hours): Offer small discount

**3. Post-Purchase**
- Email 1 (Immediately): Thank you + order confirmation
- Email 2 (3 days): How to use/care instructions
- Email 3 (14 days): Request review
- Email 4 (30 days): Related products

**4. Re-engagement (for lapsed subscribers)**
- Email 1: "We miss you" + what's new
- Email 2: Special "come back" offer
- Email 3: Last chance before removal

**In Mailchimp:**
1. Go to Automations → Create
2. Choose a pre-built journey or start from scratch
3. Set triggers (e.g., "Subscribes to list")
4. Add emails with delays between them
5. Activate""",
                "template": """WELCOME SERIES TEMPLATE
=======================

EMAIL 1: Welcome (Send immediately)
Subject: Welcome to [Business]! Here's what's next...
Content:
- Thank them for subscribing
- Set expectations (what emails they'll get)
- Share your best piece of content or offer
- CTA: Follow on social / Browse products

EMAIL 2: Our Story (Day 2)
Subject: The story behind [Business Name]
Content:
- Your origin story
- Your mission/values
- What makes you different
- CTA: Learn more about us

EMAIL 3: Best Sellers/Popular (Day 4)
Subject: Our customers' favorites 
Content:
- Showcase top 3 products/services
- Include customer reviews
- CTA: Shop/Book now

EMAIL 4: Social Proof (Day 7)
Subject: See why [X]+ customers love us
Content:
- Customer testimonials
- Press mentions
- Results/stats
- CTA: Join them

EMAIL 5: Special Offer (Day 14)
Subject: A special thank you gift 🎁
Content:
- Exclusive new subscriber offer
- Create urgency (expires in X days)
- CTA: Claim your offer
""",
            },
            {
                "title": "Enable AI Features",
                "time": "1 hour",
                "desc": "Turn on AI-powered optimization tools",
                "how_to": """**AI Features in Mailchimp:**

**1. Subject Line Helper**
- When writing email, click "Optimize" next to subject line
- AI suggests improvements based on your content
- Shows predicted open rate

**2. Send Time Optimization**
- In campaign settings, enable "Send Time Optimization"
- Mailchimp sends to each subscriber when they're most likely to open
- Based on their past behavior

**3. Content Optimizer**
- Analyzes your email content
- Suggests improvements for readability
- Checks against best practices

**4. Predictive Segments**
- Audience → Predicted Demographics
- See predicted age, gender, location of subscribers
- Create segments based on predictions

**5. Product Recommendations (E-commerce)**
- Add dynamic product blocks
- Shows each subscriber products they're likely to buy
- Based on their browsing/purchase history

**How to enable:**
1. Go to your email campaign
2. Look for "AI" or "Optimize" buttons throughout the editor
3. Turn on Send Time Optimization in delivery settings
4. Enable product recommendations if you have e-commerce connected""",
                "template": None,
            },
            {
                "title": "A/B Test & Optimize",
                "time": "Ongoing",
                "desc": "Continuously improve through testing",
                "how_to": """**What to A/B Test:**

**Start with Subject Lines (Biggest Impact)**
- Test: Short vs. long
- Test: With emoji vs. without
- Test: Question vs. statement
- Test: Personalization (name) vs. without

**Then Test:**
- Send times (morning vs. afternoon)
- From name (Business name vs. Person name)
- CTA button text
- Email length
- Number of images

**How to A/B Test in Mailchimp:**
1. Create campaign → Choose "A/B Test"
2. Select what to test (subject, from name, content, send time)
3. Set audience split (recommend 20% test, 80% winner)
4. Set how winner is determined (open rate or click rate)
5. Set test duration (4-24 hours)
6. Send!

**Track Results:**
- Wait for statistical significance (need enough data)
- Document what works for YOUR audience
- Apply learnings to future emails
- Test one thing at a time

**Monthly Testing Calendar:**
- Week 1: Test subject line style
- Week 2: Apply winner, test send time
- Week 3: Apply winner, test CTA
- Week 4: Apply winner, test content format""",
                "template": """A/B TEST TRACKING LOG
=====================

TEST #: _____
Date: _____________

WHAT WE TESTED: Subject Line
Version A: _________________________
Version B: _________________________

RESULTS:
              Version A    Version B
Sent to:      _______      _______
Open Rate:    ______%      ______%
Click Rate:   ______%      ______%

WINNER: Version ___

WHY IT WORKED:
_________________________________

APPLY TO FUTURE EMAILS:
□ Yes, will use this approach
□ Need more testing

---
LEARNINGS LOG:
- Subject lines with [X] perform better
- Our audience prefers [X] send time
- Emails with [X] get more clicks
- [Add your learnings]
""",
            },
        ],
    },
    {
        "id": "sales",
        "title": "AI Sales Assistant",
        "icon": "📈",
        "category": "Sales",
        "difficulty": "Medium",
        "time": "2 weeks",
        "cost": "$100-500/mo",
        "roi": "40% more leads",
        "description": "Automate lead scoring, follow-up sequences, and prospect research with AI tools.",
        "best_for": ["B2B Services", "SaaS", "Real Estate", "Financial Services"],
        "tools": [
            {
                "name": "HubSpot CRM",
                "cost": "Free-$800/mo",
                "url": "https://hubspot.com",
                "rec": True,
            },
            {
                "name": "Apollo.io",
                "cost": "$49-99/mo",
                "url": "https://apollo.io",
                "rec": False,
            },
            {
                "name": "Clay",
                "cost": "$149-800/mo",
                "url": "https://clay.com",
                "rec": False,
            },
        ],
        "steps": [
            {
                "title": "Define Your Ideal Customer Profile",
                "time": "3 hours",
                "desc": "Create detailed buyer personas",
                "how_to": """**An ICP (Ideal Customer Profile) answers: "Who are your BEST customers?"**

**Look at your existing customers:**
1. Who are your top 10 customers by revenue?
2. Who are easiest to work with?
3. Who refers others to you?
4. What do they have in common?

**Define these attributes:**

**Company Profile (B2B):**
- Industry
- Company size (employees)
- Revenue range
- Location
- Tech they use

**Person Profile:**
- Job title/role
- Department
- Seniority level
- Goals/KPIs they care about
- Challenges they face

**Buying Behavior:**
- How they find you (channel)
- Length of sales cycle
- Decision-making process
- Budget authority""",
                "template": """IDEAL CUSTOMER PROFILE (ICP)
============================

COMPANY PROFILE:
Industry: _____________
Company Size: ______ - ______ employees
Revenue: $______ - $______
Location: _____________
Other criteria: _____________

DECISION MAKER:
Title(s): _____________
Department: _____________
Reports to: _____________
Years in role: _____________

THEIR GOALS:
1. _____________
2. _____________
3. _____________

THEIR CHALLENGES:
1. _____________
2. _____________
3. _____________

HOW WE HELP:
_____________

BUYING TRIGGERS:
(Events that make them ready to buy)
- _____________
- _____________

RED FLAGS (NOT a good fit):
- _____________
- _____________

SAMPLE TARGET COMPANIES:
1. _____________
2. _____________
3. _____________
""",
            },
            {
                "title": "Set Up Your CRM",
                "time": "4 hours",
                "desc": "Configure HubSpot or similar with AI features",
                "how_to": """**Getting Started with HubSpot (Free CRM):**

**1. Sign Up (10 mins)**
- Go to hubspot.com
- Click "Get started free"
- Create account with work email
- Choose "Sales" as your focus

**2. Import Your Contacts (30 mins)**
- Go to Contacts → Import
- Upload CSV of existing leads/customers
- Map fields (name, email, company, etc.)

**3. Set Up Deal Pipeline (30 mins)**
- Go to Sales → Deals → Pipeline
- Customize stages to match YOUR sales process:
  - Lead In
  - Contacted
  - Meeting Scheduled
  - Proposal Sent
  - Negotiation
  - Closed Won / Closed Lost

**4. Connect Your Email (15 mins)**
- Settings → Integrations → Email
- Connect Gmail or Outlook
- Enable email tracking (see when leads open)

**5. Enable AI Features (15 mins)**
- HubSpot AI is built into the free CRM
- Creates contact summaries
- Suggests next actions
- Helps write emails""",
                "template": """CRM SETUP CHECKLIST
===================

□ Account created
□ Team members invited
□ Email connected
□ Calendar connected

CONTACTS:
□ Existing contacts imported
□ Contact properties customized
□ Lead source tracking set up

PIPELINE:
□ Stages defined:
  Stage 1: _____________
  Stage 2: _____________
  Stage 3: _____________
  Stage 4: _____________
  Stage 5: _____________
  Stage 6: Won/Lost

□ Deal values estimated
□ Win probability per stage set

AUTOMATIONS:
□ Task reminders enabled
□ Follow-up sequences created
□ Meeting scheduler connected

REPORTING:
□ Dashboard created
□ Key metrics defined
□ Weekly review scheduled
""",
            },
            {
                "title": "Build Lead Scoring System",
                "time": "3 hours",
                "desc": "Automatically rank leads by likelihood to buy",
                "how_to": """**Lead Scoring = Points for behaviors and attributes that indicate buying intent**

**Give POSITIVE points for:**

Demographic Fit:
- Job title matches ICP: +15 points
- Company size matches ICP: +10 points
- Industry matches ICP: +10 points
- Location matches: +5 points

Engagement Signals:
- Opened email: +1 point
- Clicked email link: +3 points
- Visited pricing page: +10 points
- Downloaded content: +5 points
- Attended webinar: +15 points
- Requested demo: +25 points

**Give NEGATIVE points for:**
- Competitor domain: -50 points
- Student email (.edu): -20 points
- Unsubscribed: -30 points
- No engagement in 60 days: -10 points

**In HubSpot:**
1. Go to Settings → Properties → Contact Properties
2. Find "HubSpot Score"
3. Click "Add criteria" for positive/negative attributes
4. Set point values
5. Create views filtered by score

**Score Thresholds:**
- 0-20: Cold - nurture with content
- 21-50: Warm - begin outreach
- 51-75: Hot - prioritize follow-up
- 76+: Sales Ready - call immediately""",
                "template": """LEAD SCORING MODEL
==================

POSITIVE POINTS:
Attribute/Behavior                    Points
--------------------------------------------
Job title matches ICP                 +15
Company size matches ICP              +10
Visited website                       +2
Opened email                          +1
Clicked email                         +3
Visited pricing page                  +10
Downloaded content                    +5
Filled out contact form               +15
Requested demo                        +25
Attended webinar                      +15
Referred by customer                  +20

NEGATIVE POINTS:
Attribute/Behavior                    Points
--------------------------------------------
Competitor company                    -50
Personal email (gmail, etc.)          -5
No engagement 30 days                 -5
No engagement 60 days                 -10
Unsubscribed                          -30
Bounced email                         -25

SCORE TIERS:
0-20 = Cold Lead → Nurture sequence
21-50 = Warm Lead → Outreach sequence
51-75 = Hot Lead → Priority follow-up
76+ = Sales Ready → Immediate call

REVIEW & ADJUST: Monthly
""",
            },
            {
                "title": "Create Outreach Sequences",
                "time": "4 hours",
                "desc": "Design automated follow-up email sequences",
                "how_to": """**Create these essential sequences:**

**Sequence 1: New Lead Follow-Up (5-7 touches)**
- Day 0: Introduction email
- Day 2: Value-add (share relevant content)
- Day 5: Case study or testimonial
- Day 8: Check-in + new angle
- Day 12: Break-up email ("Should I close your file?")

**Sequence 2: Post-Meeting Follow-Up**
- Same day: Thank you + recap + next steps
- Day 2: Additional resource related to discussion
- Day 5: Check-in if no response

**Sequence 3: Re-engagement (Cold Leads)**
- Email 1: "Quick update" - what's new
- Email 2: New case study or offer
- Email 3: "Is this still relevant?"

**Writing Effective Sales Emails:**
1. Short subject lines (4-7 words)
2. Personalize first line (research them)
3. Focus on THEIR pain, not your product
4. One clear CTA
5. Keep under 150 words
6. No attachments in first email

**Use AI to help:**
- Paste their LinkedIn/website into ChatGPT
- Ask: "Write a personalized outreach email for this person based on their background\"""",
                "template": """OUTREACH EMAIL TEMPLATES
========================

COLD OUTREACH - Email 1
-----------------------
Subject: [Mutual connection/Relevant trigger]

Hi [First Name],

[Personalized observation - something specific about them/their company]

I work with [similar companies/roles] who struggle with [specific problem].

[One sentence about how you help - focus on outcome, not features]

Worth a 15-minute chat to see if this could help [Company Name]?

[Your Name]

---

COLD OUTREACH - Email 2 (Day 3)
-------------------------------
Subject: Re: [Previous subject]

Hi [First Name],

Wanted to share this quick [case study/article/insight] - thought you'd find it relevant given [their situation].

[Link or brief summary]

Happy to walk through how [other company] achieved [specific result] if helpful.

[Your Name]

---

BREAK-UP EMAIL (Final)
----------------------
Subject: Closing the loop

Hi [First Name],

I've reached out a few times and haven't heard back - totally understand if the timing isn't right.

Should I close out your file, or is there a better time to reconnect?

Either way, no hard feelings!

[Your Name]

P.S. If someone else at [Company] would be better to chat with, happy to connect with them instead.
""",
            },
            {
                "title": "Train & Monitor AI Continuously",
                "time": "Ongoing",
                "desc": "Optimize your sales AI over time",
                "how_to": """**Weekly Review (30 mins):**
1. Check lead scores - are hot leads actually converting?
2. Review sequence performance - open rates, reply rates
3. Look at won deals - what behaviors did they show?
4. Look at lost deals - any patterns?

**Monthly Optimization:**
1. Adjust lead scoring weights based on actual conversions
2. Update sequences based on what's working
3. Add new triggers as you learn patterns
4. Remove underperforming emails

**Using AI for Research:**
Before each call, use ChatGPT to:
- Summarize prospect's company (paste their website)
- Find recent news about them
- Generate talking points based on their industry
- Prepare objection responses

**Prompt for Pre-Call Research:**
"I'm about to call [Name], [Title] at [Company]. Based on this information from their website: [paste info], give me:
1. Three talking points relevant to their role
2. Two questions to ask about their challenges
3. How our [product] might help them\"""",
                "template": """WEEKLY SALES AI REVIEW
======================
Week of: _____________

LEAD SCORING ACCURACY:
Hot leads (75+) contacted: _____
Hot leads converted: _____
Accuracy rate: _____%
Adjustments needed: _____________

SEQUENCE PERFORMANCE:
                    This Week    Goal
New lead sequence:
- Open rate:        ____%        40%+
- Reply rate:       ____%        10%+
- Meetings booked:  _____        _____

Re-engagement sequence:
- Open rate:        ____%        30%+
- Reply rate:       ____%        5%+

TOP PERFORMING:
- Best subject line: _____________
- Best email body: _____________
- Best send time: _____________

UNDERPERFORMING (needs attention):
- _____________
- _____________

NEXT WEEK EXPERIMENTS:
1. _____________
2. _____________

LEADS TO PRIORITIZE:
1. Name: _____ Score: _____ Action: _____
2. Name: _____ Score: _____ Action: _____
3. Name: _____ Score: _____ Action: _____
""",
            },
        ],
    },
    {
        "id": "analytics",
        "title": "AI Business Analytics",
        "icon": "📊",
        "category": "Operations",
        "difficulty": "Medium",
        "time": "2-4 weeks",
        "cost": "$50-300/mo",
        "roi": "Data-driven decisions",
        "description": "Use AI to analyze sales data, predict trends, and generate actionable insights.",
        "best_for": ["Retail", "E-commerce", "Restaurants", "Service Businesses"],
        "tools": [
            {
                "name": "ChatGPT + Code Interpreter",
                "cost": "$20/mo",
                "url": "https://chat.openai.com",
                "rec": True,
            },
            {
                "name": "Obviously AI",
                "cost": "$75-250/mo",
                "url": "https://obviously.ai",
                "rec": False,
            },
            {
                "name": "Google Looker Studio",
                "cost": "Free",
                "url": "https://lookerstudio.google.com",
                "rec": False,
            },
        ],
        "steps": [
            {
                "title": "Audit Your Data Sources",
                "time": "4 hours",
                "desc": "Identify and document all your business data",
                "how_to": """**List every place your business data lives:**

**Sales Data:**
- POS system (Square, Shopify, etc.)
- CRM (HubSpot, Salesforce)
- Invoicing software (QuickBooks, FreshBooks)
- E-commerce platform

**Marketing Data:**
- Google Analytics
- Social media insights
- Email marketing platform
- Ad platforms (Google Ads, Facebook Ads)

**Operations Data:**
- Inventory system
- Scheduling software
- Employee time tracking
- Customer support tickets

**For each source, document:**
1. What data it contains
2. How to export it (CSV, API, manual)
3. How often it updates
4. Who has access

**Priority data for most businesses:**
1. Sales/Revenue by product, time, customer
2. Customer data (who, how much, how often)
3. Website traffic
4. Marketing spend vs. results""",
                "template": """DATA SOURCE INVENTORY
=====================

SOURCE 1: _____________
Type: [Sales/Marketing/Operations]
Platform: _____________
Data includes: _____________
Export method: [CSV/API/Manual]
Update frequency: [Real-time/Daily/Weekly]
Access: [Who can export]

SOURCE 2: _____________
Type: [Sales/Marketing/Operations]
Platform: _____________
Data includes: _____________
Export method: [CSV/API/Manual]
Update frequency: [Real-time/Daily/Weekly]
Access: [Who can export]

[Repeat for all sources]

PRIORITY DATA FOR ANALYSIS:
1. _____________ from _____________
2. _____________ from _____________
3. _____________ from _____________

DATA GAPS (don't have but need):
- _____________
- _____________

INTEGRATION OPPORTUNITIES:
- Can connect _____ to _____
- Can automate _____ export
""",
            },
            {
                "title": "Clean & Prepare Data",
                "time": "4 hours",
                "desc": "Export and organize data for AI analysis",
                "how_to": """**Step 1: Export Your Key Data**
- Export as CSV files from each platform
- Include at least 6-12 months of data
- Export at the most granular level (daily, per transaction)

**Step 2: Clean the Data**
Common issues to fix:
- Remove duplicate rows
- Fix date formats (make consistent)
- Handle missing values (delete row or fill in)
- Standardize names (e.g., "NYC" vs "New York City")
- Remove test transactions

**Step 3: Combine Data**
Create a "master" spreadsheet or folder with:
- Sales data
- Customer data
- Product data
All with a common identifier (customer ID, date, product SKU)

**Using ChatGPT for Cleaning:**
Upload your CSV to ChatGPT (Plus required) and say:
"Clean this data:
1. Remove duplicates
2. Standardize date format to YYYY-MM-DD
3. Fill missing values in [column] with [value]
4. Show me a summary of the cleaned data\"""",
                "template": """DATA CLEANING CHECKLIST
======================

FILE: _____________
Rows before cleaning: _____
Date range: _____ to _____

CLEANING STEPS:
□ Duplicates removed: _____ rows
□ Date format standardized: [YYYY-MM-DD]
□ Missing values handled:
  - Column ___: [deleted/filled with ___]
  - Column ___: [deleted/filled with ___]
□ Names/categories standardized
□ Test data removed
□ Outliers reviewed (unusually high/low values)

Rows after cleaning: _____
Data quality score: ___/10

COLUMNS INCLUDED:
□ Date/Time
□ Transaction ID
□ Customer ID
□ Product/Service
□ Quantity
□ Revenue
□ [Other]: _____________
□ [Other]: _____________

READY FOR ANALYSIS: □ Yes □ No
Issues remaining: _____________
""",
            },
            {
                "title": "Define Key Business Questions",
                "time": "2 hours",
                "desc": "Decide what insights you need from your data",
                "how_to": """**Start with these universal questions:**

**Revenue & Sales:**
- What are our total sales trends? (growing/declining)
- What are our best selling products/services?
- What's our average order value?
- Which day/time do we sell most?
- What's our revenue by customer segment?

**Customers:**
- Who are our best customers?
- How often do customers return?
- What's our customer lifetime value?
- Where are we losing customers?
- What products do customers buy together?

**Operations:**
- What's our busiest time?
- Where are we overstaffed/understaffed?
- What products should we stock more/less of?

**Marketing:**
- Which channels bring most customers?
- What's our customer acquisition cost?
- Which campaigns are most effective?

**Pick your TOP 5 questions to start:**
Focus on questions that, if answered, would change how you run your business.""",
                "template": """KEY BUSINESS QUESTIONS
======================

Our TOP 5 questions to answer with data:

1. Question: _____________
   Why it matters: _____________
   Data needed: _____________
   
2. Question: _____________
   Why it matters: _____________
   Data needed: _____________
   
3. Question: _____________
   Why it matters: _____________
   Data needed: _____________
   
4. Question: _____________
   Why it matters: _____________
   Data needed: _____________
   
5. Question: _____________
   Why it matters: _____________
   Data needed: _____________

DECISIONS THESE WILL INFORM:
- _____________
- _____________
- _____________

HOW OFTEN WE'LL REVIEW:
[ ] Daily [ ] Weekly [ ] Monthly
""",
            },
            {
                "title": "Build Analysis & Dashboards",
                "time": "6 hours",
                "desc": "Use AI to analyze data and create visualizations",
                "how_to": """**Option 1: ChatGPT + Code Interpreter (Easiest)**

1. Go to chat.openai.com (need Plus: $20/mo)
2. Upload your CSV file
3. Ask questions in plain English:

"Analyze this sales data and tell me:
1. Total revenue trend by month
2. Top 10 products by revenue
3. Which day of week has highest sales
4. Customer purchase frequency distribution
5. Create charts for each insight"

**Option 2: Google Looker Studio (Free Dashboard)**

1. Go to lookerstudio.google.com
2. Connect your data source (Google Sheets, CSV)
3. Drag and drop to create charts:
   - Line chart for trends over time
   - Bar chart for comparisons
   - Pie chart for breakdowns
   - Scorecards for key numbers

**Option 3: Spreadsheet (Google Sheets/Excel)**

Use Pivot Tables:
1. Select your data
2. Insert → Pivot Table
3. Drag fields to Rows, Columns, Values
4. Create charts from pivot table results

**Recommended Dashboard Elements:**
- Revenue scorecard (this month vs last month)
- Sales trend line (last 12 months)
- Top products bar chart
- Customer breakdown pie chart
- Key metrics table""",
                "template": """DASHBOARD LAYOUT TEMPLATE
=========================

TOP ROW - Key Scorecards:
[Total Revenue] [# Customers] [Avg Order] [# Orders]
 This Month      This Month    Value       This Month
 vs Last Month   vs Last Month             vs Last Month

ROW 2 - Trend Charts:
[Revenue Over Time - Line Chart]
- Show: Last 12 months
- Compare: This year vs Last year

ROW 3 - Breakdowns:
[Top Products]      [Sales by Channel]
Bar Chart           Pie Chart

ROW 4 - Customer Insights:
[Customer Segments] [Purchase Frequency]
Bar Chart           Histogram

ROW 5 - Detailed Table:
[Recent Transactions / Top Customers / etc.]

REFRESH FREQUENCY: [Daily/Weekly]
ACCESS: [Who can view]
""",
            },
            {
                "title": "Automate Reports & Insights",
                "time": "2 hours",
                "desc": "Set up recurring automated analysis",
                "how_to": """**Weekly Automated Report Setup:**

**Option 1: Email Yourself Data Summaries**
- Most platforms (Shopify, Square, Mailchimp) have scheduled reports
- Set them to email you every Monday morning
- Include: Last week vs previous week comparisons

**Option 2: Google Looker Studio Scheduled Email**
1. Open your dashboard
2. Click Share → Schedule email delivery
3. Set frequency (weekly recommended)
4. Add recipients

**Option 3: ChatGPT Weekly Analysis Ritual**

Every Monday, upload fresh data to ChatGPT and use this prompt:

"Analyze this week's data compared to last week. Tell me:
1. Revenue change (% up or down)
2. Top performing products/services
3. Any concerning trends
4. Customer behavior changes
5. 3 actionable recommendations for this week"

**Set Calendar Reminder:**
- Monday 9am: Run weekly analysis
- First of month: Run monthly deep dive
- Quarterly: Full business review

**What to Do with Insights:**
- Share highlights with team
- Make one data-driven decision per week
- Track if decisions improved results""",
                "template": """WEEKLY ANALYTICS REPORT
======================
Week of: _____________
Prepared by: _____________

EXECUTIVE SUMMARY:
This week was [better/worse/same] than last week.
Key highlight: _____________
Key concern: _____________

KEY METRICS:
                    This Week   Last Week   Change
Revenue:            $_____      $_____      ____%
Transactions:       _____       _____       ____%
Avg Order Value:    $_____      $_____      ____%
New Customers:      _____       _____       ____%

TOP PERFORMERS:
1. _____________ ($_____)
2. _____________ ($_____)
3. _____________ ($_____)

TRENDS TO WATCH:
- _____________
- _____________

AI-GENERATED INSIGHTS:
[Paste ChatGPT analysis here]

ACTION ITEMS FOR THIS WEEK:
1. □ _____________
2. □ _____________
3. □ _____________

REVIEWED BY: _____________ DATE: _____
""",
            },
        ],
    },
    {
        "id": "image",
        "title": "AI Image Generation",
        "icon": "🎨",
        "category": "Creative",
        "difficulty": "Easy",
        "time": "1 day",
        "cost": "$10-60/mo",
        "roi": "Save $500+/mo",
        "description": "Generate custom product images, social graphics, and marketing visuals with AI.",
        "best_for": [
            "E-commerce",
            "Marketing Agencies",
            "Content Creators",
            "Real Estate",
        ],
        "tools": [
            {
                "name": "DALL-E 3 (ChatGPT)",
                "cost": "In Plus $20/mo",
                "url": "https://chat.openai.com",
                "rec": True,
            },
            {
                "name": "Midjourney",
                "cost": "$10-30/mo",
                "url": "https://midjourney.com",
                "rec": False,
            },
            {
                "name": "Canva AI",
                "cost": "$13/mo",
                "url": "https://canva.com",
                "rec": False,
            },
        ],
        "steps": [
            {
                "title": "Define Your Visual Style",
                "time": "1 hour",
                "desc": "Create a visual style guide for AI-generated images",
                "how_to": """**Create a Visual Style Document:**

**Answer these questions:**
1. What colors represent your brand? (list 3-5 colors)
2. What mood should images convey? (e.g., professional, playful, luxurious)
3. What style do you prefer? (realistic, illustrated, minimalist, vibrant)
4. What should ALWAYS be in your images?
5. What should NEVER be in your images?

**Look at competitors and brands you admire:**
- Save 10-20 images you like
- Note what you like about each
- Identify patterns

**Style Categories:**

**Photorealistic:** Looks like a real photo
Best for: Products, food, real estate

**Illustrated:** Drawn/artistic look
Best for: Tech, apps, creative services

**Minimalist:** Clean, simple, lots of white space
Best for: Professional services, luxury

**Vibrant/Bold:** Bright colors, high energy
Best for: Food, fitness, youth brands

**Lifestyle:** Products in real-world settings
Best for: E-commerce, home goods""",
                "template": """VISUAL STYLE GUIDE
==================
Business: _____________
Date: _____________

BRAND COLORS:
Primary: _____________ (hex: #______)
Secondary: _____________ (hex: #______)
Accent: _____________ (hex: #______)

STYLE DIRECTION:
[ ] Photorealistic
[ ] Illustrated
[ ] Minimalist  
[ ] Vibrant/Bold
[ ] Lifestyle
[ ] Other: _____________

MOOD/FEELING:
(circle all that apply)
Professional | Friendly | Playful | Luxurious
Warm | Cool | Energetic | Calm | Trustworthy

ALWAYS INCLUDE:
- _____________
- _____________
- _____________

NEVER INCLUDE:
- _____________
- _____________
- _____________

LIGHTING PREFERENCE:
[ ] Natural/soft light
[ ] Bright/studio light
[ ] Moody/dramatic
[ ] Warm tones
[ ] Cool tones

REFERENCE IMAGES:
(attach or link 5-10 inspiration images)
1. _____________ - What I like: _____________
2. _____________ - What I like: _____________
3. _____________ - What I like: _____________
""",
            },
            {
                "title": "Learn Prompting Basics",
                "time": "2 hours",
                "desc": "Master the art of writing effective image prompts",
                "how_to": """**The Basic Prompt Formula:**
[Subject] + [Style] + [Setting] + [Lighting] + [Mood] + [Details]

**Example breakdown:**
"A freshly baked sourdough bread loaf (subject) in professional food photography style (style) on a rustic wooden cutting board in a cozy kitchen (setting) with warm morning window light (lighting) conveying homemade comfort (mood) with visible flour dusting and crispy crust texture (details)"

**Key Prompt Elements:**

**Subject:** What's the main focus?
- "A coffee cup", "A woman working", "Fresh vegetables"

**Style keywords:**
- "professional photography"
- "product photography"  
- "lifestyle photography"
- "flat lay"
- "portrait"
- "minimal illustration"

**Setting/Background:**
- "on white background"
- "in modern office"
- "outdoor cafe setting"
- "kitchen counter"

**Lighting:**
- "natural lighting"
- "soft studio lighting"
- "golden hour"
- "bright and airy"

**Mood:**
- "warm and inviting"
- "clean and professional"
- "energetic and vibrant"

**Camera/Technical:**
- "shallow depth of field"
- "top-down view"
- "close-up shot"
- "wide angle"

**Practice these 5 prompts now:**
1. Your main product on clean background
2. Lifestyle shot of product in use
3. Flat lay arrangement
4. Team/professional portrait style
5. Seasonal/holiday themed image""",
                "template": """IMAGE PROMPT TEMPLATES
======================

PRODUCT SHOT (Clean Background):
"Professional product photography of [PRODUCT], 
centered on pure white background, 
soft studio lighting, 
sharp focus, high-end commercial style,
[SPECIFIC DETAILS about product]"

LIFESTYLE SHOT:
"[PRODUCT] in use by [PERSON DESCRIPTION] 
in [SETTING - modern home, office, etc.],
natural lighting, lifestyle photography style,
warm and inviting mood, 
candid feeling, [BRAND MOOD]"

FLAT LAY:
"Flat lay photography arrangement of [ITEMS],
top-down view on [SURFACE - marble, wood, etc.],
[COLOR SCHEME] color palette,
styled with [PROPS],
bright natural lighting, Instagram-worthy"

FOOD/RESTAURANT:
"Appetizing food photography of [DISH],
on [PLATE/SURFACE], 
[SETTING - restaurant table, rustic kitchen],
warm natural lighting,
shallow depth of field,
garnished with [DETAILS], 
making viewer hungry"

SOCIAL MEDIA GRAPHIC:
"[STYLE - minimal, bold, etc.] graphic design,
[MAIN VISUAL ELEMENT],
[COLOR] color scheme,
modern and clean,
suitable for Instagram post,
[MOOD] feeling"
""",
            },
            {
                "title": "Create Your Asset Library",
                "time": "3 hours",
                "desc": "Generate a core set of images for your business",
                "how_to": """**Generate these core assets:**

**Essential Images for Any Business:**

1. **Hero/Banner Images (3-5)**
   - Website homepage
   - Social media cover photos
   - Email header

2. **Product/Service Images (5-10)**
   - Each main product/service
   - Different angles if relevant
   - In-use/lifestyle versions

3. **Background/Texture Images (3-5)**
   - For text overlays
   - For social media stories
   - For presentations

4. **Seasonal/Campaign Images (4)**
   - Spring/Summer
   - Fall/Winter
   - Holiday
   - Sale/Promotion

5. **Social Media Templates (5-10)**
   - Quote graphics
   - Tip/educational posts
   - Promotional posts

**Workflow for Each Image:**
1. Write detailed prompt based on your style guide
2. Generate 4 variations
3. Pick the best one
4. Note what worked in prompt (save for future)
5. Edit in Canva if needed (add text, crop, adjust)
6. Save in organized folder

**Pro tip:** Generate in batches by category. Do all product shots at once, then all lifestyle shots, etc.""",
                "template": """ASSET LIBRARY CHECKLIST
=======================

HERO IMAGES:
□ Website homepage hero
  Prompt used: _____________
  File: _____________
□ Facebook cover
  Prompt used: _____________
  File: _____________
□ LinkedIn banner
  Prompt used: _____________
  File: _____________

PRODUCT IMAGES:
□ [Product 1] - clean background
□ [Product 1] - lifestyle
□ [Product 2] - clean background
□ [Product 2] - lifestyle
[Add more as needed]

BACKGROUNDS:
□ Light/bright background for text
□ Dark background for text
□ Textured/lifestyle background
□ Seasonal background

SOCIAL MEDIA:
□ Quote template background
□ Tip post template
□ Promotion template
□ Behind-scenes style
□ Testimonial template

SEASONAL:
□ Spring/Summer
□ Fall/Winter
□ Holiday (Christmas, etc.)
□ Special events

FILE ORGANIZATION:
/AI-Images
  /Products
  /Backgrounds
  /Social-Media
  /Seasonal
  /Approved-Finals
""",
            },
            {
                "title": "Set Up Your Workflow",
                "time": "1 hour",
                "desc": "Create a process for requesting and approving images",
                "how_to": """**Simple Workflow for Solo/Small Team:**

**When you need a new image:**
1. **Request:** Write down exactly what you need
2. **Prompt:** Write prompt using your templates + style guide
3. **Generate:** Create 4 variations
4. **Select:** Pick best one
5. **Edit:** Touch up in Canva if needed
6. **Save:** Put in organized folder
7. **Use:** Add to your content

**For Teams:**

**Create a simple request form:**
- What is this image for?
- Where will it be used?
- What size do you need?
- Deadline?
- Any specific requirements?

**Approval process:**
1. Requester fills out form
2. Designer/AI generates options
3. Requester picks favorite
4. Final approval
5. Image added to library

**Tools to Help:**
- **Canva:** Edit, resize, add text
- **Remove.bg:** Remove backgrounds
- **TinyPNG:** Compress file sizes
- **Google Drive/Dropbox:** Store and share

**Sizing Guide:**
- Instagram Post: 1080x1080
- Instagram Story: 1080x1920
- Facebook Post: 1200x630
- LinkedIn Post: 1200x627
- Website Hero: 1920x1080""",
                "template": """IMAGE REQUEST FORM
==================

Requested by: _____________
Date needed: _____________

IMAGE PURPOSE:
What is this for? _____________
Where will it be used? 
[ ] Website  [ ] Social media  [ ] Email
[ ] Print    [ ] Ads          [ ] Other: ____

SIZE NEEDED:
[ ] Square (1080x1080) - Instagram
[ ] Landscape (1200x630) - Facebook/Blog
[ ] Portrait (1080x1920) - Stories
[ ] Custom: _____ x _____

DESCRIPTION:
What should be in the image?
_________________________________
_________________________________

MOOD/FEELING:
_________________________________

TEXT TO INCLUDE (if any):
_________________________________

REFERENCE IMAGES (if any):
_________________________________

URGENCY:
[ ] ASAP  [ ] This week  [ ] Flexible

---
FOR CREATOR USE:
Prompt used: _____________
# Variations generated: _____
Selected version: _____
Approved by: _____________
Final file location: _____________
""",
            },
            {
                "title": "Integrate with Design Tools",
                "time": "1 hour",
                "desc": "Connect AI images with your existing design workflow",
                "how_to": """**Connect AI Images to Canva (Recommended):**

1. **Save AI images to your computer**
2. **Upload to Canva:**
   - Open Canva
   - Go to Uploads → Upload files
   - Drag in your AI images
3. **Create Brand Kit:**
   - Go to Brand Kit (Canva Pro)
   - Add your colors
   - Add your fonts
   - Add your logo
4. **Create Templates:**
   - Make one good design per format
   - Save as template
   - Swap AI images as needed

**Canva AI Features (built-in):**
- **Magic Resize:** One design → all sizes
- **Background Remover:** Remove backgrounds instantly
- **Magic Edit:** Change parts of images
- **Text to Image:** Generate directly in Canva

**Other Integrations:**

**Shopify:**
- Upload AI product images directly
- Use for product listings and marketing

**Social Media Schedulers:**
- Buffer, Later, Hootsuite
- Upload images and schedule posts

**Email Marketing:**
- Mailchimp, Klaviyo
- Use as email headers and graphics

**Google Drive/Dropbox:**
- Store master files
- Share with team members
- Organize by campaign/date

**Tips:**
- Always keep original AI files
- Create different crops/sizes from one image
- Build a "template" in Canva for quick edits
- Maintain consistent naming convention""",
                "template": """TOOL INTEGRATION CHECKLIST
==========================

PRIMARY DESIGN TOOL: [ ] Canva [ ] Figma [ ] Adobe [ ] Other:___

CANVA SETUP:
□ Account created/upgraded
□ Brand Kit configured:
  □ Logo uploaded
  □ Brand colors added
  □ Brand fonts added
□ AI images uploaded to library
□ Templates created for:
  □ Instagram post
  □ Facebook post
  □ Story
  □ Email header
  □ Other: _________

FILE STORAGE:
Platform: [ ] Google Drive [ ] Dropbox [ ] Other:___
Folder structure created: □

CONNECTED PLATFORMS:
□ Website CMS: _____________
□ Social scheduler: _____________
□ Email platform: _____________
□ E-commerce: _____________

TEAM ACCESS:
Who needs access: _____________
Permissions set: □

NAMING CONVENTION:
Format: [date]_[type]_[description]
Example: 2024-01_product_blue-widget-hero

BACKUP SYSTEM:
Where: _____________
Frequency: [ ] Daily [ ] Weekly [ ] Monthly
""",
            },
        ],
    },
]

# Content Templates
CONTENT_TEMPLATES = [
    {"id": "social", "name": "Social Media Post", "icon": "📱"},
    {"id": "email", "name": "Marketing Email", "icon": "📧"},
    {"id": "product", "name": "Product Description", "icon": "🛍️"},
    {"id": "blog", "name": "Blog Post Outline", "icon": "📝"},
    {"id": "ad", "name": "Ad Copy", "icon": "📢"},
    {"id": "chatbot", "name": "Chatbot Script", "icon": "🤖"},
]

# Prompt Categories
PROMPT_CATEGORIES = [
    {"id": "customer_service", "name": "Customer Service Bot", "icon": "💬"},
    {"id": "content_writer", "name": "Content Writer", "icon": "✍️"},
    {"id": "sales_assistant", "name": "Sales Assistant", "icon": "📈"},
    {"id": "data_analyst", "name": "Data Analyst", "icon": "📊"},
    {"id": "email_writer", "name": "Email Writer", "icon": "📧"},
    {"id": "social_manager", "name": "Social Media Manager", "icon": "📱"},
]


def calculate_roi(
    hours_on_task, hourly_rate, ai_efficiency, tool_cost, implementation_hours
):
    """Calculate ROI metrics for AI implementation"""
    hours_saved = hours_on_task * (ai_efficiency / 100)
    labor_savings = hours_saved * hourly_rate * 4  # Monthly
    monthly_roi = labor_savings - tool_cost
    implementation_cost = implementation_hours * hourly_rate
    payback_period = implementation_cost / monthly_roi if monthly_roi > 0 else 999
    yearly_roi = (monthly_roi * 12) - implementation_cost
    roi_percentage = (
        ((yearly_roi / (implementation_cost + tool_cost * 12)) * 100)
        if (implementation_cost + tool_cost * 12) > 0
        else 0
    )

    return {
        "hours_saved": round(hours_saved * 4),
        "monthly_roi": round(monthly_roi),
        "yearly_roi": round(yearly_roi),
        "payback_period": round(payback_period, 1),
        "roi_percentage": round(roi_percentage),
    }


def get_assessment_results():
    """Calculate assessment results based on answers"""
    answers = st.session_state.assessment_answers

    numeric_scores = []
    for key in ["tech_comfort", "data_quality", "budget", "team_size"]:
        if key in answers and isinstance(answers[key], int):
            numeric_scores.append(answers[key])

    avg_score = sum(numeric_scores) / len(numeric_scores) if numeric_scores else 1
    pain_point = answers.get("pain_points", "customer_service")

    if avg_score < 2:
        level = {
            "name": "Beginner",
            "color": "🟡",
            "desc": "Start with simple, low-cost AI tools",
        }
        recommendations = ["chatbot", "content", "image"]
    elif avg_score < 3:
        level = {
            "name": "Intermediate",
            "color": "🔵",
            "desc": "Ready for integrated AI solutions",
        }
        recommendations = ["content", "email", "chatbot", "analytics"]
    else:
        level = {
            "name": "Advanced",
            "color": "🟢",
            "desc": "Ready for comprehensive AI transformation",
        }
        recommendations = ["sales", "analytics", "email", "content", "chatbot"]

    pain_point_map = {
        "customer_service": "chatbot",
        "content": "content",
        "admin": "analytics",
        "sales": "sales",
    }

    priority = pain_point_map.get(pain_point, "chatbot")
    if priority in recommendations:
        recommendations.remove(priority)
    recommendations.insert(0, priority)

    return {
        "avg_score": avg_score,
        "level": level,
        "recommendations": recommendations[:4],
        "pain_point": pain_point,
    }


def call_openai(messages, system_prompt=None):
    """Call OpenAI API with messages"""
    client = get_openai_client()
    if not client:
        return "⚠️ OpenAI API key not configured. Please add OPENAI_API_KEY to your Streamlit secrets."

    try:
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)

        response = client.chat.completions.create(
            model="gpt-4o", messages=full_messages, max_tokens=1500, temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error calling OpenAI: {str(e)}"


# Sidebar Navigation
st.sidebar.markdown(f"## 🧠 {BRAND_CONFIG['business_name']}")
st.sidebar.markdown("*For Small Business*")
st.sidebar.markdown("---")

# Page options
page_options = [
    "🏠 Home",
    "🤖 AI Tools",
    "🎯 Assessment",
    "💡 Use Cases",
    "💰 ROI Calculator",
]

# Get current index
current_index = (
    page_options.index(st.session_state.current_page)
    if st.session_state.current_page in page_options
    else 0
)

# Sidebar radio for navigation (without key)
selected_page = st.sidebar.radio(
    "Navigate", page_options, index=current_index, label_visibility="collapsed"
)

# If user clicked a different radio option, update and rerun
if selected_page != st.session_state.current_page:
    st.session_state.current_page = selected_page
    st.rerun()

# Current page for routing
current_page = st.session_state.current_page

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Stats")
if st.session_state.assessment_complete:
    results = get_assessment_results()
    st.sidebar.markdown(
        f"**Readiness:** {results['level']['color']} {results['level']['name']}"
    )
    st.sidebar.markdown(f"**Top Priority:** {results['recommendations'][0].title()}")
else:
    st.sidebar.markdown("*Complete assessment for personalized insights*")

# Sidebar CTA
render_sidebar_cta()


# HOME PAGE
if current_page == "🏠 Home":
    st.markdown(f"# 🧠 {BRAND_CONFIG['business_name']}")
    st.markdown(f"### {BRAND_CONFIG['tagline']}")

    st.markdown(
        """
    <div class="info-box">
        <strong>🚀 Live AI-Powered</strong> • Get personalized AI strategy, generate content instantly, 
        and transform your business — all powered by OpenAI.
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
        <div class="metric-card">
            <div class="metric-value">🤖</div>
            <div class="metric-label">AI Consultant<br>Get instant advice</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="metric-card">
            <div class="metric-value">✨</div>
            <div class="metric-label">Content Gen<br>Create in seconds</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="metric-card">
            <div class="metric-value">📋</div>
            <div class="metric-label">6 Use Cases<br>Step-by-step guides</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
        <div class="metric-card">
            <div class="metric-value">💰</div>
            <div class="metric-label">ROI Calculator<br>Justify investments</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### How It Works")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        **1️⃣ Take the Assessment**
        - Answer 6 quick questions
        - Get your AI readiness score
        - Receive personalized recommendations
        
        **2️⃣ Chat with AI Consultant**
        - Ask any implementation question
        - Get specific tool recommendations
        - Receive custom strategies
        """
        )

    with col2:
        st.markdown(
            """
        **3️⃣ Generate Content**
        - Create social posts, emails, ads
        - Build custom AI prompts
        - Get chatbot scripts
        
        **4️⃣ Implement & Track ROI**
        - Follow step-by-step guides
        - Calculate your savings
        - Track progress with checklists
        """
        )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("🚀 Get Started - Take Assessment", use_container_width=True):
            st.session_state.assessment_complete = False
            navigate_to("🎯 Assessment")
            st.rerun()

    # Footer on home page
    render_footer()


# AI TOOLS PAGE
elif current_page == "🤖 AI Tools":
    st.markdown("# 🤖 AI-Powered Tools")

    tool_tab = st.tabs(
        ["💬 AI Consultant", "✨ Content Generator", "📋 Prompt Builder"]
    )

    # AI CONSULTANT TAB
    with tool_tab[0]:
        st.markdown("### Chat with Your AI Business Consultant")
        st.markdown("*Ask any question about implementing AI in your business*")

        # Check for API key
        if not get_openai_client():
            st.warning(
                "⚠️ OpenAI API key not configured. Add OPENAI_API_KEY to your Streamlit secrets to enable AI features."
            )
            st.code(
                """
# In .streamlit/secrets.toml:
OPENAI_API_KEY = "your-api-key-here"
            """
            )
        else:
            # Display chat history
            for msg in st.session_state.chat_history:
                if msg["role"] == "assistant":
                    st.markdown(
                        f"""
                    <div class="chat-message chat-assistant">
                        <strong>🤖 AI Consultant:</strong><br>{msg["content"]}
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                    <div class="chat-message chat-user">
                        <strong>👤 You:</strong><br>{msg["content"]}
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

            # Quick prompts
            st.markdown("**Quick Questions:**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("What's the fastest AI win for my business?"):
                    st.session_state.pending_message = (
                        "What's the fastest AI win for my business?"
                    )
                    st.rerun()
                if st.button("Help me create a customer service chatbot"):
                    st.session_state.pending_message = (
                        "Help me create a customer service chatbot"
                    )
                    st.rerun()
            with col2:
                if st.button("How do I calculate AI ROI?"):
                    st.session_state.pending_message = "How do I calculate AI ROI?"
                    st.rerun()
                if st.button("Give me a social media content strategy"):
                    st.session_state.pending_message = (
                        "Give me a social media content strategy"
                    )
                    st.rerun()

            # Chat input
            user_input = st.chat_input("Ask me anything about implementing AI...")

            # Check for pending message from quick buttons
            if (
                "pending_message" in st.session_state
                and st.session_state.pending_message
            ):
                user_input = st.session_state.pending_message
                st.session_state.pending_message = None

            if user_input:
                # Add user message
                st.session_state.chat_history.append(
                    {"role": "user", "content": user_input}
                )

                # Build context from assessment
                business_context = ""
                if st.session_state.assessment_answers:
                    answers = st.session_state.assessment_answers
                    business_context = f"""
Business Profile:
- Type: {answers.get('business_type', 'Not specified')}
- Tech Comfort: {answers.get('tech_comfort', 'Not specified')}/4
- Main Challenge: {answers.get('pain_points', 'Not specified')}
- Budget: {answers.get('budget', 'Not specified')}/4
- Team Size: {answers.get('team_size', 'Not specified')}/4
"""

                system_prompt = f"""You are an expert AI Business Consultant helping small businesses implement AI solutions. 

{business_context}

You have deep knowledge of:
- AI tools (ChatGPT, Claude, Midjourney, automation tools)
- Business operations and AI improvements
- ROI calculations and business cases
- Implementation best practices
- Prompt engineering

Guidelines:
1. Give specific, actionable advice
2. Recommend specific tools with pricing
3. Provide step-by-step guidance
4. Include example prompts they can use
5. Be encouraging but realistic
6. Keep responses focused and practical"""

                # Get AI response
                with st.spinner("Thinking..."):
                    messages = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.chat_history
                    ]
                    response = call_openai(messages, system_prompt)

                st.session_state.chat_history.append(
                    {"role": "assistant", "content": response}
                )
                st.rerun()

            # Clear chat button
            if st.session_state.chat_history:
                if st.button("🗑️ Clear Chat"):
                    st.session_state.chat_history = []
                    st.rerun()

    # CONTENT GENERATOR TAB
    with tool_tab[1]:
        st.markdown("### AI Content Generator")
        st.markdown("*Generate marketing content instantly*")

        template = st.selectbox(
            "Select Content Type",
            options=[t["id"] for t in CONTENT_TEMPLATES],
            format_func=lambda x: next(
                t["icon"] + " " + t["name"] for t in CONTENT_TEMPLATES if t["id"] == x
            ),
        )

        col1, col2 = st.columns(2)
        with col1:
            business_name = st.text_input(
                "Business Name", placeholder="e.g., Sunrise Bakery"
            )
            product = st.text_input(
                "Product/Service/Topic", placeholder="e.g., artisan sourdough bread"
            )
        with col2:
            audience = st.text_input(
                "Target Audience", placeholder="e.g., health-conscious foodies"
            )
            tone = st.selectbox(
                "Tone",
                [
                    "Professional",
                    "Friendly & Casual",
                    "Luxurious & Premium",
                    "Playful & Fun",
                    "Authoritative & Expert",
                    "Empathetic & Caring",
                ],
            )

        additional_info = st.text_area(
            "Additional Details (optional)",
            placeholder="Any specific promotions, key messages, or requirements...",
        )

        if st.button("✨ Generate Content", use_container_width=True):
            if not get_openai_client():
                st.error("OpenAI API key not configured")
            else:
                template_prompts = {
                    "social": f"Create 3 engaging social media posts for {business_name or 'a business'} about {product or 'their product'}. Target: {audience or 'general audience'}. Tone: {tone}. {additional_info}\n\nInclude hashtags and best platform for each.",
                    "email": f"Write a marketing email for {business_name or 'a business'} promoting {product or 'their product'}. Target: {audience or 'subscribers'}. Tone: {tone}. {additional_info}\n\nInclude: 3 subject lines, preview text, body (150-200 words), CTA, P.S. line.",
                    "product": f"Write a product description for {product or 'a product'} by {business_name or 'a business'}. Target: {audience or 'customers'}. Tone: {tone}. {additional_info}\n\nInclude: headline, short description, features, benefits, CTA.",
                    "blog": f"Create a blog post outline for {business_name or 'a business'} about {product or 'their expertise'}. Target: {audience or 'readers'}. Tone: {tone}. {additional_info}\n\nInclude: SEO title, meta description, intro hook, 5-7 sections, conclusion, keywords.",
                    "ad": f"Write ad copy for {business_name or 'a business'} promoting {product or 'their product'}. Target: {audience or 'customers'}. Tone: {tone}. {additional_info}\n\nCreate versions for: Facebook/Instagram, Google Search, LinkedIn.",
                    "chatbot": f"Create a chatbot script for {business_name or 'a business'} handling {product or 'customer inquiries'}. Target: {audience or 'website visitors'}. Tone: {tone}. {additional_info}\n\nInclude: welcome message, 5 FAQ Q&As, booking flow, handoff message.",
                }

                with st.spinner("Generating content..."):
                    response = call_openai(
                        [{"role": "user", "content": template_prompts[template]}]
                    )
                    st.session_state.generated_content = response

        if st.session_state.generated_content:
            st.markdown("### Generated Content")
            st.markdown(st.session_state.generated_content)

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download Content",
                    st.session_state.generated_content,
                    file_name=f"{template}_content.txt",
                    mime="text/plain",
                )
            with col2:
                if st.button("🔄 Regenerate"):
                    st.session_state.generated_content = ""
                    st.rerun()

    # PROMPT BUILDER TAB
    with tool_tab[2]:
        st.markdown("### Custom Prompt Builder")
        st.markdown("*Build professional system prompts for any AI use case*")

        category = st.selectbox(
            "AI Assistant Type",
            options=[c["id"] for c in PROMPT_CATEGORIES],
            format_func=lambda x: next(
                c["icon"] + " " + c["name"] for c in PROMPT_CATEGORIES if c["id"] == x
            ),
        )

        col1, col2 = st.columns(2)
        with col1:
            pb_business = st.text_input(
                "Business Name", key="pb_business", placeholder="Your business name"
            )
        with col2:
            pb_industry = st.text_input(
                "Industry",
                key="pb_industry",
                placeholder="e.g., Healthcare, Retail, Tech",
            )

        pb_specific = st.text_area(
            "Specific Requirements",
            placeholder="Any specific capabilities, knowledge, or behaviors you need...",
        )

        if st.button("🔧 Generate System Prompt", use_container_width=True):
            if not get_openai_client():
                st.error("OpenAI API key not configured")
            else:
                category_name = next(
                    c["name"] for c in PROMPT_CATEGORIES if c["id"] == category
                )

                prompt = f"""Create a detailed system prompt for an AI assistant that will act as a {category_name} for {pb_business or 'a small business'} in the {pb_industry or 'general'} industry.

Additional requirements: {pb_specific or 'None specified'}

The prompt should:
1. Define the AI's role and personality clearly
2. Include specific knowledge it should have
3. Set boundaries and limitations
4. Include example responses or behaviors
5. Be ready to copy-paste into ChatGPT, Claude, or similar

Format as a ready-to-use system prompt starting with "You are..." """

                with st.spinner("Building prompt..."):
                    response = call_openai([{"role": "user", "content": prompt}])
                    st.session_state.generated_prompt = response

        if st.session_state.generated_prompt:
            st.markdown("### Your Custom System Prompt")
            st.code(st.session_state.generated_prompt, language=None)

            st.download_button(
                "📥 Download Prompt",
                st.session_state.generated_prompt,
                file_name=f"{category}_prompt.txt",
                mime="text/plain",
            )


# ASSESSMENT PAGE
elif current_page == "🎯 Assessment":
    st.markdown("# 🎯 AI Readiness Assessment")

    if not st.session_state.assessment_complete:
        st.markdown("### Answer 6 quick questions to get personalized recommendations")

        answered_count = len(st.session_state.assessment_answers)
        total_questions = len(ASSESSMENT_QUESTIONS)
        progress = answered_count / total_questions

        # Progress bar and status
        st.progress(progress)

        if answered_count == total_questions:
            st.success(
                f"✅ All {total_questions} questions answered! Click the button below to see your results."
            )
        else:
            st.info(
                f"📝 {answered_count} of {total_questions} questions answered. Please answer all questions to see your results."
            )

        st.markdown("---")

        # Questions - using callbacks for immediate visual update
        def update_answer(question_id, key):
            """Callback to update answer when radio changes"""
            value = st.session_state.get(key)
            if value is not None:
                st.session_state.assessment_answers[question_id] = value

        for q in ASSESSMENT_QUESTIONS:
            # Show checkmark if answered
            is_answered = q["id"] in st.session_state.assessment_answers
            status = "✅" if is_answered else "⬜"

            st.markdown(f"### {status} {q['category']}")

            # Get current value if exists
            current_value = st.session_state.assessment_answers.get(q["id"])
            current_index = (
                list(q["options"].keys()).index(current_value)
                if current_value in q["options"]
                else None
            )

            st.radio(
                q["question"],
                options=list(q["options"].keys()),
                format_func=lambda x, opts=q["options"]: opts[x],
                key=f"q_{q['id']}",
                index=current_index,
                on_change=update_answer,
                args=(q["id"], f"q_{q['id']}"),
            )
            st.markdown("---")

        # Always show button area, but disable if not all answered
        st.markdown("### 📊 Get Your Results")
        if answered_count == total_questions:
            if st.button("✨ See My Results", use_container_width=True, type="primary"):
                st.session_state.assessment_complete = True
                st.rerun()
        else:
            remaining = total_questions - answered_count
            st.warning(
                f"⚠️ Please answer {remaining} more question{'s' if remaining > 1 else ''} to see your results."
            )

            # Show which questions are unanswered
            unanswered = [
                q["category"]
                for q in ASSESSMENT_QUESTIONS
                if q["id"] not in st.session_state.assessment_answers
            ]
            st.markdown("**Still need to answer:**")
            for category in unanswered:
                st.markdown(f"- {category}")

    else:
        # Show results
        results = get_assessment_results()

        st.markdown(
            f"## {results['level']['color']} Your Readiness Level: **{results['level']['name']}**"
        )
        st.markdown(f"*{results['level']['desc']}*")

        st.progress(results["avg_score"] / 4)
        st.markdown(f"**Score: {results['avg_score']:.1f} / 4.0**")

        st.markdown("---")
        st.markdown("### 🎯 Your Top Recommended AI Use Cases")

        for i, rec_id in enumerate(results["recommendations"], 1):
            uc = next(u for u in USE_CASES if u["id"] == rec_id)

            with st.expander(
                f"{i}. {uc['icon']} {uc['title']} - {uc['difficulty']}",
                expanded=(i == 1),
            ):
                st.markdown(f"**{uc['description']}**")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"⏱️ **Time:** {uc['time']}")
                with col2:
                    st.markdown(f"💰 **Cost:** {uc['cost']}")
                with col3:
                    st.markdown(f"📈 **ROI:** {uc['roi']}")

                st.markdown(f"**Best for:** {', '.join(uc['best_for'])}")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Retake Assessment"):
                st.session_state.assessment_answers = {}
                st.session_state.assessment_complete = False
                st.rerun()
        with col2:
            if st.button("💬 Chat with AI Consultant"):
                navigate_to("🤖 AI Tools")
                st.rerun()

        # Lead capture form
        render_lead_capture_form(context="assessment")

        # Footer
        render_footer()


# USE CASES PAGE
elif current_page == "💡 Use Cases":
    st.markdown("# 💡 AI Use Case Library")
    st.markdown("### Complete Implementation Guides with Templates")
    st.markdown(
        "*Select a use case below to see the full step-by-step implementation guide*"
    )

    st.markdown("---")

    # Filter
    col1, col2 = st.columns([1, 3])
    with col1:
        difficulty_filter = st.multiselect(
            "Filter by Difficulty", ["Easy", "Medium"], default=["Easy", "Medium"]
        )

    # Use case selector
    filtered_cases = [uc for uc in USE_CASES if uc["difficulty"] in difficulty_filter]

    # Display as cards first
    st.markdown("### Choose a Use Case")

    cols = st.columns(3)
    for idx, uc in enumerate(filtered_cases):
        with cols[idx % 3]:
            if st.button(
                f"{uc['icon']} {uc['title']}\n\n{uc['difficulty']} • {uc['time']} • {uc['cost']}",
                key=f"uc_btn_{uc['id']}",
                use_container_width=True,
            ):
                st.session_state.selected_use_case = uc["id"]

    # Initialize selected use case
    if "selected_use_case" not in st.session_state:
        st.session_state.selected_use_case = (
            filtered_cases[0]["id"] if filtered_cases else None
        )

    st.markdown("---")

    # Display selected use case details
    if st.session_state.selected_use_case:
        uc = next(
            (u for u in USE_CASES if u["id"] == st.session_state.selected_use_case),
            None,
        )

        if uc:
            # Header
            st.markdown(f"## {uc['icon']} {uc['title']}")
            st.markdown(f"*{uc['description']}*")

            # Quick stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("⏱️ Time", uc["time"])
            with col2:
                st.metric("💰 Cost", uc["cost"])
            with col3:
                st.metric("📈 ROI", uc["roi"])
            with col4:
                st.metric("📋 Steps", len(uc["steps"]))

            # Best for
            st.markdown(
                "**Best For:** " + ", ".join([f"`{b}`" for b in uc["best_for"]])
            )

            st.markdown("---")

            # Recommended Tools
            st.markdown("### 🛠️ Recommended Tools")
            tool_cols = st.columns(len(uc["tools"]))
            for idx, tool in enumerate(uc["tools"]):
                with tool_cols[idx]:
                    rec_badge = "⭐ RECOMMENDED" if tool.get("rec", False) else ""
                    st.markdown(
                        f"""
                    **{tool['name']}** {rec_badge}
                    
                    💵 {tool['cost']}
                    
                    🔗 [{tool['url']}]({tool['url']})
                    """
                    )

            st.markdown("---")

            # Implementation Progress - will be calculated after checkboxes
            st.markdown("### 📋 Implementation Progress")
            checklist_key = f"checklist_{uc['id']}"
            num_steps = len(uc["steps"])

            # Create a placeholder for progress that we'll update after checkboxes
            progress_placeholder = st.empty()
            message_placeholder = st.empty()

            st.markdown("---")

            # Step-by-step Implementation Guide
            st.markdown("### 📖 Step-by-Step Implementation Guide")

            for i, step in enumerate(uc["steps"]):
                step_num = i + 1
                cb_key = f"{checklist_key}_cb_{i}"

                # Get current state from checkbox key (default False)
                is_completed = st.session_state.get(cb_key, False)
                status_icon = "✅" if is_completed else f"**Step {step_num}**"

                with st.expander(
                    f"{status_icon} {step['title']} ({step['time']})",
                    expanded=(i == 0 and not is_completed),
                ):

                    # Completion checkbox - just use key, Streamlit manages state
                    st.checkbox("Mark as completed", key=cb_key)

                    st.markdown(f"**Summary:** {step['desc']}")

                    st.markdown("---")

                    # How To Section
                    st.markdown("#### 📝 How To Do This")
                    st.markdown(
                        step.get("how_to", "Detailed instructions coming soon...")
                    )

                    # Template Section (if available)
                    if step.get("template"):
                        st.markdown("---")
                        st.markdown("#### 📄 Template / Worksheet")
                        st.code(step["template"], language=None)

                        # Download button for template
                        st.download_button(
                            label="📥 Download Template",
                            data=step["template"],
                            file_name=f"{uc['id']}_step{step_num}_{step['title'].lower().replace(' ', '_')}.txt",
                            mime="text/plain",
                            key=f"download_{checklist_key}_{i}",
                        )

            # Calculate and display progress AFTER all checkboxes are rendered
            completed = sum(
                1
                for i in range(num_steps)
                if st.session_state.get(f"{checklist_key}_cb_{i}", False)
            )
            with progress_placeholder:
                st.progress(completed / num_steps)
            with message_placeholder:
                if completed == num_steps:
                    st.success(
                        f"🎉 Congratulations! You've completed all {num_steps} steps!"
                    )
                else:
                    st.info(f"📝 {completed} of {num_steps} steps completed")

            st.markdown("---")

            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔄 Reset Progress", key=f"reset_{uc['id']}"):
                    # Clear all checkbox keys for this use case by deleting them
                    for i in range(num_steps):
                        cb_key = f"{checklist_key}_cb_{i}"
                        if cb_key in st.session_state:
                            del st.session_state[cb_key]
                    st.rerun()
            with col2:
                if st.button("💬 Get AI Help", key=f"help_{uc['id']}"):
                    st.session_state.pending_message = f"Help me implement {uc['title']} for my business. Walk me through the process step by step."
                    navigate_to("🤖 AI Tools")
                    st.rerun()
            with col3:
                if st.button("💰 Calculate ROI", key=f"roi_{uc['id']}"):
                    navigate_to("💰 ROI Calculator")
                    st.rerun()


# ROI CALCULATOR PAGE
elif current_page == "💰 ROI Calculator":
    st.markdown("# 💰 AI ROI Calculator")
    st.markdown("*Calculate the potential return on your AI investment*")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Your Current Situation")

        hours_on_task = st.slider("Hours spent on task per week", 1, 40, 20)
        hourly_rate = st.number_input(
            "Hourly labor cost ($)", min_value=10, max_value=200, value=35
        )
        ai_efficiency = st.slider("Expected AI efficiency improvement (%)", 30, 90, 70)
        tool_cost = st.number_input(
            "Monthly AI tool cost ($)", min_value=0, max_value=1000, value=50
        )
        implementation_hours = st.number_input(
            "Implementation hours (one-time)", min_value=1, max_value=100, value=10
        )

    with col2:
        st.markdown("### Projected Returns")

        roi = calculate_roi(
            hours_on_task, hourly_rate, ai_efficiency, tool_cost, implementation_hours
        )

        st.markdown(
            f"""
        <div class="metric-card" style="text-align: center;">
            <div class="metric-value" style="font-size: 3rem;">{roi['roi_percentage']}%</div>
            <div class="metric-label">First Year ROI</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Hours Saved/Month", f"{roi['hours_saved']} hrs")
            st.metric("Monthly Savings", f"${roi['monthly_roi']:,}")
        with col_b:
            st.metric("Yearly ROI", f"${roi['yearly_roi']:,}")
            st.metric("Payback Period", f"{roi['payback_period']} months")

        # Recommendation
        if roi["roi_percentage"] > 200:
            st.success(
                "✅ **Strong investment opportunity.** Proceed with implementation."
            )
        elif roi["roi_percentage"] > 100:
            st.info("📊 **Good ROI potential.** Consider starting with a pilot.")
        else:
            st.warning(
                "⚠️ **Marginal returns.** Look for higher-impact use cases first."
            )

    st.markdown("---")
    st.markdown("### ROI Breakdown")

    st.markdown(
        f"""
| Metric | Value |
|--------|-------|
| Weekly hours on task | {hours_on_task} hrs |
| Hours saved with AI ({ai_efficiency}% efficiency) | {hours_on_task * ai_efficiency / 100:.1f} hrs/week |
| Monthly hours saved | {roi['hours_saved']} hrs |
| Labor savings (@ ${hourly_rate}/hr) | ${roi['hours_saved'] * hourly_rate:,}/month |
| Tool cost | ${tool_cost}/month |
| **Net monthly benefit** | **${roi['monthly_roi']:,}** |
| Implementation cost | ${implementation_hours * hourly_rate:,} |
| **First year net ROI** | **${roi['yearly_roi']:,}** |
    """
    )


# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("*Built with ❤️ for small businesses*")
st.sidebar.markdown("Powered by OpenAI & Streamlit")
