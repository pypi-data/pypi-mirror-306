
#***********************************************************************************************************
#*************************** WELCOME MESSAGE ****************************************************************
#***********************************************************************************************************

def seeline():
  print("**********************************************************")
  print("Seeline welcomes you ! Seeline is an innovative text analysis tool")
  print("**********************************************************")
  print()
  print("Contacts:")
  print()
  print("Dr Anna Sung - email: a.sung@chester.ac.uk")
  print("Prof Kelvin Leong - email: k.leong@chester.ac.uk")
  print()
  print("Available functions:")
  print("count, wordcloud, classify, ask, summary, emotion")
  print("The input file format should be in CSV")
  print()
  print("**********************************************************")


#***********************************************************************************************************
#*************************** WORD COUNT ****************************************************************
#***********************************************************************************************************


def count():
  # Step 1: Install necessary libraries (if not already installed)
  
  # Step 2: Import the required libraries
  import pandas as pd
  from collections import Counter
  import io
  from google.colab import files
  import nltk
  from nltk.util import ngrams
  import csv

  # Step 3: Function to perform word count analysis with n-grams
  def word_count_analysis(csv_file, text_column, n):
      # Read the CSV file into a pandas DataFrame
      df = pd.read_csv(csv_file)

      # Combine all the text data into a single string
      text_data = " ".join(df[text_column].astype(str).tolist())

      # Tokenize the text data (split into words)
      words = text_data.split()

      # Generate n-grams from the words
      n_grams = list(ngrams(words, n))

      # Perform n-gram count using the Counter class
      n_gram_count = Counter(n_grams)

      return n_gram_count

  # Step 4: Allow the user to upload the CSV file
  uploaded = files.upload()

  # Step 5: Perform word count analysis and display the results
  if len(uploaded) > 0:
      # Get the uploaded file name
      csv_file_name = list(uploaded.keys())[0]

      # Get the column name that contains text data
      text_column = input("Enter the column name containing text data: ")

      # Get the desired n-gram length from the user
      n = int(input("Enter the desired n-gram length (e.g., 2 for bigrams, 3 for trigrams, etc.): "))

      # Get the number of rules the user wants to generate
      num_rules = int(input("Enter the number of rules you want to generate: "))

      # Perform word count analysis with n-grams
      n_gram_count_result = word_count_analysis(io.BytesIO(uploaded[csv_file_name]), text_column, n)

      # Get the top n n-grams and their counts
      top_n_n_grams = n_gram_count_result.most_common(num_rules)

      # Display the top n n-grams and their counts
      print(f"\nTop {num_rules} {n}-grams:")
      for n_gram, count in top_n_n_grams:
          print(f"{' '.join(n_gram)}: {count}")

      # Save the top n n-grams and their counts to a CSV file
      output_file_name = f"top_{n}_grams.csv"
      with open(output_file_name, 'w', newline='') as csvfile:
          csv_writer = csv.writer(csvfile)
          csv_writer.writerow([f"Top {n}-grams", "Count"])
          for n_gram, count in top_n_n_grams:
              csv_writer.writerow([' '.join(n_gram), count])

      # Provide a link to download the CSV file
      print(f"\nResults saved to: {output_file_name}")
  else:
      print("No file uploaded.")



#***********************************************************************************************************
#*************************** WORD CLOUD****************************************************************
#***********************************************************************************************************

