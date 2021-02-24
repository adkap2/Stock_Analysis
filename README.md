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
    * Null Hypothesis: WallStreetBets did not influence Gamestop stock value
    * Alternate Hypothesis: WallStreetBets did influence GameStop stock value

2.  
    * Null Hypothesis: No significant correlation between GameStop stock value and WallStreetBets subscriber count
    * Alternative Hypothesis: Gamestop stock value influenced WallStreetBets subscriber count







### Monday's Work
Current collecting comment data for WallStreetBets posts between Jan 1st
and Feb 22 2021. So far, able to collect a max of 15k comments per post. 
Posts with above 80k stop the server from scraping entirely. 

Data is then inputted into a sentiment analyzer where postive/negative sentiment levels are provided for each day.

Additionally the number of time words like "Gamestop" is used is also considered in calcuation

This information will be overlaid with the daily stock price for gamestop

## Technologies Used
* MongoDB
* Reddit PRAW API
* PushShift API
* Docker
* Postgres
* Matplotlib
* Pandas


### Citations:
1.  Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014
2.  “Yahoo Finance - Stock Market Live, Quotes, Business &amp; Finance News.” Yahoo! Finance, Yahoo!, finance.yahoo.com/.
3.  “Subreddit Stats.” Subreddit Stats - Statistics for Every Subreddit, subredditstats.com/r/wallstreetbets. 
