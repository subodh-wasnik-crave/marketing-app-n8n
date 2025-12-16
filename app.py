import streamlit as st
import views.blog
import views.email
import views.linkedin_post
import views.video_script

# 1. Global Page Config (Must be here, only once)
st.set_page_config(
    page_title="Marketing Suite",
    layout="wide"
)

# 2. Styling
st.markdown("""
<style>
    .st-key-email_btn button, 
    .st-key-video_btn button, 
    .st-key-blog_btn button, 
    .st-key-linkedin_btn button,
    [data-testid="stLinkButton"] a{
        width: 100%;
        border-radius: 8px;
        height: 6em;
        background-color: white;
        border: 1px solid #ddd;
    }
    
      
    .st-key-email_btn button p, 
    .st-key-video_btn button p, 
    .st-key-blog_btn button p, 
    .st-key-linkedin_btn button p,
    [data-testid="stLinkButton"] p {
        font-size: 24px !important;  /* Much larger text */
        font-weight: 800 !important; /* Extra Bold */
    }

    .output-box {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        background-color: #f9f9f9;
        min-height: 500px;
    }
    .main-header {
        text-align: center; 
        font-size: 3rem; 
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# 3. Navigation State
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

def navigate_to(page):
    st.session_state.current_page = page

# 4. Home Page
def page_home():
    st.markdown('<div class="main-header">MARKETING SUITE</div>', unsafe_allow_html=True)
    st.write("")
    
    _, col1, col2, _ = st.columns([1, 2, 2, 1])
    with col1:
        st.link_button(
            "Customer Segmentation App ", 
            url="https://customer-segmentation-crave.streamlit.app/", 
            use_container_width=True
            )
        if st.button("Email Generator", use_container_width=True, key="email_btn"):
            navigate_to("Email")
        if st.button("Video Script Generator", use_container_width=True, key="video_btn"):
            navigate_to("Video")
        st.link_button(
            "FAQ Chatbot",
            url="https://crave-chatbot.vercel.app/",
            use_container_width=True
        )


            
    with col2:
        st.link_button(
            "Sentiment Analysis App",
            url="https://int_ai_sentimentanalysis-proud-parrot-ip.cfapps.eu10-004.hana.ondemand.com/",
            use_container_width=True
            )
        if st.button("Blog Generator", use_container_width=True, key="blog_btn"):
            navigate_to("Blog")
        if st.button("LinkedIn Post Generator", use_container_width=True, key="linkedin_btn"):
            navigate_to("LinkedIn")
        st.link_button(
            "RFP Response Generator",
            url="https://rfp-demo-1-u9ft5cqd2nuvfc9mrckaig.streamlit.app/",
            use_container_width=True
            )

        

# 5. Router
def main():
    if st.session_state.current_page == 'Home':
        page_home()
    elif st.session_state.current_page == 'Email':
        views.email.show(navigate_to)
    elif st.session_state.current_page == 'Blog':
        views.blog.show(navigate_to)
    elif st.session_state.current_page == 'Video':
        views.video_script.show(navigate_to)
    elif st.session_state.current_page == 'LinkedIn':
        views.linkedin_post.show(navigate_to)

if __name__ == "__main__":
    main()