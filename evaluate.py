import os
import json
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import math
from scipy import stats
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

pd.options.mode.chained_assignment = None

# Enable LaTeX-style font rendering
plt.rcParams.update({
    "text.usetex": True,  # Use LaTeX for text
    "font.family": "serif",  # Use a serif font
    "font.size": 12,  # Base font size
    "axes.labelsize": 12,  # Axis labels
    "xtick.labelsize": 10,  # X-axis tick size
    "ytick.labelsize": 10,  # Y-axis tick size
    "axes.titlesize": 14,  # Title size
})

def get_question(data_structure, model, condition, question, variation_id):
    # Navigate to the specific variation
    answers = data_structure.get(model, {}).get(condition, {}).get(question, [])
    
    # Find the question with the specified variation_id
    for answer in answers:
        if answer["question_id"] == variation_id:
            return answer
    return None 

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

def generate_distplot(dataframe, model, condition = "baseline", difficulties = ["easy", "medium", "hard"]):
    datas = []
    for difficulty in difficulties:
        chosen_data = dataframe[(dataframe["model"] == model) & (dataframe["complexity"] == difficulty) & (dataframe["condition"] == condition)]["score"]
        datas.append(chosen_data*100)

def generate_histplot(dataframe, models, complexity_colors = {"easy": "green", "medium": "orange", "hard": "red"}, condition = "baseline"):

    fig, axes = plt.subplots(3,2)
    fig.set_figheight(9)
    fig.set_figwidth(10)
    
    for model, ax in zip(models, axes.flatten()):
        for complexity, color in complexity_colors.items():
            chosen_data = dataframe[(dataframe["model"] == model) 
                            & (dataframe["condition"] == condition)
                            & (dataframe["complexity"] == complexity)]
            chosen_data["score"]= chosen_data["score"]*100
            correctness_rate = len(chosen_data[chosen_data["is_correct"] == True])/len(chosen_data)
            
            custom_clip = (min(chosen_data["score"]), max(chosen_data["score"]))
            custom_kde_kws={"bw_adjust": 2, "cut": 2, "clip": (custom_clip)}
            
            
            if(complexity == "easy"):
                nb_items = 10
            elif(complexity == "medium"):
                nb_items = 14
            elif(complexity == "hard"):
                nb_items = 17
            
            custom_binwidth = 100 / nb_items
                
            sns.histplot(data=chosen_data, x="score", kde=True, binwidth=custom_binwidth, binrange=(-custom_binwidth/2, 100 + custom_binwidth/2), legend=True, stat='count', 
                         ax=ax, color=color, kde_kws=custom_kde_kws, common_norm=True)
            # To prevent overlap between hard and medium on this particular graph, we offset it by 0.5
            if(complexity == "medium" and model == "llama3.2:3b"):
                ax.axvline(x = correctness_rate*100 + 0.5, color = color, linestyle = 'dashed')
            else:
                ax.axvline(x = correctness_rate*100, color =color, linestyle = 'dashed')
            ax.set_title(model)
            ax.set_ylim(0, 60)
            ax.set_xlim(0, 105)
            ax.set_xlabel("Accuracy")
            ax.set_ylabel("Frequency")
            ax.minorticks_on()
               
    hist_legend = [mpatches.Patch(color=color, alpha=0.5, label=complexity) for complexity, color in complexity_colors.items()]
    legend_hist = fig.legend(handles=hist_legend, title="Completeness distribution", loc="upper left", fontsize=11, 
                             title_fontsize=11, ncol = 3, columnspacing=0.5, alignment='left')

    line_legend = [mlines.Line2D([], [], color=color, linestyle="--", linewidth=2, label=complexity) for complexity, color in complexity_colors.items()]
    legend_lines = fig.legend(handles=line_legend, title="Correctness score", loc="upper center", fontsize=11, 
                              title_fontsize=11, ncol = 3, columnspacing=0.5, alignment='left')
        
    fig.add_artist(legend_hist)
    fig.subplots_adjust(wspace=0.15, hspace=0.4)
    fig.legend()
    plt.show()
    
