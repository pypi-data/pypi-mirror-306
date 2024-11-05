import gym
import gymnasium
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import os

class RLVisualizer:
    """
    RLVisualizer is a tool for visualizing action probabilities, entropy, and reward progression
    within reinforcement learning environments.

    Features:
        - Visualizes action probabilities as a bar chart
        - Tracks entropy of the action distribution to measure model uncertainty
        - Plots reward progression within each episode
        - Compatible with both Gym and Gymnasium environments with discrete action spaces

    Args:
        action_space (gym.Space): The action space of the environment. Must be of type Discrete.
        config (dict, optional): Configuration options for customizing the visualizer. Defaults to None.

    Configuration Options:
        history_length (int): Number of timesteps to keep in history for entropy and reward plots.
        pause_time (float): Delay time between plot updates, in seconds.
        show_entropy (bool): If True, displays entropy plot.
        show_action_counts (bool): If True, displays action count plot.
        show_rewards (bool): If True, displays reward progression plot.
        save_path (str): Directory path for saving plots as images.
        episode_end_save (bool): If True, saves plots at the end of each episode.
        colors (list): List of colors for each action in the probability plot.
        highlight_color (str): Color to highlight the chosen action.
        figsize (tuple): Figure size for the plots.
        prob_ylabel, prob_xlabel, prob_title (str): Labels and title for the action probability plot.
        entropy_title, reward_title (str): Titles for the entropy and reward plots.
    """
    
    def __init__(self, action_space, config=None):
        if not isinstance(action_space, (gym.spaces.Discrete, gymnasium.spaces.Discrete)):
            raise ValueError("RLVisualizer only supports Discrete action spaces.")
        
        self.config = config or {}
        self.num_actions = action_space.n
        self.history_length = self.config.get("history_length", 50)
        self.pause_time = self.config.get("pause_time", 0.001)
        self.show_entropy = self.config.get("show_entropy", True)
        self.show_action_counts = self.config.get("show_action_counts", True)
        self.show_rewards = self.config.get("show_rewards", True)
        self.save_path = self.config.get("save_path", None)
        self.episode_end_save = self.config.get("episode_end_save", False)
        self.colors = self.config.get("colors", ["gray"] * self.num_actions)
        self.highlight_color = self.config.get("highlight_color", "blue")
        self.figsize = self.config.get("figsize", (8, 8))
        self.prob_ylabel = self.config.get("prob_ylabel", "Probability")
        self.prob_xlabel = self.config.get("prob_xlabel", "Actions")
        self.prob_title = self.config.get("prob_title", "Current Action Probabilities")
        self.entropy_title = self.config.get("entropy_title", "Entropy of Action Distribution")
        self.reward_title = self.config.get("reward_title", "Reward per Step in Current Episode")

        self.prob_history = [deque(maxlen=self.history_length) for _ in range(self.num_actions)]
        self.entropy_history = deque(maxlen=self.history_length)
        self.reward_history = deque(maxlen=self.history_length)
        self.action_counts = np.zeros(self.num_actions)

        self.fig, (self.ax_probs, self.ax_entropy, self.ax_rewards) = plt.subplots(3, 1, figsize=self.figsize)
        self._initialize_probability_plot()
        self._initialize_entropy_plot()
        self._initialize_reward_plot()

    def _initialize_probability_plot(self):
        """
        Initializes the bar chart plot for action probabilities.
        """
        self.ax_probs.set_ylim(0, 1)
        self.ax_probs.set_xlim(-0.5, self.num_actions - 0.5)
        self.bar_probs = self.ax_probs.bar(range(self.num_actions), [0] * self.num_actions,
                                           color=self.colors,
                                           tick_label=[f"Action {i}" for i in range(self.num_actions)])
        self.ax_probs.set_ylabel(self.prob_ylabel)
        self.ax_probs.set_xlabel(self.prob_xlabel)
        self.ax_probs.set_title(self.prob_title)
        self.chosen_action_text = self.ax_probs.text(0.5, 0.9, "", ha="center", va="center", 
                                                     transform=self.ax_probs.transAxes, fontsize=12, 
                                                     color=self.highlight_color)

    def _initialize_entropy_plot(self):
        """
        Initializes the line plot for entropy if show_entropy is True.
        """
        if self.show_entropy:
            self.ax_entropy.set_ylim(0, np.log(self.num_actions))
            self.ax_entropy.set_xlim(0, self.history_length)
            self.ax_entropy.set_ylabel("Entropy")
            self.ax_entropy.set_xlabel("Time Step")
            self.ax_entropy.set_title(self.entropy_title)
            self.entropy_line, = self.ax_entropy.plot([], [], lw=2)
        else:
            self.ax_entropy.set_visible(False)

    def _initialize_reward_plot(self):
        """
        Initializes the line plot for per-step rewards within a single episode.
        """
        if self.show_rewards:
            self.ax_rewards.set_ylim(-1, 1)  # Adjust this range based on expected reward values
            self.ax_rewards.set_xlim(0, self.history_length)
            self.ax_rewards.set_ylabel("Reward")
            self.ax_rewards.set_xlabel("Time Step")
            self.ax_rewards.set_title(self.reward_title)
            self.reward_line, = self.ax_rewards.plot([], [], lw=2)
        else:
            self.ax_rewards.set_visible(False)

    def update_visualization(self, action_probs, reward, chosen_action=None):
        """
        Updates the plots for action probabilities, entropy, and rewards.

        Args:
            action_probs (array-like): Probability distribution over actions.
            reward (float): Reward received at the current step.
            chosen_action (int, optional): The action chosen by the agent. Defaults to None.
        """
        action_probs = np.array(action_probs).flatten()
        
        for i, (bar, prob) in enumerate(zip(self.bar_probs, action_probs)):
            bar.set_height(prob)
            bar.set_color(self.highlight_color if i == chosen_action else self.colors[i])

        if chosen_action is not None:
            self.chosen_action_text.set_text(f"Chosen Action: {chosen_action}")
            self.action_counts[chosen_action] += 1

        for i, prob in enumerate(action_probs):
            self.prob_history[i].append(prob)
        entropy = -np.sum(action_probs * np.log(action_probs + 1e-10))
        self.entropy_history.append(entropy)
        
        self.reward_history.append(reward)
        
        if self.show_entropy:
            self.entropy_line.set_data(range(len(self.entropy_history)), list(self.entropy_history))
            self.ax_entropy.relim()
            self.ax_entropy.autoscale_view()
        
        if self.show_rewards:
            self.reward_line.set_data(range(len(self.reward_history)), list(self.reward_history))
            self.ax_rewards.relim()
            self.ax_rewards.autoscale_view()

        plt.pause(self.pause_time)

    def reset(self):
        """
        Resets the histories and plots for the start of a new episode.
        """
        self.prob_history = [deque(maxlen=self.history_length) for _ in range(self.num_actions)]
        self.action_counts.fill(0)
        self.entropy_history.clear()
        self.reward_history.clear()
        if self.show_entropy:
            self.entropy_line.set_data([], [])
        if self.show_rewards:
            self.reward_line.set_data([], [])
        self.chosen_action_text.set_text("")
        plt.draw()

    def plot_action_counts(self):
        """
        Plots a bar chart showing the counts of each action taken within the episode.
        """
        if self.show_action_counts:
            plt.figure(figsize=(8, 4))
            plt.bar(range(self.num_actions), self.action_counts, color=self.colors)
            plt.xlabel("Actions")
            plt.ylabel("Count")
            plt.title("Action Counts for Current Episode")
            plt.show()

    def save_plots(self, suffix=""):
        """
        Saves the current figure to the specified path.

        Args:
            suffix (str, optional): Optional suffix for the filename. Defaults to "".
        """
        if self.save_path:
            os.makedirs(self.save_path, exist_ok=True)
            self.fig.savefig(os.path.join(self.save_path, f"action_probabilities{suffix}.png"))
            if self.show_action_counts:
                plt.figure()
                plt.bar(range(self.num_actions), self.action_counts, color=self.colors)
                plt.xlabel("Actions")
                plt.ylabel("Count")
                plt.title("Action Counts for Current Episode")
                plt.savefig(os.path.join(self.save_path, f"action_counts{suffix}.png"))
                plt.close()
