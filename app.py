import os
import streamlit as st
from PIL import Image
from image_verifier import ImageVerifier
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Initialize verifier
verifier = ImageVerifier(GOOGLE_API_KEY)

# Page config
st.set_page_config(
    page_title="Image Verification System",
    page_icon="🔍",
    layout="centered"
)

# Title and description
st.title("🔍 Product Image Verification System")
st.markdown("""
This tool helps detect potential fraud by verifying if product images match their descriptions.
Upload an image, select the category, and enter the product title to get a confidence score.
""")

st.divider()

# Create form for inputs
with st.form("verification_form"):
    # Image upload
    uploaded_file = st.file_uploader(
        "Upload Product Image",
        type=["png", "jpg", "jpeg"],
        help="Upload the product image you want to verify"
    )
    
    # Category selection
    category = st.selectbox(
        "Product Category",
        options=["Gaming Console", "Audio"],
        help="Select the category the seller claimed"
    )
    
    # Title input
    title = st.text_input(
        "Product Title",
        placeholder="e.g., PlayStation 5 Digital Edition",
        help="Enter the product title/description provided by the seller"
    )
    
    # Submit button
    submit_button = st.form_submit_button("🔍 Verify Product", use_container_width=True)

# Process verification when form is submitted
if submit_button:
    if uploaded_file is None:
        st.error("⚠️ Please upload an image first!")
    elif not title.strip():
        st.error("⚠️ Please enter a product title!")
    else:
        # Show loading state
        with st.spinner("🤔 Analyzing image and description..."):
            # Load image
            image = Image.open(uploaded_file)
            
            # Display uploaded image
            st.subheader("Uploaded Image")
            st.image(image, caption="Product Image", use_container_width=True)
            
            # Verify image
            result = verifier.verify_image(image, category, title)
            
            # Display results
            st.divider()
            st.subheader("Verification Results")
            
            if result["success"]:
                confidence = result["confidence"]
                verdict = result["verdict"]
                reasoning = result["reasoning"]
                
                # Display confidence with color coding
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.metric("Confidence Score", f"{confidence}%")
                    
                    # Color-coded progress bar
                    if confidence >= 70:
                        st.success(f"**Verdict**: ✅ {verdict}")
                    elif confidence >= 30:
                        st.warning(f"**Verdict**: ⚠️ {verdict}")
                    else:
                        st.error(f"**Verdict**: ❌ {verdict}")
                
                with col2:
                    # Visual indicator
                    if confidence >= 70:
                        st.markdown("### 🟢")
                        st.caption("Likely Match")
                    elif confidence >= 30:
                        st.markdown("### 🟡")
                        st.caption("Uncertain")
                    else:
                        st.markdown("### 🔴")
                        st.caption("Likely Fraud")
                
                # Progress bar for confidence
                st.progress(confidence / 100)
                
                # Display reasoning
                st.subheader("Analysis")
                st.info(reasoning)
                
                # Additional info
                with st.expander("📋 Verification Details"):
                    st.write(f"**Category**: {category}")
                    st.write(f"**Title**: {title}")
                    st.write(f"**Model**: Google Gemini Flash (Latest)")
                    
            else:
                st.error(f"❌ Verification failed: {result['error']}")
                st.info("Please try again or check your internet connection.")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This fraud detection system uses AI to verify if product images match their descriptions.
    
    **How it works:**
    1. Upload a product image
    2. Select the claimed category
    3. Enter the product title
    4. AI analyzes the match
    
    **Confidence Levels:**
    - 🟢 **70-100%**: Likely genuine
    - 🟡 **30-70%**: Uncertain
    - 🔴 **0-30%**: Likely fraud
    
    **Categories:**
    - Gaming Console
    - Audio
    """)
    
    st.divider()
    
    st.caption("Powered by Google Gemini API")
