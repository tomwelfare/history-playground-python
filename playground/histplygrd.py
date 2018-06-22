import requests
import json
import itertools as itr

class Playground():

	def __init__(self):
		self._baseUrl = 'http://playground.enm.bris.ac.uk/' # protected
		self.__authToken = None # private

	def login(self, email, password):
		'''Authenticate the user to use the History Playground.
		Stores the authentication token in the Playground object.
		@param self: Playground object
		@param email: Email address used to register on the History Playground
		@param password: Password associated with email address when registering
		'''
		session = requests.Session()
		payload = {'email':email,'password':password}
		data = session.post(self._baseUrl + 'auth', data = payload).json()
		if 'token' in data:
			self.__authToken = data['token']
		else:
			self.__authToken = None
			print('Failed to login.')	


	def query(self, queries, datasets, **kwargs):
		'''Queries the History Playground for the given queries in 
		each of the datasets specified
		@param self: Playground object
		@param queries: n-gram query terms to search for
		@param datasets: datasets to search against
		@return: List of dictionaries containing the time series
		'''
		if self.__authToken != None:
			session = requests.Session()
			headers = {
				'Authorization' : 'Bearer ' + self.__authToken, 
				'Content-Type': 'application/json; charset=UTF-8'
			}
			payload = {
				'corpora':datasets,
				'terms': self.__parseTerms(queries,datasets), 
				'display':[kwargs.pop('display','rank')],
				'lang':self.__expand(['english'],datasets),
				'dateFormat':self.__expand(['YYYY'],datasets),
				'interval':self.__expand(['1'],datasets),
				'resolution':self.__expand(['years'],datasets),
				'minDate':kwargs.pop('minDate', ''),
				'maxDate':kwargs.pop('maxDate', ''),
				'smooth':kwargs.pop('smooth', False),
				'confidence':kwargs.pop('confidence', False),
				'bestFit':kwargs.pop('bestfit', False),
				'detrend':kwargs.pop('detrend', False),
				'diff':kwargs.pop('diff', False),
				'zscore':kwargs.pop('standardize', False),
				'multiterm':kwargs.pop('multiterm', False),
				'changepoints':kwargs.pop('changepoints', False)}
			data = session.post(self._baseUrl + 'ngram', headers=headers, data = json.dumps(payload))
			return data.json()
		else:
			print('Please login first.')

	def availableDatasets(self):
		'''Returns a list of the available datasets that the user can query against to compute time series.
		@return: list of datasets which can be queried
		'''
		return ['bna','caa']

	def describeDataset(self, dataset):
		'''Returns a human-readable description of the dataset
		@return: String describing the dataset
		'''
		switch = {
			'bna': 'British Newspaper Archive (bna).',
			'caa': 'Chronicling America Archive (caa).'
		}
		return switch.get(dataset, 'Invalid dataset')

	def __parseTerms(self,queries, datasets):
		return [str(q + ':' + d) for q in queries for d in datasets]
	
	def __expand(self, list, datasets):
		return list * len(datasets)