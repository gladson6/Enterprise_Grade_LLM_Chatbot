from sentence_transformers import SentenceTransformer

print("Downloading the sentence-transformer model...")
print("This may take a few minutes...")

model_name = 'sentence-transformers/all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

# Create a new directory and save the model there
model.save('./local_model')

print("\n✅ Model downloaded and saved to the './local_model' directory.")