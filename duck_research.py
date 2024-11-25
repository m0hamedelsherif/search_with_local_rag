from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

def duck_search_and_scrape(queries, num_results=3):
    """Search duckduckgo with multiple queries and scrape content from results"""
    all_content = []
    seen_links = set()
    wrapper = DuckDuckGoSearchAPIWrapper(max_results=num_results)
    search = DuckDuckGoSearchResults(api_wrapper=wrapper,output_format="list")

    for query in queries[:num_results]:
        try:
            search_results = search.invoke(query)

            for result in search_results[:num_results]:
                if result['link'] in seen_links:
                    continue
                    
                try:
                    all_content.append({
                        'title': result['title'],
                        'link': result['link'],
                        'content': result['snippet'],
                        'query': query,
                        'order': search_results.index(result)+1
                    })
                    seen_links.add(result['link'])

                except Exception as e:
                    print(f"Error scraping {result['link']}: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error searching for query '{query}': {str(e)}")
            continue

    print(f"All content: {all_content}")  # Debug print
    return all_content