def generate_average_histplot(dataframe, models, condition_colors = {"baseline": "blue", "rule": "orange", "shuffle": "red"}):
    fig, axes = plt.subplots(3,2)
    fig.set_figheight(9)
    fig.set_figwidth(10)

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
            ax.set_ylim(0, 80)
            ax.set_xlim(0, 105)
            ax.set_xlabel("Accuracy")
            ax.set_ylabel("Frequency")
            ax.minorticks_on()

    hist_legend = [mpatches.Patch(color=color, alpha=0.5, label=condition) for condition, color in condition_colors.items()]
    legend_hist = fig.legend(handles=hist_legend, title="Completeness", loc="upper left", fontsize=10, title_fontsize=10)

    line_legend = [mlines.Line2D([], [], color=color, linestyle="--", linewidth=2, label=condition) for condition, color in condition_colors.items()]
    legend_lines = fig.legend(handles=line_legend, title="Correctness", loc="upper center", fontsize=10, title_fontsize=10)
    
    fig.add_artist(legend_hist)
    fig.subplots_adjust(wspace=0.18, hspace=0.4)
    fig.legend()
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
    plt.xlabel("Completion score (%)")
    plt.ylabel("Count")
    
    hist_legend = [mpatches.Patch(color=color, alpha=0.5, label=model) for model, color in models_colored.items()]
    legend_hist = ax.legend(handles=hist_legend, title="Complexity level", loc="upper left", fontsize=10, title_fontsize=10)

    line_legend = [mlines.Line2D([], [], color=color, linestyle="--", linewidth=2, label=model) for model, color in models_colored.items()]
    legend_lines = ax.legend(handles=line_legend, title="Correctness rate", loc="center left", fontsize=10, title_fontsize=10)
    
    ax.add_artist(legend_hist)
    plt.tight_layout()
    plt.show()

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
    grouped_data = dataframe.groupby(["model", "condition"])["score"].mean().reset_index()
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
    plt.ylabel("Completeness Median Accuracy (\%)")
    plt.ylim(0, 100)  # Ensure proper scaling
    # plt.xticks(rotation=45)  # Rotate model names for better readability
    plt.legend(title="Category")  # Display legend

    plt.show()

def get_chosen_data(dataframe, model, condition, difficulty, question_id):
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
                
                average_score = chosen_data["score"].median()
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

def compute_average_scoring_table(dataframe, models, conditions = ["baseline", "rule", "shuffle"], 
                                  metric_completion = "mean"):
    df_results = pd.DataFrame(columns=['Model', 'condition', 'Correctness score', 'Completeness Mean Score'])
    df_results['Model'] = models

    for model in models:
        for condition in conditions:
            chosen_data = dataframe[(dataframe["model"] == model) & (dataframe["condition"] == condition)]
            
            average_score = chosen_data["score"].mean()
            rounded_average_score = round(average_score, 3)
            std_score = chosen_data["score"].std()
            rounded_std_score = round(std_score, 3)
            
            correctness_rate = len(chosen_data[chosen_data["is_correct"] == True])/len(chosen_data)
            rounded_correctness_rate = round(correctness_rate, 3)
            new_elem = np.array([model, condition, rounded_correctness_rate, 
                                    str(rounded_average_score) + "(± " + str(rounded_std_score) + ")"])
            
            #df_results = pd.concat([df_results, columns=df_results.columns, new_elem], ignore_index=True)
            df_results = pd.concat([pd.DataFrame([new_elem], columns=df_results.columns), df_results], ignore_index=True)
            # df_results.loc[-1] = np.array([model, condition, rounded_correctness_rate, 
            #                                str(rounded_average_score) + "(± " + str(rounded_std_score) + ")"])
            # df_results["Correctness score"] = rounded_correctness_rate
            # df_results["Completeness Mean Score"] = str(rounded_average_score) + "(± " + str(rounded_std_score) + ")"
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

# Path to the dataset directory
data_directory = "/home/bdussard/inference_explanation/dataset/evaluations"

answers_array = explore_and_store_data(data_directory)

model = "llama3.1:8b"
condition = "baseline"
question = "grasp_easy"
question_id = "a_grasp_easy_1b"

# Example: Accessing data for a specific model, condition, and variation
example_data = answers_array["llama3.1:8b"]["baseline"]["grasp_easy"]
dataframe = pd.DataFrame.from_records(example_data)

print(dataframe.head())

# Example usage of compute_stats
res_stats = compute_stats(example_data)

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
                id = "_".join([model, question, difficulty, condition])
                scores.append([id, stats['average_score']])
   
df = flatten_data(answers_array)

compute_scoring_table(df, ["gemma2:2b", "llama3.2:3b", "llama3.1:8b", "gemma2:9b", "mistral-nemo:12b", "mistral-small:22b"])

# ==================== 6 subplots with each difficulty level ================
models_reordered = ["llama3.2:3b", "llama3.1:8b", "gemma2:2b", "gemma2:9b", "mistral-nemo:12b", "mistral-small:22b"]

models_colored = {"llama3.2:3b": 'green',
                 "gemma2:2b": 'red',
                 "llama3.1:8b" :'blue',
                 "gemma2:9b": 'purple',
                 "mistral-nemo:12b": 'orange',
                 "mistral-small:22b": 'brown'}

# ======== generate 6 subplots with each model and average of difficulty levels ===
condition_colors = {"baseline": "blue"}
generate_average_histplot(df, models_reordered, condition_colors)
condition_colors = {"baseline": "blue", "rule": "orange"}
generate_average_histplot(df, models_reordered, condition_colors)
condition_colors = {"baseline": "blue", "shuffle": "red"}
generate_average_histplot(df, models_reordered, condition_colors)

# ======== generate 6 subplots with each model and each difficulty level, on baseline ===
generate_histplot(df, models_reordered)
