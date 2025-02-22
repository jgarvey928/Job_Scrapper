import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
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
    "software", "development", "technology", "strong", "design", "business", "computer", "project", "engineering", "technical", "application", "related", "environment", "solution", "bachelor",
    "preferred", "problem", "excellent", "plus", "communication", "practice", "process", "working", "including", "tool", "written",
    "skill", "team", "support", "science", "life", "basic", "best", "within", "required", "approach",
    "familiarity", "equivalent", "industry", "build", "role", "service", "field",
    "academic", "cumulative", "gpa", "company", "government", "agency", "perform", "tech", "technology", "companies", "skillstorm", "built", "paid", "government", "agencies", "enterprise",
    "oriented", "window", "user", "company", "requirement", "professional",
    "management", "information", "cycle", "proficiency", "methodology", "verbal", "proficient", "one", "platform",
    "office", "developing", "programming", "use", "level", "training", "partner", "effective",
    "position", "equal", "greater", "open", "language",
    "procedure", "delivery", "general", "issue", "implement", "product", "salary", "configuration",
    "production", "scope", "complex", "expert", "similar", "etc", "benefit",
    "relevant", "time", "need", "following", "provide", "vision", 
    "demonstrated", "education", "combination", "view", "system", "degree", "coding"
])

# Remove stopwords and custom words
stop_words = set(stopwords.words('english'))
all_stop_words = stop_words.union(custom_stop_words)
filtered_tokens = [word for word in lemmatized_tokens if word not in all_stop_words and word.isalnum()]

# Debugging: Print filtered tokens to verify stopwords removal
print("Filtered tokens:", filtered_tokens)

# Frequency Analysis
def frequency_analysis(tokens):
    frequency = Counter(tokens)
    print("Most common tokens:")
    print(frequency.most_common(20))

# Word Cloud
def generate_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

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

# Perform the analyses
frequency_analysis(filtered_tokens)
generate_word_cloud(' '.join(filtered_tokens))
skill_clustering(requirements)
ngram_analysis(filtered_tokens, 2)  # Bigrams
ngram_analysis(filtered_tokens, 3)  # Trigrams
# ngram_analysis(filtered_tokens, 4)  # 4-grams
# ngram_analysis(filtered_tokens, 5)  # 5-grams