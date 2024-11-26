import matplotlib.pyplot as plt

'''Make graph of article data'''
# Data
total_articles = 1395
neurodegenerative_articles = 933
smell_disorder_articles = 144
both_articles = 92

# Categories and values
categories = ['Neurodegenerative Diseases', 'Smell Disorder', 'Both']
values = [neurodegenerative_articles, smell_disorder_articles, both_articles]

# Create bar graph
plt.figure(figsize=(10, 6))
plt.bar(categories, values, color=['yellow', 'orange', 'red'])
plt.title('Distribution of Articles Across Different Categories')
plt.xlabel('Categories')
plt.ylabel('Number of Articles')
#plt.xticks(rotation=45)

# Save the figure as a high-quality .tiff file
plt.savefig('article_distribution.tiff', format='tiff', dpi=300)

# Display the graph
plt.show()


'''Make graph of entity data'''

# Data
neurodegenerative_entities = 5588
smell_disorder_entities = 405

# Categories and values
categories = ['Neurodegenerative Diseases', 'Smell Disorder']
values = [neurodegenerative_articles, smell_disorder_articles]

# Create bar graph
plt.figure(figsize=(10, 6))
plt.bar(categories, values, color=['orange', 'red'])
plt.title('Distribution of Entities Across Different Categories')
plt.xlabel('Categories')
plt.ylabel('Number of Entities')
#plt.xticks(rotation=45)

# Save the figure as a high-quality .tiff file
plt.savefig('entity_distribution.tiff', format='tiff', dpi=300)

# Display the graph
plt.show()
