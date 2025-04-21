import streamlit as st
from find_papers import get_list_of_papers
from scihub_downloader import download_pdf


def main():
    st.set_page_config(page_title="DBLP Paper Searcher",
                       page_icon=":book:", layout="wide")
    with st.container():
        # st.sidebar.title("Search history")
        st.title("DBLP :handshake: SciHub")
        st.subheader("we are not communists, but science must be free ...")

        col1, col2 = st.columns([1, 4])
        with col1:
            choice = st.selectbox(
                "Search Mode",
                ["publication", "author", "venue"],
                label_visibility="collapsed",
                help="Select the mode of search",
                format_func=lambda x: x.capitalize()
            )
        with col2:
            user_input = st.text_input(
                "Search",
                placeholder="Enter your search term...",
                label_visibility="collapsed"
            )

        if user_input:
            try:
                with st.spinner('Searching papers...'):
                    papers = get_list_of_papers(
                        mode=choice,
                        input_text=user_input,
                        num_results=100
                    )

                st.subheader(f"Found {len(papers)} results")

                # Sort papers by year in descending order before displaying
                papers = sorted(papers, key=lambda p: p.get('year', 0), reverse=True)
                for paper in papers:
                    if not isinstance(paper, dict):
                        continue
                    

                    title = paper.get('title', 'Untitled')[:100] + ('...' if len(paper.get('title', 'Untitled')) > 50 else '')
                    year = paper.get('year', 'N/A')
                    authors = paper.get('authors', [])
                    venue = paper.get('venue', 'N/A')
                    with st.expander(f"""***{title}*** ({year})
                                     \nauthors: {', '.join(authors) if isinstance(authors, list) else authors}
                                    \n**{venue}**"""):

                        title = paper.get('title', 'Untitled')
                        authors = paper.get('authors', [])
                        venue = paper.get('venue', 'N/A')
                        doi = paper.get('doi', '')
                        url = paper.get('url', '')

                        col1, col2 = st.columns([10, 1])
                        with col1:
                            if isinstance(authors, list):
                                st.write(f"**Title:** {title}")
                                st.write(f"**Authors:** {', '.join(authors)}")
                                st.write(f"**Venue:** {venue}")
                                st.write(f"**Year:** {year}")
                            if doi:
                                st.write(f"**DOI:** {doi}")
                            if url:
                                st.write(f"**URL:** {url}")
                        with col2:
                            st.button("⬇️", key=title, help="Download the paper",
                                      on_click=lambda:download_pdf(doi=doi) if doi else None, disabled=not doi, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
