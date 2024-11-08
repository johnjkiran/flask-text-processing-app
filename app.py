from flask import Flask, render_template, request, redirect, url_for
import nltk
from nltk.corpus import stopwords
import random
from nltk.corpus import wordnet

# Ensure necessary NLTK resources are downloaded
# nltk.download('stopwords')
# nltk.download('wordnet')

app = Flask(__name__)

# Global variables to store data
data = None
processed_data = None
augmented_data = None

def preprocess_text(file_path):
    stop_words = set(stopwords.words('english'))
    with open(file_path, 'r') as file:
        lines = file.readlines()
    processed_lines = []
    for line in lines:
        line = line.lower()
        words = line.split()
        filtered_words = [word for word in words if word not in stop_words]
        processed_lines.append(' '.join(filtered_words))
    return processed_lines

def synonym_replacement(sentence, n):
    words = sentence.split()
    num_replacements = min(n, len(words))
    replaced_indices = set()
    for _ in range(num_replacements):
        while True:
            word_to_replace = random.choice(words)
            index = words.index(word_to_replace)
            if index not in replaced_indices:
                synonyms = wordnet.synsets(word_to_replace)
                if synonyms:
                    synonym = random.choice(synonyms[0].lemmas()).name()
                    words[index] = synonym
                    replaced_indices.add(index)
                break
    return ' '.join(words)

def random_word_insertion(sentence, n):
    words = sentence.split()
    for _ in range(n):
        random_word = random.choice(words)
        insert_position = random.randint(0, len(words))
        words.insert(insert_position, random_word)
    return ' '.join(words)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global data
    file = request.files['file']
    if file:
        file.save('sample.txt')
        with open('sample.txt', 'r') as f:
            data = f.readlines()
    return redirect(url_for('show_data'))

@app.route('/show_data')
def show_data():
    print("Data to show:", data)  # Debugging line
    return render_template('preprocess.html', data=data)

@app.route('/preprocess', methods=['POST'])
def preprocess():
    global processed_data
    processed_data = preprocess_text('sample.txt')
    print("Processed Data:", processed_data)  # Debugging line
    return render_template('augment.html', data=processed_data)

@app.route('/augment', methods=['POST'])
def augment():
    global augmented_data
    augmented_data = []
    for sentence in processed_data:
        augmented_sentence = synonym_replacement(sentence, n=2)
        augmented_sentence = random_word_insertion(augmented_sentence, n=2)
        augmented_data.append(augmented_sentence)
    
    # Render the final output template
    return render_template('final_output.html', data=augmented_data)

if __name__ == '__main__':
    app.run(debug=True)
