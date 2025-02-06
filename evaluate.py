import os
import json
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import math
from fitter import Fitter, get_common_distributions, get_distributions
from scipy import stats
from scipy.stats import gamma
from sklearn.neighbors import KernelDensity
from scipy.stats import pearsonr, ttest_ind, spearmanr
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

pd.options.mode.chained_assignment = None

# Path to the dataset directory
data_dir = "/home/bdussard/inference_explanation/dataset/evaluations"
data_dir2 = "/home/bdussard/inference_explanation/dataset_fix_correctness/evaluations"




def get_question(data_structure, model, condition, question, variation_id):
    # Navigate to the specific variation
    answers = data_structure.get(model, {}).get(condition, {}).get(question, [])
    
    # Find the question with the specified variation_id
    for answer in answers:
        if answer["question_id"] == variation_id:
            return answer
    return None 

def explore_and_store_data(base_dir):
    # Structure to hold the data
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

# Run the function to populate the structure
answers_array = explore_and_store_data(data_dir)

model = "llama3.1:8b"
condition = "baseline"
question = "grasp_easy"
question_id = "a_grasp_easy_1b"

answers_correctness = explore_and_store_data(data_dir2)
# question_data = get_question(data_structure, model, condition, question, question_id)

# if question_data:
#     print("Question Data:", json.dumps(question_data, indent=4))
# else:
#     print(f"Question {question_id} not found in {model}/{condition}/{question}.")
    
# Example: Accessing data for a specific model, condition, and variation
# model = "llama3.1:8b", condition = "baseline", variation = "a_grasp_easy_b"
example_data = answers_array["llama3.1:8b"]["baseline"]["grasp_easy"]

def compute_stats(data):
    total_questions = len(data)
    correct_answers = sum(1 for answer in data if answer["is_correct"])
    average_score = sum(answer["score"] for answer in data) / total_questions if total_questions > 0 else 0

    missing_concepts_count = defaultdict(int)
    for answer in data:
        for concept in answer["missing_concepts"]:
            missing_concepts_count[concept] += 1

    return {
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "average_score": average_score,
        "missing_concepts_count": dict(missing_concepts_count)
    }

# Example usage of compute_stats
stats = compute_stats(example_data)
#print("Stats:", json.dumps(stats, indent=4))

models = ["llama3.2:3b", "llama3.1:8b", "gemma2:2b", "gemma2:9b", "mistral-nemo:12b", "mistral-small:22b"]

conditions = ["baseline", "rule", "shuffle"]
questions = ["grasp", "lift", "push", "perceive"]
difficulties = ["easy", "medium", "hard"]

scores = []
for model in models:
    for question in questions:
        for difficulty in difficulties:         
            for condition in conditions:
                data = answers_array[model][condition][question+"_"+difficulty]
                stats = compute_stats(data)
                # print("For m=", model, " ,q=", question, " ,d=", difficulty, " ,c=", condition)
                # print(" Stats:", json.dumps(stats, indent=4))
                id = "_".join([model, question, difficulty, condition])
                scores.append([id, stats['average_score']])
   
# Flatten the data structure into a DataFrame for plotting
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

def sturge_optimal_bins(data: np.array) -> int:
    """ Sturge's rule for optimal bin selection
    Parameters: 
        data (np.array) - a one-dimensional array with data
    Returns:
        nbins (int) - number of bins
    """
    assert data.ndim == 1
    n = data.size
    width = 1.0 + np.log2(n)
    
    nbins = math.ceil((data.max() - data.min()) / width)
    nbins = max(1, nbins)
    
    return nbins

df = flatten_data(answers_array)

df_correctness = flatten_data(answers_correctness)
#df_correctness.to_csv("/home/bdussard/inference_explanation/df_correctness.csv")

#print(df.head(), df_correctness.head())


def generate_distplot(dataframe, model, condition = "baseline", difficulties = ["easy", "medium", "hard"]):
    datas = []
    for difficulty in difficulties:
        chosen_data = dataframe[(dataframe["model"] == model) & (dataframe["complexity"] == difficulty) & (dataframe["condition"] == condition)]["score"]
        datas.append(chosen_data*100)

