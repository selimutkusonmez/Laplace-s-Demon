from src.engine import *
class DemonEngine():
    def __init__(self):

        self.operation_map = {
            "Population Mean" : CalculatePopulationMean,
            "Sample Mean" : CalculateSampleMean,
            "Population Variance" : CalculatePopulationVariance,
            "Sample Variance" : CalculateSampleVariance,
            "Population Standard Deviation" : CalculatePopulationStandardDeviation,
            "Sample Standard Deviation" : CalculateSampleStandardDeviation,
            "Percentile" : CalculatePercentile,
            "Population Covariance" : CalculatePopulationCovariance,
            "Sample Covariance" : CalculateSampleCovariance,
            "Correlation" : CalculateCorrelation,
            "Mutually Exclusive" : CalculateMutuallyExclusiveProbability,
            "Non Mutually Exclusive" : CalculateNonMutuallyExclusiveProbability,
            "Independent Events" : CalculateIndependentEventsProbability,
            "Dependent Events" : CalculateDependentEventsProbability,
            "Bayes" : CalculateBayesProbability,
            "Central Limit Theorem" : CalculateCentralLimit,
            "Confidence Interval" : CalculateConfidenceInterval,
            "Margin Of Error" : CalculateMarginOfError,
            "Bernoulli Distribution" : CalculateBernoulliDistribution,
            "Binomial Distribution" : CalculateBinomialDistribution,
            "Poisson Distribution PMF" : CalculatePoissonDistributionPMF,
            "Poisson Distribution CDF" : CalculatePoissonDistributionCDF,
            "Normal Distribution PDF" : CalculateNormalDistributionPDF,
            "Normal Distribution CDF" : CalculateNormalDistributionCDF,
            "Standard Normal Distribution" : CalculateStandardNormalDistribution,
            "Uniform Distribution PDF" : CalculateUniformDistributionPDF,
            "Uniform Distribution CDF" : CalculateUniformDistributionCDF,
            "Log Normal Distribution PDF" : CalculateLogNormalDistributionPDF,
            "Log Normal Distribution CDF" : CalculateLogNormalDistributionCDF,
            "Pareto Distribution PDF" : CalculateParetoDistributionPDF,
            "Pareto Distribution CDF" : CalculateParetoDistributionCDF,
            "Z Test" : TestZTest,
            "Single Sample t Test" : TestSingleSampleTTest,
            "Independent Sample t Test" : TestIndependentSampleTTest,
            "Paired Sample t test" : TestPairedSampleTTest,
            "Chi Square Test" : TestChiSquareTest,
            "ANOVA" : TestAnova,
        }
        
    def calculate(self, operation_name : str, input_list : list):

        worker_class = self.operation_map.get(operation_name)

        result = worker_class.calculate(input_list)
        
        return result