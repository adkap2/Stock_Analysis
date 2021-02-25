# Analysis of Gamestop Stock in the WallStreetBets Subreddit

## Proposition

WallStreetBets users played a role in the value of gamestop stock as other highly shorted
during January and February of 2021. WallStreetBets subreddit data will be overlayed with daily stock
price for top "Hype" stocks during the given time frame. 

## Hypothesis Testing

H01 = Probability of no significant correlation between WallStreetBets Posts Gamestop stock value
HA1 = Probility of significant correlation between WallStreetBets Posts and GameStop stock Value

H02 = Probability of no significant correlation between Gamestop stock value WallStreetBets subscriber count
HA2 = Probility that Gamestop stock value played a significant roll increasing WallStreetBets subscriber count


## Statistical Tests

1.  
    * Null Hypothesis: No correlation between Number of stock mentions and gamestop stock price per day
    * Alternate Hypothesis: Significant correlation between stock mentions and gamestop stock price per day

2.  
    * Null Hypothesis: No significant correlation between GameStop stock value and WallStreetBets subscriber count
    * Alternative Hypothesis: Gamestop stock value influenced WallStreetBets subscriber count


## Plots

### GME
<img src="figures/GME_Mentions_Price.png" alt="alt text" width=400 height=300>

By visual inspection, there is a clear connection between GME's high price and the number of mentions
in a given day. The filtered dataset includes frequency of GME ticker sybol recorded on a daily basis. For the 50
days this is plotted over, number of mentions range between 10 to 2800. In this time period, GME intraday high values
range between $19 and $483.


<img src="figures/GME_Mentions_Changes.png" alt="alt text" width=400 height=300>

This plot shows the daily number of mentions plotted against the daily change in stock price.
Here, it is seen that on the days when the stock made the largest leaps, whether postive or negative, redditors were
posting the most about the stock. This plot would suggest that people discuss the stock most on days with significant change. This is 
regardless as to whether the stock value is increasing or decreasing.

<img src="figures/GME_Mentions_vs_Day_Change_Norm.png" alt="alt text" width=400 height=300>

This scatter plot shows the similarities between change in daily number of mentions and daily stock day change.
After dropping obvious outlier, it is clear that for every change in daily mentions, an expected similar change will occur in GME
stock value.

### AMC
<img src="figures/AMC_Mentions_Price.png" alt="alt text" width=400 height=300>

AMC stock was known to have followed a similar trend to GME stock in early 2021. The mentions and stock price follow a near
identical pattern to that of GME.


## Results

###  Running the one way anova test with Gradient of Daily Number of Stock Mentions, Daily change in Stock Price
1.  **GME**
    *  f value = 1.305
    *  pvalue = 0.257
2.  **AMC**
    *  f value = 1.816
    *  pvalue = 0.181

The resulting p values from the Anova test suggest that there is not a significant enough correlation between stock
price and GME or AMC stock to reject the Null Hypothesis.

###  Running the One Sample Ttest with combined gradient values from Daily Number of Stock Mentions, Daily change in Stock Price
1.  **GME**
    *  statistic = -3.999
    *  pvalue = 0.00019
2.  **AMC**
    *  statistic = -3.195
    *  pvalue = 0.0024

The resulting p values from the one sample Ttest suggest that there is enough statistical signficance to reject the Null Hypothesis that GME price
and WallStreetBets GME mentions are correlated.




### Monday's Work
Current collecting comment data for WallStreetBets posts between Jan 1st
and Feb 22 2021. So far, able to collect a max of 15k comments per post.
Posts with above 80k stop the server from scraping entirely.

Data is then inputted into a sentiment analyzer where postive/negative sentiment levels are provided for each day.

Additionally the number of time words like "Gamestop" is used is also considered in calcuation

This information will be overlaid with the daily stock price for gamestop

## Technologies Used
* MongoDB
* PRAW API
* PushShift API
* Docker
* Postgres
* Matplotlib
* Pandas


### Citations:
1.  Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014
2.  “Yahoo Finance - Stock Market Live, Quotes, Business &amp; Finance News.” Yahoo! Finance, Yahoo!, finance.yahoo.com/.
3.  “Subreddit Stats.” Subreddit Stats - Statistics for Every Subreddit, subredditstats.com/r/wallstreetbets. 