def generate_histplot(dataframe, models, difficulties):
    colors = ["green", "orange", "red"]
    complexity_colors = {"easy": "green", "medium": "orange", "hard": "red"}
    fig, axes = plt.subplots(2,3)

    for model, ax in zip(models, axes.flatten()):
        for i in range(0, len(difficulties)):
            chosen_data = dataframe[(dataframe["model"] == model) 
                            & (dataframe["condition"] == "baseline")
                            & (dataframe["complexity"] == difficulties[i])]
                            # & (dataframe["question"] == 'perceive')]
            chosen_data["score"]= chosen_data["score"]*100
            correctness_rate = len(chosen_data[chosen_data["is_correct"] == True])/len(chosen_data)
            
            custom_clip = (min(chosen_data["score"]), max(chosen_data["score"]))
            custom_kde_kws={"bw_adjust": 2, "cut": 2, "clip": (custom_clip)}
            
            
            if(difficulties[i]=="easy"):
                nb_items = 10
            elif(difficulties[i]=="medium"):
                nb_items = 14
            elif(difficulties[i]=="hard"):
                nb_items = 17
            custom_binwidth = 100 / nb_items
                
            sns.histplot(data=chosen_data, x="score", kde=True, binwidth=custom_binwidth, binrange=(-custom_binwidth/2, 100 + custom_binwidth/2), legend=True, stat='count', 
                         ax=ax, color=colors[i], kde_kws=custom_kde_kws, common_norm=True)
            
            ax.axvline(x = correctness_rate*100, color = colors[i], linestyle = 'dashed')
            ax.set_title(model)
            ax.set_ylim(0, len(chosen_data))
            ax.set_xlim(0, 105)
            
            hist_legend = [mpatches.Patch(color=color, alpha=0.5, label=complexity) for complexity, color in complexity_colors.items()]
            legend_hist = ax.legend(handles=hist_legend, title="Complexity level", loc="upper left", fontsize=8, title_fontsize=8)

            line_legend = [mlines.Line2D([], [], color=color, linestyle="--", linewidth=2, label=complexity) for complexity, color in complexity_colors.items()]
            legend_lines = ax.legend(handles=line_legend, title="Correctness rate", loc="center left", fontsize=8, title_fontsize=8)
            
            ax.add_artist(legend_hist)

        plt.xlabel("Completion Score (%)")
        plt.ylabel("Frequency")
    fig.suptitle("Completion Score distribution for all models on baseline condition")
    plt.tight_layout()
    plt.show()

def generate_average_histplot(dataframe, models, condition_colors = {"baseline": "blue", "rule": "orange", "shuffle": "red"}):
    fig, axes = plt.subplots(2,3)
    #fig.suptitle("Completion Score distribution over all 6 models")
    
    for model, ax in zip(models, axes.flatten()):
        for condition, color in condition_colors.items():
            chosen_data = dataframe[(dataframe["model"] == model) 
                        & (dataframe["condition"] == condition)]
        
            chosen_data["score"]= chosen_data["score"]*100
            correctness_rate = len(chosen_data[chosen_data["is_correct"] == True])/len(chosen_data)
            
            custom_clip = (min(chosen_data["score"]), max(chosen_data["score"]))
            custom_kde_kws={"bw_adjust": 1.5, "cut": 2, "clip": (custom_clip)}
            custom_binwidth = 100/((10+14+17)/3)
            
            sns.histplot(data=chosen_data, x="score", kde=True, binwidth=custom_binwidth, binrange=(-custom_binwidth/2, 100 + custom_binwidth/2), color = color, legend=True, 
                        stat='count', ax=ax, kde_kws=custom_kde_kws, common_norm=True)
        
            ax.axvline(x = correctness_rate*100, linestyle = 'dashed', color = color)
            ax.set_title(model)
            ax.set_ylim(0, 100)
            ax.set_xlim(0, 105)
            ax.set_xlabel("Completion Score (%) - (3s CoT)")
            ax.set_ylabel("Frequency")

        hist_legend = [mpatches.Patch(color=color, alpha=0.5, label=condition) for condition, color in condition_colors.items()]
        legend_hist = ax.legend(handles=hist_legend, title="Condition", loc="upper left", fontsize=10, title_fontsize=10,  bbox_to_anchor=(0, 1))

        line_legend = [mlines.Line2D([], [], color=color, linestyle="--", linewidth=2, label=condition) for condition, color in condition_colors.items()]
        legend_lines = ax.legend(handles=line_legend, title="Correctness rate", loc="upper left", fontsize=10, title_fontsize=10, bbox_to_anchor=(0, 0.82))
        
        ax.add_artist(legend_hist)
    plt.subplots_adjust(wspace=0.15, hspace=0.2)
    #plt.tight_layout()
    plt.show()

