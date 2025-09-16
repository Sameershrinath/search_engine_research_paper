import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

st.set_page_config(
    page_title="Researchpaper Search Engine",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="expanded"
)

indexName = "my_research_paper"
model = SentenceTransformer('all-mpnet-base-v2')

try:
    es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "-cC8rBqKeq_ESUrF7nCi"),
    ca_certs=r"C:\Users\Samee\http_ca.crt",
    verify_certs=True
    )
except ConnectionError as e:
    print("Connection Error:", e)
    
if es.ping():
    print("Succesfully connected to ElasticSearch!!")
else:
    print("Oops!! Can not connect to Elasticsearch!")




def search(input_keyword, k=5):
    vector_of_input_keyword = model.encode(input_keyword).tolist()  
    query = {
        "knn": {
            "field": "DescriptionVector",
            "query_vector": vector_of_input_keyword,
            "k": k,
            "num_candidates": 500
        }
    }

    res = es.search(
        index="my_research_paper",
        body={
            **query,
            "_source": ["Title", "Description"]
        }
    )

    results = [hit["_source"] for hit in res["hits"]["hits"]]
    return results



# This code is not working changing this leaving it becoz may be used later

# def search(input_keyword):
#     model = SentenceTransformer('all-mpnet-base-v2')
#     vector_of_input_keyword = model.encode(input_keyword)

#     query = {
#         "field": "DescriptionVector",
#         "query_vector": vector_of_input_keyword,
#         "k": 10,
#         "num_candidates": 500
#     }
#     res = es.knn_search(index="all_papers"
#                         , knn=query 
#                         , source=["ProductName","Description"]
#                         )
#     results = res["hits"]["hits"]

#     return results

def main():
    # Sidebar
    with st.sidebar:
        st.markdown("### 🦉 Researchpaper search Engine ")
        st.markdown("---")
        
        st.markdown("### ℹ️ About")
        st.info("""
            Just Type the name of any topic and you will get most related Research-paper....
        """)
        
        st.markdown("### 💡 Search Tips")
        st.markdown("""
        - Use descriptive terms
        - Be specific about what you want
        - Examples:
          -Sustainable space
        """)
        
        st.markdown("### 🔧 Search Settings")
        num_results = st.slider("Number of results", 1, 10, 2)
        
        st.markdown("---")
        st.markdown("### 📊 Search Stats")
        st.metric("Total papers", "40+")
    st.markdown("""
    <style>
    .main-header {
        background: red;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .main-title {
        color: white;
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .subtitle {
        color: #f0f0f0;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border: 1px solid #e0e0e0;
    }
    .result-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        transition: transform 0.2s ease;
    }
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    .product-name {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .product-description {
        color: #5a6c7d;
        font-size: 1rem;
        line-height: 1.5;
    }
    .no-results {
        text-align: center;
        padding: 3rem;
        color: #7f8c8d;
        font-size: 1.2rem;
    }
    .search-stats {
        background: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: #2980b9;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🦉 Research Papers</h1>
        <p class="subtitle">Discover amazing Research papers with AI-powered semantic search</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown("### 🔍 What are you looking for?")
            search_query = st.text_input(
                "Search for papers...",
                placeholder="e.g., sustainable Space ....",
                label_visibility="collapsed"
            )
            
            search_button = st.button(
                "🚀 Search papers",
                use_container_width=True,
                type="primary"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Search results
    if search_button:
        if search_query:
            with st.spinner('🔄 Searching for the perfect papers...'):
                results = search(search_query, k=num_results)

            if not results:
                st.markdown("""
                <div class="no-results">
                    <h3>😔 No results found</h3>
                    <p>Try different keywords or check your spelling</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Search statistics
                st.markdown(f"""
                <div class="search-stats">
                    📊 Found {len(results)} relevant papers for "{search_query}"
                </div>
                """, unsafe_allow_html=True)
                
                # Display results
                for i, result in enumerate(results, 1):
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="product-name">
                            🏷️ {result.get("Title", "No Name Available")}
                        </div>
                        <div class="product-description">
                            📝 {result.get('Description', 'No Description Available')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter a search query to find papers!")

                    
if __name__ == "__main__":
    main()
