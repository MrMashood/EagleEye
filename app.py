import streamlit as st
from PIL import Image
from image_verifier import ImageVerifier

# Initialize verifier
verifier = ImageVerifier()

# Page config
st.set_page_config(
    page_title="Image Verification System",
    page_icon="🔍",
    layout="centered"
)

# Title
st.title("🔍 Product Image Verification System")
st.markdown("""
Verify whether a product image matches the seller’s claimed title and category.
This system runs **locally**, uses **open-source AI**, and requires **no API key**.
""")

st.divider()

# Input form
with st.form("verification_form"):
    uploaded_file = st.file_uploader(
        "Upload Product Image",
        type=["png", "jpg", "jpeg"]
    )

    category = st.selectbox(
        "Product Category",
        ["Gaming Console", "Audio", "Electronics", "Other"]
    )

    title = st.text_input(
        "Product Title",
        placeholder="e.g., PlayStation 5 Digital Edition"
    )

    submit = st.form_submit_button("🔍 Verify Product", use_container_width=True)

# Handle submit
if submit:
    if uploaded_file is None:
        st.error("⚠️ Please upload an image.")
    elif not title.strip():
        st.error("⚠️ Please enter a product title.")
    else:
        with st.spinner("🤔 Analyzing image..."):
            image = Image.open(uploaded_file).convert("RGB")

            st.subheader("Uploaded Image")
            st.image(image, use_container_width=True)

            result = verifier.verify_image(image, category, title)

            st.divider()
            st.subheader("Verification Results")

            if result["success"]:
                confidence = result["confidence"]
                verdict = result["verdict"]
                reasoning = result["reasoning"]

                col1, col2 = st.columns([2, 1])

                with col1:
                    st.metric("Confidence Score", f"{confidence}%")

                    if confidence >= 70:
                        st.success(f"✅ Verdict: {verdict}")
                    elif confidence >= 30:
                        st.warning(f"⚠️ Verdict: {verdict}")
                    else:
                        st.error(f"❌ Verdict: {verdict}")

                with col2:
                    st.progress(confidence / 100)

                st.subheader("Analysis")
                st.info(reasoning)

            else:
                st.error(result["reasoning"])