def generate_histplot_all_models_single_plot(dataframe, models, condition = "baseline"):
    
    models_colored = {"llama3.2:3b": 'green',
                 "gemma2:2b": 'red',
                 "llama3.1:8b" :'blue',
                 "gemma2:9b": 'purple',
                 "mistral-nemo:12b": 'orange',
                 "mistral-small:22b": 'brown'}
    
    colors = sns.husl_palette(len(models), l=.5)
    fig, ax = plt.subplots(figsize=(7, 5))
    
    for model, color in models_colored.items():
        chosen_data = dataframe[(dataframe["model"] == model) 
                        & (dataframe["condition"] == condition)]
                        # & (dataframe["question"] == 'perceive')]
        chosen_data["score"]= chosen_data["score"]*100
        correctness_rate = len(chosen_data[chosen_data["is_correct"] == True])/len(chosen_data)
        
        custom_clip = (min(chosen_data["score"]), max(chosen_data["score"]))
        custom_kde_kws={"bw_adjust": 1.5, "cut": 2, "clip": (custom_clip)}
        custom_binwidth = 100/((10+14+17)/3)
        #bins = range(-custom_binwidth/2, 100 + custom_binwidth/2, custom_binwidth)
        sns.histplot(data=chosen_data, x="score", kde=True, binwidth=custom_binwidth, 
                     binrange=(-custom_binwidth/2, 100 + custom_binwidth/2), legend=True, stat='count', 
                     kde_kws=custom_kde_kws, common_norm=True, color = color, multiple="stack",
                     alpha=0, element="bars", edgecolor="white")
        ax.axvline(x = correctness_rate*100, linestyle = 'dashed', color = color, lw = 3)
        # sns.distplot(chosen_data["score"], ax=ax, kde=True, hist=False, fit=None,
        #              bins = range(int(-custom_binwidth/2), 100 + int(custom_binwidth/2), int(custom_binwidth)), 
        #              kde_kws=custom_kde_kws, color = color, norm_hist= False)

        # sns.kdeplot(data=chosen_data["score"], 
        #             ax=ax, 
        #             bw_adjust=1.5,  # Adjust bandwidth if needed
        #             clip= custom_clip,
        #             cut=2,
        #             color=color, 
        #            linewidth=2)
        #sns.displot(data=chosen_data, x="score", kind="kde", legend=True, stat='count', kde_kws=custom_kde_kws, common_norm=True, color = color, multiple="stack" )
    # ======== generate legends ========= 
    plt.xlabel("Completion Score (%)")
    plt.ylabel("Count")
    
    hist_legend = [mpatches.Patch(color=color, alpha=0.5, label=model) for model, color in models_colored.items()]
    legend_hist = ax.legend(handles=hist_legend, title="Complexity level", loc="upper left", fontsize=10, title_fontsize=10)

    line_legend = [mlines.Line2D([], [], color=color, linestyle="--", linewidth=2, label=model) for model, color in models_colored.items()]
    legend_lines = ax.legend(handles=line_legend, title="Correctness rate", loc="center left", fontsize=10, title_fontsize=10)
    
    ax.add_artist(legend_hist)
    plt.tight_layout()
    plt.show()

