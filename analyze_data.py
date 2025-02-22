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
requirements = read_requirements('job_requirements2.txt')

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
    "oriented", "window", "user", "company", "collaboration", "requirement", "professional",
    "management", "information", "cycle", "proficiency", "methodology", "verbal", "proficient", "one", "platform",
    "office", "developing", "programming", "use", "level", "training", "partner", "effective",
    "position", "equal", "greater", "open", "language",
    "procedure", "delivery", "general", "issue",
    "and/or", "'s", "2+", "hands-on", "etc.", "on-site", "framework",
    "coding", "time", "ii", "configuration", "product", "scripting",
    "provide", "production", "implement", "code", "vision", "developer",
    "stack", "person", "complex", "well", "result", "need", "analytical",
    "benefit", "etc", "combination", "education", "similar"
])

# Remove stopwords and custom words
stop_words = set(stopwords.words('english'))
all_stop_words = stop_words.union(custom_stop_words)

# Filter tokens: keep words with at least one alphanumeric character and not in stopwords
filtered_tokens = [word for word in lemmatized_tokens if word not in all_stop_words and re.search(r'\w', word)]

# Debugging: Print filtered tokens to verify stopwords removal
print("Filtered tokens:", filtered_tokens)

# Frequency Analysis
def frequency_analysis(tokens):
    frequency = Counter(tokens)
    most_common = frequency.most_common(20)
    words, counts = zip(*most_common)
    
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
    plt.pie(counts, labels=words, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Most Common Skills in Requirements')
    plt.savefig(pdf, format='pdf')
    plt.close()

# Word Cloud
def generate_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Skills in Requirements')
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
        print(f"Cluster {i}:")
        for ind in order_centroids[i, :10]:
            print(f" {terms[ind]}")

# N-gram Analysis
def ngram_analysis(tokens, n=2):
    n_grams = ngrams(tokens, n)
    ngram_frequency = Counter(n_grams)
    print(f"Most common {n}-grams:")
    print(ngram_frequency.most_common(20))

# Save all plots to a single PDF file
with PdfPages('requirements_analysis.pdf') as pdf:
    frequency_analysis(filtered_tokens)
    generate_word_cloud(' '.join(filtered_tokens))

# Perform the analyses
skill_clustering(requirements)
ngram_analysis(filtered_tokens, 2)  # Bigrams
ngram_analysis(filtered_tokens, 3)  # Trigrams
ngram_analysis(filtered_tokens, 4)  # 4-grams
# ngram_analysis(filtered_tokens, 5)  # 5-grams