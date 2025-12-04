import streamlit as st
import requests

def show(navigate_to):
    # Init services

    col_nav, col_title = st.columns([1, 5])
    with col_nav:
        if st.button("← Home"):
            navigate_to("Home")
    with col_title:
        st.title("💼 LinkedIn Post Creator")

    left, right = st.columns([1, 2])
    # ---------------- LEFT SIDE ----------------
    with left:
        st.header("LinkedIn Post Creator")
        user_input = st.text_area(
            "Enter the topic for your LinkedIn post",
            height=400
        )
        if st.button("Create LinkedIn Post"):
            if not user_input.strip():
                st.warning("Please enter a topic.")
            else:
                try:
                    # BLOG GENERATOR WORKFLOW (already working)
                    N8N_WEBHOOK_URL = "https://n8n-app.app.n8n.cloud/webhook/8b60934c-0ead-43c0-4da0-eb3f1f5b1881"
                    payload = {"text": user_input}
                    response = requests.post(N8N_WEBHOOK_URL, json=payload)
                    data = response.json()
                    st.session_state["output"] = data
                except Exception as e:
                    st.session_state["output"] = {"error": str(e)}

    # ---------------- RIGHT SIDE ----------------
    with right:
        st.header("Generated Output")
        if "output" in st.session_state:
            data = st.session_state["output"]
            if "error" in data:
                st.error(data["error"])
            else:
                # extract blog content from nested JSON
                if isinstance(data, dict) and "output" in data:
                    inner = data["output"]
                    heading = inner.get("post title", "")
                    content = inner.get("post content", "")
                    image_description = inner.get("image description", "")
                    hashtags = inner.get("Hashtags", [])
                else:
                    heading = ""
                    content = str(data)
                    image_description = ""
                    hashtags = []
                # Show Title & Content
                st.subheader(heading)
                st.write(content)
                # Ask For Feedback
                st.markdown("### **Do you like the blog? 😊**")
                user_feedback = st.text_input("Type yes or no", "")
                # If YES → allow image creation
                if user_feedback.lower().strip() == "yes":
                    st.success("Great! You liked the blog 🎉")
                    if st.button("Create Image"):
                        st.info("Generating Image from n8n...")
                        # 👉 YOUR IMAGE GENERATOR WEBHOOK URL
                        # Note: Using the local URL from your workflow JSON for local testing
                        IMAGE_N8N_URL = "http://localhost:5678/webhook/8b91c2ce-255e-4582-a7f6-4ffb06465fdf"
                        try:
                            payload = {
                                "prompt": heading,
                                "content": content,
                                "hashtags": hashtags,
                                "image_description": image_description
                            } # sending blog title
                            img_response = requests.post(IMAGE_N8N_URL, json=payload)
                            img_data = img_response.json()
                            # ----------------------------------------------------
                            # 👇 THE FIX: Correctly access the nested 'image' key
                            # ----------------------------------------------------
                            if isinstance(img_data, list) and len(img_data) > 0:
                                # img_data[0] is the top-level dict (e.g., {"success": true, "post": {...}})
                                post_data = img_data[0].get("post", {})
                                image_base64 = post_data.get("image", "")
                            else:
                                image_base64 = ""
                            # ----------------------------------------------------

                            # if image_base64:
                            #     st.subheader("Generated Image")
                            #     display_base64_image(image_base64)
                            # else:
                            #     st.error("❌ No image returned from n8n.")
                        except Exception as e:
                            st.error(f"Error generating image: {e}")
                # If NO
                elif user_feedback.lower().strip() == "no":
                    st.warning("No problem! Try another topic 😊")
        else:
            st.info("Output will appear here after generating.")