# generate_average_histplot(df, ["llama3.1:8b"], conditions)
# generate_average_histplot(df_correctness, ["llama3.1:8b"], conditions)
# ==================== 1 model on baseline condition with all 4 questions ================
#generate_distplot(df, model="llama3.2:3b")

# ==================== 6 subplots with each difficulty level ================
models_reordered = ["llama3.2:3b", "gemma2:2b", "llama3.1:8b", "gemma2:9b", "mistral-nemo:12b", "mistral-small:22b"]

models_colored = {"llama3.2:3b": 'green',
                 "gemma2:2b": 'red',
                 "llama3.1:8b" :'blue',
                 "gemma2:9b": 'purple',
                 "mistral-nemo:12b": 'orange',
                 "mistral-small:22b": 'brown'}

new_models = ["llama3.2:3b", "gemma2:2b", "llama3.1:8b", "gemma2:9b", "mistral-nemo:12b", "mistral-small:22b"]
# ======== generate 6 subplots with each model and average of difficulty levels ===
#generate_average_histplot(df_correctness, new_models, conditions)
condition_colors = {"baseline": "blue", "rule": "orange"}
generate_average_histplot(df_correctness, new_models, condition_colors)
condition_colors = {"baseline": "blue", "shuffle": "red"}
generate_average_histplot(df_correctness, new_models, condition_colors)

# ======== generate 1 plot with each model and average of difficulty levels ===
# generate_histplot_all_models_single_plot(df, models_reordered, "baseline")
# generate_histplot_all_models_single_plot(df, models_reordered, "rule")
# generate_histplot_all_models_single_plot(df, models_reordered, "shuffle")

# ======== generate 6 subplots with each model and each difficulty level, on baseline ===
generate_histplot(df_correctness, new_models, ["easy", "medium", "hard"])

def compute_correlations(dataframe, models):
    for model in models:
        print("Computing correlation model ", model)
        
        chosen_data = dataframe[(dataframe["condition"] == "rule")
                                & (dataframe["model"] == model)]
                        #& (dataframe["question"] == 'lift')]
        chosen_data["score"]= chosen_data["score"]*100

        data = pd.DataFrame({
            'correctness': chosen_data["is_correct"],
            'completion_rate': chosen_data["score"]
        })
        #print(data['correctness'])
        # Step 1: Convert correctness to numeric (True -> 1, False -> 0)
        data['correctness_numeric'] = data['correctness'].astype(int)
        
        #sns.scatterplot(x='correctness_numeric', y='completion_rate', data=data)
        #sns.boxplot(x='correctness', y='completion_rate', data=data)
        sns.violinplot(x='correctness', y='completion_rate', data=data)
        plt.xticks([0, 1], ['False', 'True'])
        plt.title("Scatter Plot: Correctness vs Completion Rate")
        plt.xlabel("Correctness (True=1, False=0)")
        plt.ylabel("Completion Rate")
        plt.show()
        
        #print(data['correctness_numeric'])
        # Step 2: Focus on the rows where correctness is True
        true_data = data[data['correctness'] == True]
        false_data = data[data['correctness'] == False]
        
        # Check variability (Standard Deviation) for True and False cases
        true_data_variability = true_data['completion_rate'].std()
        false_data_variability = false_data['completion_rate'].std()

        print(f"Standard Deviation for True values: {true_data_variability}")
        print(f"Standard Deviation for False values: {false_data_variability}")
        
        # If the standard deviation is 0, correlation might not work
        if true_data_variability == 0 or false_data_variability == 0:
            print("One or both groups have no variability, correlation may not be meaningful.")

        # Compute Spearman correlation (for robustness against small sample sizes or constant values)
        spearman_corr, spearman_p_value = spearmanr(true_data['correctness_numeric'], true_data['completion_rate'])
        print(f"Spearman Correlation for True values: {spearman_corr:.4f} (p-value: {spearman_p_value:.4f})")

        # Step 3: Correlation (if comparing True values with their corresponding completion rates)
        # Treat True as 1 and compare with completion_rate
        # true_corr, true_p_value = pearsonr(true_data['correctness_numeric'], true_data['completion_rate'])
        # print(f"Pearson Correlation for True values: {true_corr:.4f} (p-value: {true_p_value:.4f})")

        # Step 4: Alternatively, compare the means using a t-test
        # We can test if the completion rates for True and False are statistically different
        t_stat, t_p_value = ttest_ind(true_data['completion_rate'], false_data['completion_rate'])
        print(f"T-test result: t-statistic = {t_stat:.4f}, p-value = {t_p_value:.4f}")