def wordcloud():
    def wordcloud_generator():
      from google.colab import files
      import pandas as pd
      import nltk
      from nltk.corpus import stopwords
      from nltk.tokenize import word_tokenize
      from wordcloud import WordCloud
      import matplotlib.pyplot as plt
      from sklearn.feature_extraction.text import CountVectorizer

      nltk.download('punkt')
      nltk.download('stopwords')

      # Step 1: Allow the user to browse and select the CSV file
      uploaded = files.upload()
      file_name = list(uploaded.keys())[0]

      # Step 2: Read the CSV file and preprocess the text data
      def preprocess_text(text):
          # Convert text to lowercase
          text = text.lower()
          # Tokenize the text
          words = word_tokenize(text)
          # Remove punctuation and non-alphabetic characters
          words = [word for word in words if word.isalpha()]
          # Remove stopwords
          stop_words = set(stopwords.words('english'))
          words = [word for word in words if word not in stop_words]

          return " ".join(words)

      def load_csv_data(file_path):
          df = pd.read_csv(file_path)
          return df

      def extract_keywords(text_list):
          vectorizer = CountVectorizer(max_features=100)
          X = vectorizer.fit_transform(text_list)
          keywords = vectorizer.get_feature_names_out()

          return keywords

      def generate_word_cloud(keywords):
          wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(keywords))

          plt.figure(figsize=(10, 5))
          plt.imshow(wordcloud, interpolation='bilinear')
          plt.axis("off")

          # Save the word cloud as a JPG image
          output_image_file = "word_cloud_output.jpg"
          plt.savefig(output_image_file)

          plt.show()

      # Main function
      data_frame = load_csv_data(file_name)

      # Get the column name containing the text data from the user
      text_column = input("Enter the column name containing the text data: ")

      # Assuming the column containing the text data is named 'text'
      text_data = data_frame[text_column].tolist()

      preprocessed_text_data = [preprocess_text(text) for text in text_data]

      keywords = extract_keywords(preprocessed_text_data)

      generate_word_cloud(keywords)

    # Call the function to start the word cloud generation process
    wordcloud_generator()



#***********************************************************************************************************
#*************************** CLASSIFICATION****************************************************************
#***********************************************************************************************************


def classify():
  # Step 2: Import necessary libraries
  import pandas as pd
  import torch
  from transformers import pipeline
  from google.colab import files

  # Step 3: Load the emotion analysis model for zero-shot classification
  classifier = pipeline("zero-shot-classification")

  # Step 4: Define a function to analyze emotions in the messages
  def analyze_emotions(messages, labels):
      emotions = []
      for msg in messages:
          result = classifier(msg, labels)
          emotion_label = result['labels'][0]
          emotions.append(emotion_label)
      return emotions

  # Step 5: Upload the CSV file
  print("Please upload the CSV file:")
  uploaded = files.upload()

  # Step 6: Get the uploaded file name
  file_name = list(uploaded.keys())[0]

  # Step 7: Read the CSV file into a DataFrame
  df = pd.read_csv(file_name)

  # Step 8: Display the columns and let the user select one
  print("Columns in the CSV file:")
  print(df.columns)

  selected_column = input("Enter the column name containing the messages for emotion analysis: ")

  # Step 9: Check if the selected column exists in the DataFrame
  if selected_column not in df.columns:
      print("Selected column does not exist in the CSV file.")
  else:
      # Step 10: Ask the user to define the classification labels
      label_list = input("Enter the classification labels (comma-separated): ").split(',')

      # Step 11: Analyze emotions and add results to the DataFrame
      emotions = analyze_emotions(df[selected_column], label_list)
      df['emotion'] = emotions

      # Step 12: Save the results to a new CSV file
      output_file_name = "output_emotions.csv"
      df.to_csv(output_file_name, index=False)

      print("Emotion analysis completed and results saved to the CSV file:", output_file_name)


#***********************************************************************************************************
#*************************** QA****************************************************************
#***********************************************************************************************************

