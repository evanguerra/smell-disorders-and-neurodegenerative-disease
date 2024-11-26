import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline, Trainer, TrainingArguments
from datasets import load_dataset, load_metric
import numpy as np
from sklearn.metrics import classification_report


# Load PubTator-formatted dataset
# Assuming the data is already in PubTator format and stored in a compatible format (NER tags, tokens)

def load_pubtator_dataset(pubtator_file):
    # Load your data here from PubTator format, this function is a placeholder for loading data
    # Return it in the format:
    #   tokens = [['token1', 'token2', ...], ...]
    #   labels = [['B-ENTITY', 'O', 'O', 'B-ENTITY', ...], ...]
    tokens = [['This', 'is', 'an', 'example'], ['Another', 'sentence']]
    labels = [['O', 'O', 'O', 'B-DISEASE'], ['O', 'O']]
    return tokens, labels


# Load tokens and labels
tokens, labels = load_pubtator_dataset("your_pubtator_file.txt")

# Tokenizer and model
model_name = "bert-base-cased"  # You can choose other models like BERT, GPT, etc.
tokenizer = AutoTokenizer.from_pretrained(model_name)


# Prepare data
def tokenize_and_align_labels(tokens, labels):
    tokenized_inputs = tokenizer(tokens, truncation=True, is_split_into_words=True, padding=True)

    label_ids = []
    for i, label in enumerate(labels):
        word_ids = tokenized_inputs.word_ids(batch_index=i)  # Map tokens to their respective word.
        previous_word_idx = None
        label_ids.append([])
        for word_idx in word_ids:
            if word_idx is None:
                label_ids[i].append(-100)
            elif word_idx != previous_word_idx:  # First token of the word
                label_ids[i].append(label[word_idx])
            else:
                label_ids[i].append(-100)  # Subword tokens get -100
            previous_word_idx = word_idx

    return tokenized_inputs, label_ids


# Tokenize and align
tokenized_inputs, label_ids = tokenize_and_align_labels(tokens, labels)

# Define NER model
model = AutoModelForTokenClassification.from_pretrained(model_name, num_labels=3)  # Adjust number of labels

# Load metric
metric = load_metric("seqeval")


# Define compute metrics function for evaluation
def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    true_labels = [[label for label in label if label != -100] for label in labels]
    true_predictions = [
        [p for (p, l) in zip(pred, label) if l != -100]
        for pred, label in zip(predictions, labels)
    ]

    results = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }


# Training arguments for fine-tuning the model
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Trainer class for handling training and evaluation
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_inputs,
    eval_dataset=tokenized_inputs,
    compute_metrics=compute_metrics,
)

# Train model (Few-shot learning)
trainer.train()

# Evaluate model (Few-shot)
results_few_shot = trainer.evaluate()
print("Few-Shot Results:", results_few_shot)

# Zero-shot NER using Hugging Face pipeline (if you don't want to train the model)
zero_shot_ner = pipeline("ner", model=model_name, tokenizer=model_name)
zero_shot_results = zero_shot_ner("This is an example sentence with anosmia and Parkinson's disease.")

print("Zero-Shot NER Results:", zero_shot_results)