def generate_barplot(dataframe, models, conditions, metric = "completion"):
    # data = pd.DataFrame({
    # "Model": ["llama3.2:3b", "gemma2:2b", "llama3.1:8b", "gemma2:9b", "mistral-nemo:12b", "mistral-small:22b"] * 2,
    # "Completion Rate": [75, 80, 85, 90, 70, 65, 82, 87, 78, 92, 75, 68],  # Example completion rates
    # "Category": ["Baseline"] * 6 + ["Rule"] * 6  # Two categories per model
    # })
    
    # Set colors for categories
    palette = {"Baseline": "blue", "Rule": "yellow"}
    grouped_data = dataframe.groupby(["model", "condition"])["score"].median().reset_index()
    # metrics :
    #IQR
    iqr_data = df.groupby("model")["score"].quantile(0.75) - df.groupby("model")["score"].quantile(0.25)
    print(iqr_data)
    iqr_data_conditions = df.groupby(["model", "condition"])["score"].quantile(0.75) - df.groupby(["model", "condition"])["score"].quantile(0.25)
    print(iqr_data_conditions)
    # grouped_data = grouped_data["score"]*100
    grouped_data.score *= 100
   
    grouped_data = grouped_data.drop(grouped_data[grouped_data['condition'] == 'shuffle'].index)
    print(grouped_data)
    plt.figure(figsize=(10, 6))
    for model in models:
        for condition in conditions:
            
            #grouped_data = df.groupby(["model", "condition"])["score"].median().reset_index()
            # chosen_data = dataframe[(dataframe["model"] == model) 
            #                 & (dataframe["condition"] == condition)]
            score_value = grouped_data.loc[(grouped_data["model"] == model) & (grouped_data["condition"] == condition), "score"].values[0]
            #print("model :", model, "condition", condition, "mean score : ", score_value)
           
            # if(metric == "correctness"):
            #     correctness_rate = len(chosen_data[chosen_data["is_correct"] == True])/len(chosen_data)
            # else:
            #     chosen_data["score"]= chosen_data["score"]*100
            #     average_score = chosen_data["score"].median()
            #     rounded_average_score = round(average_score, 2)
            #     std_score = chosen_data["score"].std()
            #     rounded_std_score = round(std_score, 2)
            
            ax = sns.barplot(
            data=grouped_data,
            x="model",
            y="score",
            hue="condition",
            # palette=bar_colors,
            # edgecolor=[edge_colors[c] for c in grouped_data["condition"]],  # Custom edge colors
            linewidth=2  # Thin borders
        )

            # Add values inside the bars
            for bar in ax.containers:
                ax.bar_label(bar, fmt="%.1f", label_type="center", fontsize=12, color="black")

    # Format plot
    plt.title("Model Completion Rates")
    plt.xlabel("Model")
    plt.ylabel("Completion Rate (%)")
    plt.ylim(0, 100)  # Ensure proper scaling
    # plt.xticks(rotation=45)  # Rotate model names for better readability
    plt.legend(title="Category")  # Display legend

    plt.show()

generate_barplot(df_correctness, new_models, ["baseline", "rule"])

