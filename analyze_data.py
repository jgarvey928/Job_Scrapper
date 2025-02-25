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
import random

# Global list to store top most frequent tokens
top_skills = []

def download_nltk_data():
    # Ensure you have the necessary NLTK data
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

# Function to read requirements from the file
def read_requirements(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    return data.split("\n__________________________________________________\n")

# Function to combine similar words
def combine_similar_words(tokens, word1, word2):
    combined_tokens = []
    for token in tokens:
        if token == word1 or token == word2:
            combined_tokens.append(word1)
        else:
            combined_tokens.append(token)
    
    return combined_tokens

# Frequency Analysis
def frequency_analysis(tokens, num_top, pdf):

    combined_tokens = combine_similar_words(tokens, 'frontend','front-end')
    combined_tokens = combine_similar_words(combined_tokens, 'backend','back-end')  
    combined_tokens = combine_similar_words(combined_tokens, 'apis','api')  
    combined_tokens = combine_similar_words(combined_tokens, 'windows','window')  
    combined_tokens = combine_similar_words(combined_tokens, 'analysis','analyze')  
    combined_tokens = combine_similar_words(combined_tokens, 'analysis','analytics') 
    combined_tokens = combine_similar_words(combined_tokens, 'reporting','report') 
    combined_tokens = combine_similar_words(combined_tokens, 'communication','communicate') 

    frequency = Counter(combined_tokens)

    most_common = frequency.most_common(num_top)
    words, counts = zip(*most_common)
    
    global top_skills
    # Store the top most frequent tokens in the global list
    top_skills = list(words)
    
    # Bar Graph
    plt.figure(figsize=(12, 6))  # Increased figure size
    plt.bar(words, counts)
    plt.xlabel('Skills')
    plt.ylabel('Frequency')
    plt.title('Most Common Skills in Requirements')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
    plt.tight_layout()  # Adjust layout to prevent clipping
    plt.savefig(pdf, format='pdf')
    plt.close()
    
    # Pie Chart
    plt.figure(figsize=(10, 5))
    plt.pie(counts, labels=[f'{word} ({count})' for word, count in zip(words, counts)], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Most Common Skills in Requirements')
    plt.savefig(pdf, format='pdf')
    plt.close()

# Custom color function for word clouds
def random_color_func(word=None, font_size=None, position=None, orientation=None, random_state=None, **kwargs):
    return "hsl({}, {}%, {}%)".format(random.randint(0, 360), random.randint(50, 100), random.randint(25, 75))

# Word Cloud
def generate_word_cloud(text, title, pdf):
    wordcloud = WordCloud(width=800, height=400, background_color='white', color_func=random_color_func).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.savefig(pdf, format='pdf')
    plt.close()

# Skill Clustering
def skill_clustering(requirements, pdf):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(requirements)
    kmeans = KMeans(n_clusters=5, random_state=0).fit(X)
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    
    for i in range(5):
        cluster_terms = [terms[ind] for ind in order_centroids[i, :20]]
        cluster_text = ' '.join(cluster_terms)
        generate_word_cloud(cluster_text, f'Word Cloud of Cluster {i}', pdf)

# N-gram Analysis
def ngram_analysis(tokens, n, num_top, pdf):
    n_grams = ngrams(tokens, n)
    ngram_frequency = Counter(n_grams)
    most_common = ngram_frequency.most_common(num_top)
    ngrams_list, counts = zip(*most_common)
    ngrams_labels = [' '.join(ngram) for ngram in ngrams_list]
    
    # Pie Chart for N-grams
    plt.figure(figsize=(10, 5))
    plt.pie(counts, labels=[f'{label} ({count})' for label, count in zip(ngrams_labels, counts)], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title(f'Most Common {n}-grams in Requirements')
    plt.savefig(pdf, format='pdf')
    plt.close()

# Analyze Data
def analyze_data(name_file):

    download_nltk_data()

    # Load requirements from the file
    requirements = read_requirements('scrapped_data/'+name_file+'_reqs.txt')

    # Combine all requirements into a single list
    all_requirements_combined = ' '.join(requirements)

    # Tokenize the combined text
    tokens = word_tokenize(all_requirements_combined)

    # Add more text processing for present tense
    # present_tokens = [conjugate(word, tense=PRESENT) for word in tokens]

    # Lemmatization and remove purely numeric tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens if not word.isdigit()]

    # Define custom words to remove
    custom_stop_words = set([
        "year", "years", "work", "using", "new", "understand", "understanding", "experience",
        "knowledge", "skills", "ability", "must", "have", "with", "the", "and", "or", "to", "a", "in", "of", "for", "on", "as", "is", "are",
        "software", "development", "technology", "strong", "design", "business", "computer",
        "project", "engineering", "technical", "system", "application", "degree", "related", "environment", "solution", "bachelor",
        "preferred", "data", "problem", "excellent", "plus", "practice", "process", "working", "including", "tool", "written",
        "skill", "team", "support", "science", "life", "basic", "best", "within", "security", "required", "approach",
        "familiarity", "equivalent", "learn", "industry", "build", "role", "service", "field",
        "academic", "cumulative", "gpa", "company", "government", "agency", "perform",
        "tech", "technology", "companies", "clients", "skillstorm", "built", "paid", "government", "agencies", "enterprise",
        "oriented", "user", "company", "collaboration", "requirement", "professional",
        "management", "information", "cycle", "proficiency", "methodology", "verbal", "proficient", "one", "platform",
        "office", "developing", "programming", "use", "level", "training", "partner", "effective",
        "position", "equal", "greater", "open", "language",
        "procedure", "delivery", "general", "issue", "and/or", "'s", "2+", "hands-on", "etc.", "on-site", "framework",
        "coding", "time", "ii", "configuration", "product", "scripting",
        "provide", "production", "implement", "code", "vision", "stack", "person", "complex", "well", "result", "need", "analytical",
        "perform", "career", "contribute", "selected", "perform", "demonstrate", "develop", "desire",
        "previous", "pattern", "performs", "demonstrated", "effectively","salary",
        "benefit", "etc", "combination", "similar", "developer", "end", "expertise",
        "like", "good", "core", "spring", "slack", "e.g.", "highly", "learning", "performance", "deployment", "boot", "building",
        "client", "candidate", "job", "collaborate", "feature", "remote", "program", "quality",
        "insurance", "get", "engineer", "master", "opportunity", "across", "interview",
        "employee", "please", "take", "u", "review", "flexible" ,"closely", "medical", "email",
        "manager", "maintain", "synergisticit", "electrical", "minimum", "help", "infrastructure",
        "qualification", "leave", "participate", "supporting", "based", "startup", "comprehensive",
        "world", "continuously", "make", "share","growth", "ownership",
        "implementation", "mobile", "looking", "existing", "web", "also", "creating", "per",
        "jobseekers", "customer", "someone", "love", "important", "helped", "care",
        "fully", "know", "market", "assist", "test", "status", "eligible", "ensure", "may", "area", "vehicle",
        "company-paid", "history", "change", "part", "standard", "meet", "u.s.", "plan", "appropriate","success",
        "assigned", "specification", "document", "health", "apply", "schedule",
        "education", "create", "clearance", "without", "stakeholder", "pay", "functional", "relevant",
        "task", "collaborative","hour","united","duty", "relocation", "sponsorship", "state",
        "control", "manage", "dental" ,"organization", "scope", "day", "ensuring", "visa",
        "excellence","specific", "solve", "lead", "keep", "detail", "identify", "continuous","power",
        "global", "internal", "member", "able", "request" , "various", "operational", "attention", 
        "disability", "responsibility", "operation", "policy", "necessary" , "conduct", "workflow" ,
        "department", "analyst", "operating", "employer", "location", "external", "source", "etl",
        "offer", 


    ])

    # Remove stopwords and custom words
    stop_words = set(stopwords.words('english'))
    all_stop_words = stop_words.union(custom_stop_words)

    # Filter tokens: keep words with at least one alphanumeric character and not in stopwords
    filtered_tokens = [word for word in lemmatized_tokens if word not in all_stop_words and re.search(r'\w', word)]

    # Create less_filtered_tokens by removing periods, commas, "'s", and single character words
    less_filtered_tokens = [re.sub(r"\'s", '', re.sub(r'[.,]', '', word)) for word in tokens if len(word) > 1]

    # Save all plots to a single PDF file
    with PdfPages('processed_data/'+name_file+'_analysis.pdf') as pdf:
        frequency_analysis(filtered_tokens, 20, pdf)
        ngram_analysis(less_filtered_tokens, 2, 20, pdf)  # Bigrams
        ngram_analysis(less_filtered_tokens, 3, 20, pdf)  # Trigrams
        ngram_analysis(less_filtered_tokens, 4, 20, pdf)  # 
        ngram_analysis(less_filtered_tokens, 6, 20, pdf)  # 
        ngram_analysis(less_filtered_tokens, 8, 20, pdf)  #
        ngram_analysis(less_filtered_tokens, 12, 20, pdf)  #
        generate_word_cloud(' '.join(top_skills), 'Word Cloud of Top Skills', pdf)
        generate_word_cloud(' '.join(filtered_tokens),  'Word Cloud of Skills in Requirements', pdf)
        # skill_clustering(requirements)