def ask():
  # Step 2: Import necessary libraries
  import pandas as pd
  import torch
  from transformers import pipeline
  from google.colab import files

  # Step 3: Load the question-answering model
  question_answerer = pipeline("question-answering")

  # Step 4: Define a function to find answers to the user-defined questions
  def find_answers(messages, question):
      answers = []
      for msg in messages:
          result = question_answerer(context=msg, question=question)
          answer = result['answer']
          answers.append(answer)
      return answers

  # Step 5: Upload the CSV file
  print("Please upload the CSV file:")
  uploaded = files.upload()

  # Step 6: Get the uploaded file name
  file_name = list(uploaded.keys())[0]

  # Step 7: Read the CSV file into a DataFrame
  df = pd.read_csv(file_name)

  # Step 8: Display the columns and let the user select one
  print("Columns in the CSV file:")
  print(df.columns)

  selected_column = input("Enter the column name containing the messages for question answering: ")

  # Step 9: Check if the selected column exists in the DataFrame
  if selected_column not in df.columns:
      print("Selected column does not exist in the CSV file.")
  else:
      # Step 10: Ask the user to input the question
      question = input("Enter your question: ")

      # Step 11: Find answers to the user-defined question within the messages
      answers = find_answers(df[selected_column], question)
      df['answer'] = answers

      # Step 12: Save the results to a new CSV file
      output_file_name = "output_answers.csv"
      df.to_csv(output_file_name, index=False)

      print("Question answering completed and results saved to the CSV file:", output_file_name)



#***********************************************************************************************************
#*************************** SUMMARIZATION****************************************************************
#***********************************************************************************************************
 
def summary():
  # Step 2: Import necessary libraries
  import pandas as pd
  import torch
  from transformers import pipeline
  from google.colab import files

  # Step 3: Load the summarization model
  summarizer = pipeline("summarization")

  # Step 4: Define a function to summarize each message
  def summarize_messages(messages):
      summaries = []
      for msg in messages:
          result = summarizer(msg, max_length=100, min_length=30, do_sample=False)
          summary = result[0]['summary_text']
          summaries.append(summary)
      return summaries

  # Step 5: Upload the CSV file
  print("Please upload the CSV file:")
  uploaded = files.upload()

  # Step 6: Get the uploaded file name
  file_name = list(uploaded.keys())[0]

  # Step 7: Read the CSV file into a DataFrame
  df = pd.read_csv(file_name)

  # Step 8: Display the columns and let the user select one
  print("Columns in the CSV file:")
  print(df.columns)

  selected_column = input("Enter the column name containing the messages for summarization: ")

  # Step 9: Check if the selected column exists in the DataFrame
  if selected_column not in df.columns:
      print("Selected column does not exist in the CSV file.")
  else:
      # Step 10: Summarize each message
      summaries = summarize_messages(df[selected_column])
      df['summary'] = summaries

      # Step 11: Save the results to a new CSV file
      output_file_name = "output_summaries.csv"
      df.to_csv(output_file_name, index=False)

      print("Summarization completed and results saved to the CSV file:", output_file_name)



#***********************************************************************************************************
#*************************** EMOTION ***********************************************************************
#***********************************************************************************************************
 


def emotion():
  # Step 2: Import necessary libraries
  import pandas as pd
  import torch
  from transformers import pipeline
  from google.colab import files

  # Step 3: Load the emotion analysis model
  classifier = pipeline("sentiment-analysis")

  # Step 4: Define a function to analyze emotions in the messages
  def analyze_emotions(messages):
      emotions = []
      for msg in messages:
          result = classifier(msg)
          emotion_label = result[0]['label']
          emotions.append(emotion_label)
      return emotions

  # Step 5: Upload the CSV file
  print("Please upload the CSV file:")
  uploaded = files.upload()

  # Step 6: Get the uploaded file name
  file_name = list(uploaded.keys())[0]

  # Step 7: Read the CSV file into a DataFrame
  df = pd.read_csv(file_name)

  # Step 8: Display the columns and let the user select one
  print("Columns in the CSV file:")
  print(df.columns)

  selected_column = input("Enter the column name containing the messages for emotion analysis: ")

  # Step 9: Check if the selected column exists in the DataFrame
  if selected_column not in df.columns:
      print("Selected column does not exist in the CSV file.")
  else:
      # Step 10: Analyze emotions and add results to the DataFrame
      emotions = analyze_emotions(df[selected_column])
      df['emotion'] = emotions

      # Step 11: Save the results to a new CSV file
      output_file_name = "output_emotions.csv"
      df.to_csv(output_file_name, index=False)

      print("Emotion analysis completed and results saved to the CSV file:", output_file_name)
