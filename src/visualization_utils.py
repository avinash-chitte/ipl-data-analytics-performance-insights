import matplotlib.pyplot as plt
import seaborn as sns

# Professional Harmonious Color Palette
PRIMARY_COLOR = '#1E3A8A'  # Deep Navy Blue
SECONDARY_COLOR = '#F97316'  # Orange Accent
NEUTRAL_DARK = '#1F2937'  # Charcoal
NEUTRAL_LIGHT = '#F3F4F6'  # Soft Gray
SUCCESS_COLOR = '#10B981'  # Emerald Green
WARNING_COLOR = '#EF4444'  # Crimson Red

def setup_plot_style():
    """
    Sets up a modern, clean, and professional design theme for matplotlib and seaborn.
    Uses Outfit/Inter-like default settings for sizing and fonts.
    """
    sns.set_theme(style="whitegrid")
    
    plt.rcParams.update({
        'figure.figsize': (12, 6),
        'figure.dpi': 100,
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'legend.title_fontsize': 11,
        'axes.edgecolor': '#E5E7EB',
        'axes.linewidth': 1.2,
        'grid.color': '#F3F4F6',
        'grid.linestyle': '-',
        'figure.titlesize': 16,
        'figure.titleweight': 'bold'
    })
    print("Plotting styles and themes initialized successfully.")

def get_ipl_team_colors():
    """
    Returns the hex color code mapping for major IPL teams to ensure brand authenticity.
    """
    return {
        'Chennai Super Kings': '#F7E115',
        'Mumbai Indians': '#004B87',
        'Royal Challengers Bangalore': '#EC1C24',
        'Kolkata Knight Riders': '#2E0854',
        'Rajasthan Royals': '#EA1B85',
        'Delhi Capitals': '#000080',
        'Kings XI Punjab': '#DD1F26',
        'Punjab Kings': '#DD1F26',
        'Sunrisers Hyderabad': '#FF822A',
        'Deccan Chargers': '#0D2240',
        'Delhi Daredevils': '#DD1F26',
        'Gujarat Titans': '#1B252C',
        'Lucknow Super Giants': '#0057E7',
        'Rising Pune Supergiant': '#D11D5B',
        'Rising Pune Supergiants': '#D11D5B',
        'Kochi Tuskers Kerala': '#FF8000',
        'Pune Warriors': '#2F4F4F',
        'Gujarat Lions': '#FF7C24'
    }

def get_palette_by_name(name="cool"):
    """
    Returns pre-curated color list for generic visual elements.
    """
    palettes = {
        "cool": ['#1E3A8A', '#3B82F6', '#60A5FA', '#93C5FD', '#BFDBFE'],
        "warm": ['#F97316', '#FDBA74', '#F43F5E', '#FDA4AF', '#FFE4E6'],
        "diverse": ['#1E3A8A', '#F97316', '#10B981', '#8B5CF6', '#EC4899', '#F59E0B'],
        "gray": ['#374151', '#4B5563', '#6B7280', '#9CA3AF', '#D1D5DB']
    }
    return palettes.get(name, palettes["cool"])
