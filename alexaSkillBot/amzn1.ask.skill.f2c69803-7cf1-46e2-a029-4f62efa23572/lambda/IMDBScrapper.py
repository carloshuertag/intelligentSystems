"""
Authors: Juan Jose Urioste (@juanurioste), Carlos Huerta García (@huerta2502)
Date: February 17, 2023

This script gets movie info from IMDB.
"""

import requests
import re
from collections import defaultdict

cache = defaultdict(bool)

def getMovieInfo(movie_title):
    if cache[movie_title] == False:
        cache[movie_title] = requestMovieInfo(movie_title)
    return cache[movie_title]

def requestMovieInfo(title: str):
    """ Gets movie info from IMDB """
    searchHtml = searchMovie(title)
    movieId = getMovieId(searchHtml)
    movieHtml = getMovieContent(movieId)
    movie = getMovie(movieHtml)
    movie['title'] = title
    return movie

def searchMovie(title: str) -> str:
    """ Searches for a movie on IMDB """
    urlstart = 'https://www.imdb.com/find/?q='
    urlend = '&ref_=nv_sr_sm'
    url = urlstart + title + urlend
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return response.content.decode('utf-8')

def getMovieId(htmlContent: str) -> str:
    """ Gets the movie id from the search results """
    regex = '.*?href="/title/(.*?)/'
    matches = re.search(regex, htmlContent, re.DOTALL)
    return matches.group(1)

def getMovieContent(movieId: str) -> str:
    """ Gets the movie content from the movie id """
    urlstart = 'https://www.imdb.com/title/'
    urlend = '/?ref_=fn_al_tt_1'
    url = urlstart + movieId + urlend
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return response.content.decode('utf-8')

def getMovie(htmlContent: str):
    """ Gets the movie info from the movie content """
    movie = {}
    movie['duration'] = getMovieDuration(htmlContent)
    movie['rating'] = getMovieRating(htmlContent)
    movie['votes'] = getMovieVotes(htmlContent)
    movie['plot'] = getMoviePlot(htmlContent)
    movie['director'] = getMovieDirector(htmlContent)
    return movie

def getMovieDuration(htmlContent: str) -> str:
    """ Gets the movie duration from the movie content """
    durationRegex = '</li><li role="presentation" class="ipc-inline-list__item">(.*?)</li></ul></div><div';
    durationMatches = re.search(durationRegex, htmlContent, re.DOTALL)
    duration = durationMatches.group(1)
    duration = duration[(len(duration) - 6):len(duration)]
    hours = duration[0:duration.index('h')]
    minutes = duration[(duration.index('h') + 1):duration.index('m')]
    return hours + ' hours and ' + minutes + ' minutes'

def getMovieRating(htmlContent: str) -> str:
    """ Gets the movie rating from the movie content """
    ratingRegex = '<span class="sc-bde20123-1 iZlgcd">(.*?)</span>'
    ratingMatches = re.search(ratingRegex, htmlContent, re.DOTALL)
    return ratingMatches.group(1)

def getMovieVotes(htmlContent: str) -> str:
    """ Gets the movie votes from the movie content """
    votesRegex = '<div class="sc-bde20123-3 bjjENQ">(.*?)</div>'
    votesMatches = re.search(votesRegex, htmlContent, re.DOTALL)
    return votesMatches.group(1)

def getMoviePlot(htmlContent: str) -> str:
    """ Gets the movie plot from the movie content """
    plotRegex = '<span role="presentation" data-testid="plot-l" class="sc-5f699a2-1 cfkOAP">(.*?)</span>'
    plotMatches = re.search(plotRegex, htmlContent, re.DOTALL)
    return plotMatches.group(1)

def getMovieDirector(htmlContent: str) -> str:
    """ Gets the movie director from the movie content """
    directorRegex = '<div class="ipc-metadata-list-item__content-container">(.*?)</div>'
    directorMatches = re.search(directorRegex, htmlContent, re.DOTALL)
    directorsString = re.sub("<.*?>", " ", directorMatches.group(1))
    directorsNames = list(filter(lambda x: x != '', directorsString.split()))
    directors = []
    for i in range(0, len(directorsNames), 2):
        directors.append(directorsNames[i] + ' ' + directorsNames[i + 1])
    return directors
