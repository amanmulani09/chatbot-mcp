from typing import List
import arxiv # a open source dir to papers across domains 
import os 
import json 

PAPER_DIR = "papers"

def search_papers(topic:str, max_results: int = 5) -> List[str]:

    """
    search for papers on arxiv based on a topic and store their information
    
    Args: 
        topic: the topic to search for 
        max_results: maximum number of results to retrive (defaults : 5)
    
    Returns:
        List of paper IDs found in the search 
    """
    
    client = arxiv.Client()
    
    searchPayload = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    papers = client.results(searchPayload)
    
    # crate a dir of this topics 
    path = os.path.join(PAPER_DIR, topic.lower().replace(" ", "_"))
    os.makedirs(path,exist_ok=True)

    file_path = os.path.join(path,"papers_info.json")
    
    # try to load existing papers info 

    try:
        with open(file_path,"r") as json_file:
            papers_info = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        papers_info = {}
        
    # process each paper and add papers_info 
    
    paper_ids:List[str] = []
    for paper in papers:
        paper_ids.append(paper.get_short_id())
        paper_info = {
            'title': paper.title,
            'authors': [author.name for author in paper.authors],
            'summary': paper.summary,
            'pdf_url': paper.pdf_url,
            'published': str(paper.published.date())
        }
        papers_info[paper.get_short_id()] = paper_info
        
    with open(file_path,"w") as json_file:
        json.dump(papers_info, json_file, indent=2)
    
    print(f"results are saved in : {file_path}")
    return paper_ids

def extract_info(paper_id:str) -> str :
    """
    Search for information about a specific paper across all directories. 
    
    Args:
        paper_id: the ID on the paper to look for 
        
    Returns: 
        JSON string with paper information found, error message if not found 
        
    """
    
    for item in os.listdir(PAPER_DIR):
        item_path = os.path.join(PAPER_DIR, item)
        if os.path.isdir(item_path):
            file_path = os.path.join(item_path, "papers_info.json")
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as json_file:
                        papers_info = json.load(json_file)
                        if paper_id in papers_info:
                            return json.dumps(papers_info[paper_id], indent=2)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error reading {file_path}: {str(e)}")
                    continue
    
    return f"There's no saved information related to paper {paper_id}."
    