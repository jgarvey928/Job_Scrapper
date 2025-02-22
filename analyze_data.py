import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import ngrams

# Print NLTK data paths
print("NLTK data paths:", nltk.data.path)

# Ensure you have the necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Function to read requirements from the file
def read_requirements(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    return data.split("\n__________________________________________________\n")

# Load requirements from the file
requirements = read_requirements('job_us_requirements1.txt')

# Combine all requirements into a single list
all_requirements_combined = ' '.join(requirements)

# Tokenize the combined text
tokens = word_tokenize(all_requirements_combined)

# Lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens]

# Define custom words to remove
custom_stop_words = set([
    "year", "years", "work", "using", "new", "understand", "understanding", "experience", "knowledge", "skills", "ability", "must", "have", "with", "the", "and", "or", "to", "a", "in", "of", "for", "on", "as", "is", "are",
    "software", "development", "technology", "strong", "design", "business", "computer", "project", "engineering", "technical", "system", "application", "degree", "related", "environment", "solution", "bachelor",
    "preferred", "data", "problem", "excellent", "plus", "communication", "practice", "process", "working", "including", "tool", "written",
    "skill", "team", "support", "science", "life", "basic", "best", "within", "security", "required", "approach",
    "familiarity", "equivalent", "learn", "industry", "build", "role", "service", "field",
    "academic", "cumulative", "gpa", "company", "government", "agency", "perform", "tech", "technology", "companies", "clients", "skillstorm", "built", "paid", "government", "agencies", "enterprise",
    "oriented", "user", "company", "collaboration", "requirement", "professional",
    "management", "information", "cycle", "proficiency", "methodology", "verbal", "proficient", "one", "platform",
    "office", "developing", "programming", "use", "level", "training", "partner", "effective",
    "position", "equal", "greater", "open", "language",
    "procedure", "delivery", "general", "issue",
    "and/or", "'s", "2+", "hands-on", "etc.", "on-site", "framework",
    "coding", "time", "ii", "configuration", "product", "scripting",
    "provide", "production", "implement", "code", "vision",
    "stack", "person", "complex", "well", "result", "need", "analytical",
    "perform", "career", "contribute", "selected", "perform", "demonstrate", "develop", "desire",
    "previous", "pattern", "performs", "demonstrated", "effectively","salary",
    "benefit", "etc", "combination", "similar", "developer", "end",
    "expertise", "like", "good", "core", "spring", "slack", "e.g.", "highly",
    "learning", "performance", "deployment", "boot"
])

# Remove stopwords and custom words
stop_words = set(stopwords.words('english'))
all_stop_words = stop_words.union(custom_stop_words)

# Filter tokens: keep words with at least one alphanumeric character and not in stopwords
filtered_tokens = [word for word in lemmatized_tokens if word not in all_stop_words and re.search(r'\w', word)]

# Create less_filtered_tokens by removing periods and commas
less_filtered_tokens = [re.sub(r'[.,]', '', word) for word in tokens]

# # Debugging: Print filtered tokens to verify stopwords removal
# print("Filtered tokens:", filtered_tokens)
# print("Less filtered tokens:", less_filtered_tokens)

# Global list to store top 20 most frequent tokens
top_skills = []

# Frequency Analysis
def frequency_analysis(tokens):
    global top_skills
    frequency = Counter(tokens)
    most_common = frequency.most_common(25)
    words, counts = zip(*most_common)
    
    # Store the top 20 most frequent tokens in the global list
    top_skills = list(words)
    
    # Bar Graph
    plt.figure(figsize=(10, 5))
    plt.bar(words, counts)
    plt.xlabel('Skills')
    plt.ylabel('Frequency')
    plt.title('Most Common Skills in Requirements')
    plt.xticks(rotation=90)
    plt.savefig(pdf, format='pdf')
    plt.close()
    
    # Pie Chart
    plt.figure(figsize=(10, 5))
    plt.pie(counts, labels=[f'{word} ({count})' for word, count in zip(words, counts)], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Most Common Skills in Requirements')
    plt.savefig(pdf, format='pdf')
    plt.close()

# Word Cloud
def generate_word_cloud(text, title):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.savefig(pdf, format='pdf')
    plt.close()

# Skill Clustering
def skill_clustering(requirements):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(requirements)
    kmeans = KMeans(n_clusters=5, random_state=0).fit(X)
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    
    for i in range(5):
        cluster_terms = [terms[ind] for ind in order_centroids[i, :20]]
        cluster_text = ' '.join(cluster_terms)
        generate_word_cloud(cluster_text, f'Word Cloud of Cluster {i}')

# N-gram Analysis
def ngram_analysis(tokens, n=2):
    n_grams = ngrams(tokens, n)
    ngram_frequency = Counter(n_grams)
    most_common = ngram_frequency.most_common(20)
    ngrams_list, counts = zip(*most_common)
    ngrams_labels = [' '.join(ngram) for ngram in ngrams_list]
    
    # Pie Chart for N-grams
    plt.figure(figsize=(10, 5))
    plt.pie(counts, labels=[f'{label} ({count})' for label, count in zip(ngrams_labels, counts)], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title(f'Most Common {n}-grams in Requirements')
    plt.savefig(pdf, format='pdf')
    plt.close()

# Save all plots to a single PDF file
with PdfPages('requirements_us_analysis1.pdf') as pdf:
    frequency_analysis(filtered_tokens)
    generate_word_cloud(' '.join(top_skills), 'Word Cloud of Top Skills')
    generate_word_cloud(' '.join(filtered_tokens), 'Word Cloud of Skills in Requirements')
    # skill_clustering(requirements)
    ngram_analysis(less_filtered_tokens, 3)  # Bigrams
    ngram_analysis(less_filtered_tokens, 6)  # Trigrams
    ngram_analysis(less_filtered_tokens, 9)  # 
    ngram_analysis(less_filtered_tokens, 12)  # 



