import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb

#possUtil/HPUS/simulation(possession and full match)/momentum indicator/heatmap

def cal_poss_util(data, shot_num=[6,8], cross_num=[4], num_actions=9):
    # Check if the input is a DataFrame
    if not isinstance(data, pd.DataFrame):
        data = pd.read_csv(data)
    
    # Map actions to integers
    action_dict = {'short_pass': 0, 'carry': 1, 'high_pass': 2, '_': 3, 'cross': 4, 
                   'long_pass': 5, 'shot': 6, 'dribble': 7}
    data["action"] = data["action"].map(action_dict)
    data.loc[(data["action"] == 6) & (data["goal"] == 1), "action"] = 8

    #drop all row with action = period_over
    data = data[data["action"] != 3]

    # Prepare action probability columns
    action_columns = [f'action_{i}_prob' for i in range(num_actions)]
    
    # Ensure action probabilities sum to 1 (apply softmax)
    row_sums = data[action_columns].sum(axis=1)
    if not np.allclose(row_sums, 1):
        exp_values = np.exp(data[action_columns])
        data[action_columns] = exp_values.div(exp_values.sum(axis=1), axis=0)

    # Fill NaN values with 0
    data.fillna(0, inplace=True)

    # Sum up shot and cross probabilities
    poss_util_prob = data[[f'action_{i}_prob' for i in shot_num + cross_num]].sum(axis=1)
    data['poss_util_prob'] = poss_util_prob

    # Compute attack_flag efficiently
    relevant_actions = shot_num + cross_num
    data['attack_flag'] = data['action'].isin(relevant_actions).astype(int)
    
    # Group by match_id and poss_id, and calculate total probabilities
    poss_util = data.groupby(['match_id', 'poss_id'], as_index=False).agg({
        'poss_util_prob': 'sum',
        'attack_flag': 'sum',
        'team': 'first',
    })
    
    # Set poss_util_prob to negative if no shot or cross occurred
    poss_util.loc[poss_util['attack_flag'] == 0, 'poss_util_prob'] *= -1

    # Drop attack_flag from the final output
    poss_util.drop(columns='attack_flag', inplace=True)
    
    return poss_util

def plot_poss_util_dist(poss_util, save_path, bins=20):
    # Get the unique team IDs
    teams = poss_util['team'].unique()
    
    # Set up the figure
    plt.figure(figsize=(12, 8))

    # Plot a density curve for each team
    for team in teams:
        team_data = poss_util[poss_util['team'] == team]['poss_util_prob']
        
        # Calculate the kernel density estimation using a histogram
        density, bins = np.histogram(team_data, bins=bins, density=True)
        bin_centers = 0.5 * (bins[1:] + bins[:-1])
        
        # Plot the density curve
        plt.plot(bin_centers, density, label=team, linewidth=2)

    # Set plot labels and title with increased font size
    plt.xlabel('Poss-Util Probability', fontsize=18)  # Increased to 16
    plt.ylabel('Density', fontsize=18)  # Increased to 16
    plt.title('Poss-Util', fontsize=18)  # Increased to 18
    
    # Increase font size for tick labels
    plt.tick_params(axis='both', labelsize=16)  # Set font size for x and y tick labels

    # Add legend with increased font size
    plt.legend(title='Team ID', fontsize=16)  # Increased to 14
    
    # Display the plot and save it
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(save_path + "poss_util.png")
    plt.close()  # Close the plot to free memory

def plot_poss_util_plus_dist(poss_util, save_path, bins = 20):
    #for each team summarize the poss_util_prob (only positive value) per match_id
    # Get the unique team IDs
    teams = poss_util['team'].unique()
    poss_util_plus = poss_util[poss_util['poss_util_prob'] > 0]
    poss_util_plus = poss_util_plus.groupby(['team','match_id'],as_index=False).agg({'poss_util_prob':'sum'})
    # Set up the figure
    plt.figure(figsize=(12, 8))
    for team in teams:
        team_data = poss_util_plus[poss_util_plus['team'] == team]['poss_util_prob']
        
        # Calculate the kernel density estimation using a histogram
        density, bins = np.histogram(team_data, bins=bins, density=True)
        bin_centers = 0.5 * (bins[1:] + bins[:-1])
        
        # Plot the density curve
        plt.plot(bin_centers, density, label=team, linewidth=2)
        # Plot the mean value
        plt.axvline(x=team_data.mean(), color='black', linestyle='--', linewidth=2)

    # Set plot labels and title with increased font size
    plt.xlabel('Poss-Util+ per Match', fontsize=18)  # Increased to 16
    plt.ylabel('Density', fontsize=18)  # Increased to 16
    plt.title('Poss-Util+', fontsize=18)  # Increased to 18
    # Increase font size for tick labels
    plt.tick_params(axis='both', labelsize=16)  # Set font size for x and y tick labels
    # Add legend with increased font size
    plt.legend(title='Team ID', fontsize=16)  # Increased to 14
    # Display the plot and save it
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(save_path + "poss_util_plus.png")
    plt.close()  # Close the plot to free memory

if __name__ == "__main__":
    import os
    inference_data = os.getcwd()+"/test/inference/nmstpp/inference.csv"
    save_path = os.getcwd()+"/test/application/"
    poss_util = cal_poss_util(inference_data)
    poss_util.to_csv(save_path+"poss_util.csv",index=False)
    plot_poss_util_dist(poss_util,save_path,bins=20)
    plot_poss_util_plus_dist(poss_util,save_path,bins=20)
    



