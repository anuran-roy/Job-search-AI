from langchain_community.document_loaders import RSSFeedLoader

loader = RSSFeedLoader(
    urls=["https://weworkremotely.com/remote-jobs.rss"],
    continue_on_failure=True,
    show_progress_bar=True,
)
#docs = loader.load()
#print(docs[0])