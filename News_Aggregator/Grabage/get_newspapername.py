urls = ["https://timesofindia.indiatimes.com/briefs", "https://indianexpress.com/latest-news/"]

sources = []
for url in urls:
    # Split the URL by '/' and get the second element from the end
    source_name = url.split('.')[0].split('/')[-1]
    # Append the source name to the list
    sources.append(source_name)

print(sources)  # Output: ['timesofindia', 'indianexpress']
