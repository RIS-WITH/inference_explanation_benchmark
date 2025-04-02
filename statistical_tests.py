import os
import json
from collections import defaultdict
import pandas as pd
import statsmodels.api as sm 
from statsmodels.formula.api import ols 
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.anova import anova_lm

data_directory = "/home/bdussard/inference_explanation/dataset/evaluations"

def explore_and_store_data(base_dir):

    data_structure = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                
                relative_path = os.path.relpath(file_path, base_dir)
                parts = relative_path.split(os.sep)
                
                model, condition, question = parts[0], parts[1], parts[2]
                question_name = question.split("_")[1] + "_" + question.split("_")[2]
                
                with open(file_path, "r") as f:
                    file_data = json.load(f)
                    data_structure[model][condition][question_name].extend(file_data)
    return data_structure

def flatten_data(data_structure):
    flat_data = []
    for model, conditions in data_structure.items():
        for condition, questions in conditions.items():
            for question, answers in questions.items():
                for answer in answers:
                    flat_data.append({
                        "model": model,
                        "condition": condition,
                        "question": question.split("_")[0],
                        "complexity": question.split("_")[-1],
                        "question_id": answer["question_id"].split("_")[-1],
                        "is_correct": answer["is_correct"],
                        "score": answer["score"],
                        "missing_concepts": ", ".join(answer["missing_concepts"])
                    })
    return pd.DataFrame(flat_data)

answers_array = explore_and_store_data(data_directory)
df = flatten_data(answers_array)

# Step 1: group the data by question
df_grouped = df.groupby(["model", "condition", "complexity"]).agg(
    perc_correct=("is_correct", "mean"), 
    mean_score=("score", "mean"),
    median_score = ("score", "median"),      
    std_score=("score", "std"),
    #iqr_score=("score", "iqr")         
).reset_index()

print(df_grouped.head())

# Step 2: Perform Two-Way ANOVA for correctness and mean completeness according to complexity, on baseline condition
baseline_df = df_grouped[df_grouped["condition"] == "baseline"]

# ======== Correctness ======
model_perc_correct_baseline = ols("perc_correct ~ C(complexity) + C(model)", data=baseline_df).fit()
anova_perc_correct = sm.stats.anova_lm(model_perc_correct_baseline, typ=2)
print("\nTwo-Way ANOVA for perc_correct (Baseline Condition):\n", anova_perc_correct)
tukey_baseline_complexity = pairwise_tukeyhsd(baseline_df['perc_correct'], baseline_df['complexity'], alpha=0.05)
print("Post-hoc test for perc_correct (complexity):", tukey_baseline_complexity)

# ======== Mean Completeness ======
model_mean_baseline = ols("mean_score ~ C(complexity) + C(model)", data=baseline_df).fit()
anova_mean = sm.stats.anova_lm(model_mean_baseline, typ=2)
print("\Two-Way ANOVA for Mean score (Baseline Condition):\n", anova_mean)
tukey_baseline_complexity = pairwise_tukeyhsd(baseline_df['mean_score'], baseline_df['complexity'], alpha=0.05)
print("Post-hoc test for mean_score (complexity):", tukey_baseline_complexity)

# Step 3: Perform Three-Way ANOVA for correctness and mean completeness according to complexity/condition/model

# ======== Correctness ======
model_perc_correct_all = ols('perc_correct ~ C(condition) + C(complexity) + C(model)', data=df_grouped).fit()
anova_result = sm.stats.anova_lm(model_perc_correct_all, typ=3)
print("\nANOVA Results for perc_correct:", anova_result)
# Condition on perc_correct
tukey_condition = pairwise_tukeyhsd(df_grouped['perc_correct'], df_grouped['condition'], alpha=0.05)
print("Post-hoc test for perc_correct (condition):", tukey_condition)
# Complexity on perc_correct
tukey_complexity = pairwise_tukeyhsd(df_grouped['perc_correct'], df_grouped['complexity'], alpha=0.05)
print("Post-hoc test for perc_correct (complexity):", tukey_complexity)

# ======== Mean Completeness ======
model_mean_all = ols('mean_score ~ C(condition) + C(complexity) + C(model)', data=df_grouped).fit()
anova_result = anova_lm(model_mean_all, typ=3)
print("\nANOVA Results for mean_score:", anova_result)
# Condition on mean_score
tukey_condition = pairwise_tukeyhsd(df_grouped['mean_score'], df_grouped['condition'], alpha=0.05)
print("Post-hoc test for mean_score (condition):", tukey_condition)
# Complexity on mean_score
tukey_complexity = pairwise_tukeyhsd(df_grouped['mean_score'], df_grouped['complexity'], alpha=0.05)
print("Post-hoc test for mean_score (complexity):", tukey_complexity)


