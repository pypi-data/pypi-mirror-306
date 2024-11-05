# Data GUI LLM Package

This package provides tools for exploratory data analysis (EDA) including
univariate and multivariate analysis, data visualization, and insights generation
using Groq LLM Framework.

Just pass your data, target column and groq api key like this:

from dataguillm import AnalyzeData

object= AnalyzeData(df, "targetcol", "groqapi")
object.datainsights()

See the magic by yourself!

Note: After installing please install numpy==1.26.4
