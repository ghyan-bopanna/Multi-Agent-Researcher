from agents import build_reader_agent, build_search_agent, critic_chain, writer_chain

def extract_text(content):
    """Extract plain text from agent message content (strips extras/signature blocks)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            block["text"] for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return str(content)

def run_research_pipeline(topic : str)-> dict:

    state = {} # Our storage state will be an empty dictionary

    # Search agent working 
    print("\n"+"="*50) 
    print("Step 1 -> The Search agent is working ... ")
    print("="*50)


    search_agent = build_search_agent()
    search_result = search_agent.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic} and make sure to include urls that you find")]
                         })
    #print(search_result['messages'])
    state["search_results"] = extract_text(search_result['messages'][-1].content) #(-1 gives the final ai message  and -2 gives the tool message , refer img(in the case of create agent format))

    print("\n Search Result ",state["search_results"])

    # Step 2 - Reader agent

    print("\n"+"="*50) 
    print("Step 2 -> The Reader agent is scraping top sites ... ")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages" : [("user",
                       f"Based on the following search results on the '{topic}',"
                       f"pick the most relevant URL and scrape it for deeper content. \n\n"
                       f"Search Results : \n{state['search_results'][:800]}"
                       )]
    })

    state['scraped_content'] = extract_text(reader_result['messages'][-1].content)

    print("\n Scraped content \n ", state['scraped_content'])


    print("\n"+"="*50) 
    print("Step 3 -> The Writer agent is drafting the report ... ")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
        
    )
    
    # Make another key in memory state (dictionary) and save the generated report from the LLM
    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research": research_combined
    })

    print("\n Final report \n", state['report'])

    #critic report

    print("\n"+"="*50) 
    print("Step 4 -> The Critic LLM is reviewing your report ... ")
    print("="*50)

    # Store feedback in state now
    state["feedback"] = critic_chain.invoke({
        "report":state["report"]
    })

    print("\n critic report \n", state['feedback'])

    return state

# Call function
if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)



