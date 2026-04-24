import os
from PyQt6.QtGui import QIcon
from config import JPG_PATH

icons_dir = os.path.join(JPG_PATH, "icons")

def get_icon(name, sub_folder):
    safe_name = name.lower().replace(" ", "_") + ".png"
    icon_path = os.path.join(icons_dir, sub_folder, safe_name)
    
    if os.path.exists(icon_path):
        return QIcon(icon_path)
    return QIcon()
        
ICON_MAP = {
    "Population Mean": "mean",
    "Sample Mean": "mean",
    "Population Variance": "variance",
    "Sample Variance": "variance",
    "Population Standard Deviation": "standard_deviation",
    "Sample Standard Deviation": "standard_deviation",
    "Percentile": "percentile",
    "Population Covariance": "covariance",
    "Sample Covariance": "covariance",
    "Correlation": "correlation",
    "Mutually Exclusive": "addition_rule",
    "Non Mutually Exclusive": "addition_rule",
    "Independent Events": "multiplication_rule",
    "Dependent Events": "multiplication_rule",
    "Bayes": "bayes",
    "Central Limit Theorem": "central_limit_theorem",
    "Confidence Interval": "confidence_interval",
    "Margin Of Error": "margin_of_error",
    "Bernoulli Distribution": "bernoulli_distribution",
    "Binomial Distribution": "binomial_distribution",
    "Poisson Distribution PMF": "poisson_distribution",
    "Poisson Distribution CDF": "poisson_distribution",
    "Normal Distribution PDF": "normal_distribution",
    "Normal Distribution CDF": "normal_distribution",
    "Standard Normal Distribution": "standard_normal_distribution",
    "Uniform Distribution PDF": "uniform_distribution",  # Not: Orijinal kodunda PMF yazıyordu, matematiksel olarak PDF olmalı
    "Uniform Distribution CDF": "uniform_distribution",
    "Log Normal Distribution PDF": "log_normal_distribution", # Not: Orijinal kodunda 'Nomal' ve PMF yazım hataları düzeltildi
    "Log Normal Distribution CDF": "log_normal_distribution",
    "Pareto Distribution PDF": "pareto_distribution",
    "Pareto Distribution CDF": "pareto_distribution",
    "Z Test": "z_test",
    "Single Sample t Test": "t_test",
    "Independent Sample t Test": "t_test",
    "Paired Sample t Test": "t_test",
    "Chi Square Test": "chi_square_test",
    "ANOVA": "anova"
}

def get_archive_record_icon(record_operation):
    icon_name = ICON_MAP.get(record_operation)
    
    if icon_name:
        return get_icon(icon_name, "sub_subjects")
        
    return QIcon() # Haritada bulunamazsa boş ikon döndür