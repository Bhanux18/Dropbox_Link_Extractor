import streamlit as st
import dropbox
import pandas as pd
import csv
import os


st.set_page_config(   
                page_title="DB-LinX App",
                page_icon="📥",
                layout="wide",
                initial_sidebar_state="expanded")

st.title("Dropbox Link Xtractor Application")
st.write("Powered by **:red[Mr.X]** ")
st.caption("\n")

ACCESS_TOKEN = st.text_area("🔐Feed your :red[**Dropbox**] API Key Here !:", placeholder="Here goes your key...")
st.write("\n\n\n")
FOLDER_PATH = st.text_input("📂Feed your :red[**Dropbox**] Folder path Here !:", placeholder="Here goes your data...")
   
st.write("\n\n\n\n\n")
btn=st.button("Generate Links")

st.write("-" * 30) 

if btn:
    st.spinner("Inprogress...")
    # 📝 STEP 3: Define the name of the output CSV file
    CSV_FILE_NAME = 'dropbox_links.csv'

    try:
        # Initialize the Dropbox client
        dbx = dropbox.Dropbox(ACCESS_TOKEN)
        print(f"Searching for images in: {FOLDER_PATH}...")

        result = dbx.files_list_folder(FOLDER_PATH)
        image_links = [] # Change to a list of dictionaries/tuples for CSV writing

        # Iterate through the files found in the folder
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                link = None
                try:
                    # 🔗 Get an existing shared link (or create a new one)
                    shared_link_result = dbx.sharing_create_shared_link(entry.path_display)
                    link = shared_link_result.url
                except dropbox.exceptions.ApiError as e:
                    # Handle cases where the link already exists
                    if e.error.is_shared_link_already_exists():
                        links = dbx.sharing_list_shared_links(path=entry.path_display)
                        if links.links:
                            link = links.links[0].url
                    else:
                        print(f"Error creating link for {entry.name}: {e}")
                        continue

                if link:
                    # OPTIONAL: Convert the share link to a direct download/embed link
                    # (changes '?dl=0' to '?raw=1' or just '?dl=1')
                    direct_link = link.replace('?dl=0', '?raw=1')
                    
                    # Add the data as a dictionary to the list
                    image_links.append({
                        'File Name': entry.name,
                        'Dropbox Share Link': link,
                        'Direct Embed Link (Optional)': direct_link
                    })

        # --------------------------------------------------------------------------
        # CSV WRITING SECTION
        # --------------------------------------------------------------------------
        
        if image_links:
            # Create the DataFrame
            df = pd.DataFrame(image_links)
            
            # Generate the CSV content in memory using Pandas to_csv
            csv_content = df.to_csv(index=False).encode('utf-8')
            
            st.success(f"✅ Successfully generated {len(df)} links for {len(image_links)} images.")
            st.write("\n\n\n")
            
            st.download_button(
                label="Download Dropbox Links CSV",
                data=csv_content,
                file_name=CSV_FILE_NAME,
                mime="text/csv",
                type="primary"
            )
        else:
            st.write("\n⚠️ No image files were found.Check the :red[**directory**] .So,links could not be generated.")
            st.write("\n :blue[Arey, yaar Use Common Sense, Simple sa kaam 😁😅!].")

    except dropbox.exceptions.AuthError:
        st.write("\n❌ ERROR: Invalid access token. Please check your ACCESS_TOKEN.")
        st.write("\n :blue[Arey, yaar Use Common Sense, Simple sa kaam 😁😅!].")
    except Exception as e:
        st.write(f"\n❌ An unexpected error occurred: {e}")
        st.write("\n :blue[Arey, yaar Use Common Sense, Simple sa kaam 😁😅!].")


