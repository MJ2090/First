import os
import pandas as pd
import tiktoken
import openai
import numpy as np
from openai.embeddings_utils import distances_from_embeddings, cosine_similarity
import df

################################################################################
### Step 12
################################################################################

def create_context(question, df, max_len=1800):
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    # Get the embeddings for the question
    q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

    # Get the distances from the embeddings
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')

    returns = []
    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long
    for i, row in df.sort_values('distances', ascending=True).iterrows():

        # Add the length of the text to the current length
        cur_len += row['n_tokens'] + 4

        # If the context is too long, break
        if cur_len > max_len:
            break

        # Else add it to the text that is being returned
        returns.append(row["text"])

    # Return the context
    return "\n\n###\n\n".join(returns)

def answer_question(
        df,
        model="text-davinci-003",
        question="Am I allowed to publish model outputs to Twitter, without a human review?",
        max_len=1800,
        debug=False,
        max_tokens=150,
        stop_sequence=None
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        df,
        max_len=max_len,
    )
    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # Create a completions using the questin and context
        response = openai.Completion.create(
            prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model,
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print(e)
        return ""

################################################################################
### Step 13
################################################################################


def run_it():
    my_df = df.get_df()
    qs = ["What day is it?",
          "What is Done?",
          "What is ADHD?",
          "How to treat ADHD?",
          "How many people have ADHD?",
          "Where are you",
          "How do patients like Done.?"]
    for q in qs:
        print("Question:")
        print(q)
        print("Answer:")
        print(answer_question(my_df, question=q))
        print("=======================")


def run_it_2():
    my_df = df.get_df_2()
    qs = ["What day is it?",
          "What is Done?",
          "What is ADHD?",
          "How to treat ADHD?",
          "How many people have ADHD?",
          "Where are you",
          "How do patients like Done.?"]
    for q in qs:
        print("Question:")
        print(q)
        print("Answer:")
        print(answer_question(my_df, question=q))
        print("=======================\n\n\n")



run_it_2()