def test_function(dataframe, models):

    grouped_data_completion = dataframe.groupby(["model", "condition"])["score"].median().reset_index()
    grouped_data_completion = grouped_data_completion.drop(grouped_data_completion[grouped_data_completion['condition'] == 'shuffle'].index)
    
    grouped_data_correct = dataframe.groupby(["model", "condition"])["is_correct"].agg(
                                    total_correct="sum",  # Count of True values
                                    total_samples="count"  # Total number of rows in each group
                                    )

    # Calculate correctness rate
    grouped_data_correct["correctness_rate"] = (grouped_data_correct["total_correct"] / grouped_data_correct["total_samples"])*100

    grouped_data_correct = grouped_data_correct.reset_index()
    grouped_data_correct = grouped_data_correct.drop(grouped_data_correct[grouped_data_correct['condition'] == 'shuffle'].index)
    grouped_data_correct = grouped_data_correct.drop(columns=["total_correct", "total_samples"])
    
    print(grouped_data_correct)
    
    # df = grouped_data[grouped_data['condition'] == 'baseline']
    # print("baseline values = ", df)
    
    data_baseline = {
        "Model": [],
        "Completion Score": [],
        "Correct Score": [],
        "Color": ["lightgray", "lightblue", "orangered", "pink", "purple"],
        "EdgeColor": ["black", "blue", "brown", "red", "purple"]
    }
    
    for model in models:
        data_baseline["Model"].append(model)
        data_baseline["Completion Score"].append(grouped_data[grouped_data['condition'] == 'baseline' & grouped_data['model'] == model])
    
    data_rule = {
        "Model": ["gemma2:2b", "llama3.2:3b", "llama3.1:8b", "gemma2:9b", "mistral-nemo:12b", "mistral-small:22b"],
        "Score": [87.3, 82.5, 29.4, 30.2, 22.6],
        "Color": ["lightgray", "lightblue", "orangered", "pink", "purple"],
        "EdgeColor": ["black", "blue", "brown", "red", "purple"]
    }
    
    df = pd.DataFrame(data)

    # Create figure
    fig, ax = plt.subplots(figsize=(6, 5))

    # Create bar plot
    bars = sns.barplot(
        data=df, 
        x="Model", 
        y="Score", 
        palette=list(df["Color"]), 
        edgecolor=list(df["EdgeColor"]), 
        linewidth=2
    )

    # Add value labels inside bars, rotated
    for bar, label in zip(bars.patches, df["Score"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 5, f"{label:.1f}", 
                ha="center", va="center", fontsize=12, color="black", fontweight="normal")

    # Axis labels and title
    ax.set_ylabel("Median Completion Score (IQR) (%)", fontsize=14, fontweight="bold")
    # ax.set_xlabel("Model")
    ax.set_title("Completion Score Comparison", fontsize=14, fontweight="bold")

    # Adjust y-axis limits and grid style
    ax.set_ylim(0, 100)  # Match scale
    ax.yaxis.grid(True, linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)

    # Custom x-axis labels with bold formatting
    plt.xticks(fontsize=12, fontweight="bold")

    # Remove top and right spines
    sns.despine()
    ax.text(-0.5, -1, "Model", fontsize=12, fontweight="bold", ha="left", va="top")
    plt.show()

#test_function(df_correctness, new_models)
#compute_correlations(df, models_reordered)

# single model, 3 levels, baseline condition
# model_name = "gemma2:9b"
# for difficulty in difficulties:
#     chosen_data = df[(df["model"] == model_name) 
#                      & (df["condition"] == "baseline" ) 
#                      & (df["complexity"] == difficulty )]
#     sns.histplot(data=chosen_data, x="score", kde=True, bins=20, legend=True, stat='count')
# plt.title("Score Distribution for " + model_name + " on baseline condition")
# plt.xlabel("Completion Score (%)")
# plt.ylabel("Frequency")
# plt.legend(title="Complexity level", loc='upper right', labels = difficulties) 
# plt.show()

# ========== Baseline condition, comparison between models on difficulty levels
# fig, axes = plt.subplots(1,3)
# for difficulty, ax in zip(difficulties, axes.flatten()):
#     for model in models:
#         chosen_data = df[(df["model"] == model) 
#                         & (df["condition"] == "shuffle") 
#                         & (df["complexity"] == difficulty)]
#         sns.histplot(data=chosen_data, x="score", kde=True, bins=10, legend=True, stat='density', ax=ax)
#         ax.set_title(difficulty + " condition")
#         ax.legend(title="Complexity level", loc='upper left', labels = difficulties)
#     plt.xlabel("Completion Score (%)")
#     plt.ylabel("Frequency")
#     plt.legend(title="Models", loc='upper left', labels = models) 
# plt.tight_layout()
# plt.show()

def get_chosen_data(dataframe, model, condition, difficulty, question_id):
    # print("getting data for ", model, condition, difficulty, question_id)
    df = get_model_data(dataframe, model)
    df = get_condition_data(df, condition)
    df = get_difficulty_data(df, difficulty)
    df = get_question_data(df, question_id)
    return df
        
def get_condition_data(dataframe, condition):
    if(condition != None):
        chosen_data = dataframe[(dataframe["condition"] == condition)]
    else:
        chosen_data = dataframe
    return chosen_data

def get_model_data(dataframe, model):
    if(model != None):
        chosen_data = dataframe[(dataframe["model"] == model)]
    else:
        chosen_data = dataframe
    return chosen_data

def get_difficulty_data(dataframe, difficulty):
    if(difficulty != None):
        chosen_data = dataframe[(dataframe["complexity"] == difficulty)]
    else:
        chosen_data = dataframe
    return chosen_data

def get_question_data(dataframe, question_id):
    if(question_id != None):
        chosen_data = dataframe[(dataframe["question"] == question_id)]
    else:
        chosen_data = dataframe
    return chosen_data

def compute_scoring_table(dataframe, models, conditions = ["baseline", "rule", "shuffle"], 
                          difficulties = ["easy", "medium", "hard"], question_id = None,
                          metric_completion = "mean"):
    df_results = pd.DataFrame(columns=['Model', 'Easy score', 'Easy correct', 'Medium score', 'Medium correct', 'Hard score', 'Hard correct'])
    df_results['Model'] = models

    for i in range(0, len(models)):
        for difficulty in difficulties:
            for condition in conditions:
                chosen_data = get_chosen_data(dataframe, models[i], condition, difficulty, question_id)
                
                average_score = chosen_data["score"].mean()
                rounded_average_score = round(average_score, 2)
                std_score = chosen_data["score"].std()
                rounded_std_score = round(std_score, 2)
                
                correctness_rate = len(chosen_data[chosen_data["is_correct"] == True])/len(chosen_data)
                rounded_correctness_rate = round(correctness_rate, 2)

                if(difficulty == "easy"):
                    df_results["Easy score"][i] = str(rounded_average_score) + "(± " + str(rounded_std_score) + ")"
                    df_results["Easy correct"][i] = rounded_correctness_rate
                elif(difficulty == "medium"):
                    df_results["Medium score"][i] = str(rounded_average_score) + "(± " + str(rounded_std_score) + ")"
                    df_results["Medium correct"][i] = rounded_correctness_rate
                else:
                    df_results["Hard score"][i] = str(rounded_average_score) + "(± " + str(rounded_std_score) + ")"
                    df_results["Hard correct"][i] = rounded_correctness_rate
    if(question_id == None):
        print("Results for all questions on condition :", condition)
    else:
        print("Results for question :", question_id, " on condition :", condition)
    print(df_results)

def compare_scores(data_old, data_new, models, questions = ["grasp", "lift", "push", "perceive"]):
    for model in models:
        print("===== Average: ")
        print("- OLD")
        compute_scoring_table(data_old, [model], conditions = ["baseline"], 
                              difficulties = ["easy", "medium", "hard"], question_id=None)
        print("- NEW")
        compute_scoring_table(data_new, [model], conditions = ["baseline"], 
                              difficulties = ["easy", "medium", "hard"], question_id=None)

        # for question in questions:
        #     compute_scoring_table(data_old, [model], conditions = ["baseline"], 
        #                           difficulties = ["easy", "medium", "hard"], question_id=question)
        #     compute_scoring_table(data_new, [model], conditions = ["baseline"], 
        #                           difficulties = ["easy", "medium", "hard"], question_id=question)

#compare_scores(df, df_correctness, ["llama3.1:8b", "mistral-nemo:12b", "mistral-small:22b"])
#
# # ========= Completion score/ Correctness score by questions :
# # ========= Average
# print("====Old correctness ====")
# print("average")
compute_scoring_table(df, ["gemma2:2b"], conditions = ["baseline"], difficulties = ["easy", "medium", "hard"], question_id=None)

# print("question by question")
# # # ========= Question by question
# compute_scoring_table(df, ["mistral-nemo:12b"], conditions = ["baseline"], difficulties = ["easy", "medium", "hard"], question_id="perceive")
# compute_scoring_table(df, ["mistral-nemo:12b"], conditions = ["baseline"], difficulties = ["easy", "medium", "hard"], question_id="push")
# compute_scoring_table(df, ["mistral-nemo:12b"], conditions = ["baseline"], difficulties = ["easy", "medium", "hard"], question_id="lift")
# compute_scoring_table(df, ["mistral-nemo:12b"], conditions = ["baseline"], difficulties = ["easy", "medium", "hard"], question_id="grasp")

# print("====New correctness ====")
# print("average")
# compute_scoring_table(df_correctness, ["mistral-nemo:12b"], conditions = ["baseline"], difficulties = ["easy", "medium", "hard"], question_id=None)

# print("question by question")
# # # # ========= Question by question
# compute_scoring_table(df_correctness, ["mistral-nemo:12b"], conditions = ["baseline"], difficulties = ["easy", "medium", "hard"], question_id="perceive")
# compute_scoring_table(df_correctness, ["mistral-nemo:12b"], conditions = ["baseline"], difficulties = ["easy", "medium", "hard"], question_id="push")
# compute_scoring_table(df_correctness, ["mistral-nemo:12b"], conditions = ["baseline"], difficulties = ["easy", "medium", "hard"], question_id="lift")
# compute_scoring_table(df_correctness, ["mistral-nemo:12b"], conditions = ["baseline"], difficulties = ["easy", "medium", "hard"], question_id="grasp")

# def compute_scoring_table(dataframe, model, conditions = ["baseline", "rule", "shuffle"], difficulties = ["easy", "medium", "hard"], question_id = "push"):
#     df_results = pd.DataFrame(columns=['Model', 'Easy score', 'Easy correct', 'Medium score', 'Medium correct', 'Hard score', 'Hard correct'])
#     df_results['Model'] = model

#     for difficulty in difficulties:
#         for condition in conditions:
#             chosen_data = get_chosen_data(dataframe, model, condition, difficulty, question_id)
            
#             average_score = chosen_data["score"].mean()
#             rounded_average_score = round(average_score, 2)
#             std_score = chosen_data["score"].std()
#             rounded_std_score = round(std_score, 2)
            
#             correctness_rate = len(chosen_data[chosen_data["is_correct"] == True])/len(chosen_data)
#             rounded_correctness_rate = round(correctness_rate, 2)

#             if(difficulty == "easy"):
#                 print("easy : ", str(rounded_average_score) + "(± " + str(rounded_std_score) + ")", rounded_correctness_rate)
#                 df_results["Easy score"][0] = str(rounded_average_score) + "(± " + str(rounded_std_score) + ")"
#                 df_results["Easy correct"][0] = rounded_correctness_rate
#             elif(difficulty == "medium"):
#                 print("medium : ", str(rounded_average_score) + "(± " + str(rounded_std_score) + ")", rounded_correctness_rate)
#                 df_results["Medium score"][0] = str(rounded_average_score) + "(± " + str(rounded_std_score) + ")"
#                 df_results["Medium correct"][0] = rounded_correctness_rate
#             else:
#                 print("hard : ", str(rounded_average_score) + "(± " + str(rounded_std_score) + ")", rounded_correctness_rate)
#                 df_results["Hard score"][0] = str(rounded_average_score) + "(± " + str(rounded_std_score) + ")"
#                 df_results["Hard correct"][0] = rounded_correctness_rate

# compute_scoring_table(df, "mistral-nemo:12b", conditions = ["baseline"], difficulties = ["easy", "medium", "hard"], question_id="grasp")
# compute_scoring_table(df_correctness, "mistral-nemo:12b", conditions = ["baseline"], difficulties = ["easy", "medium", "hard"], question_id="grasp")