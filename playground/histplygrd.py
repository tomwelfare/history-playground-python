import requests
import json
import itertools as itr

class Playground():

	def __init__(self):
		self._base_url = 'http://playground.enm.bris.ac.uk/'
		self.__auth_token = None

	def login(self, email, password):
		'''Authenticate the user to use the History Playground. Stores the 
		authentication token in the Playground object.
		@param self: Playground object
		@param email: Email address used to register on the History Playground
		@param password: Password associated with email address when registering
		'''
		session = requests.Session()
		payload = {'email':email,'password':password}
		data = session.post(self._base_url + 'auth', data = payload).json()
		if 'token' in data:
			self.__auth_token = data['token']
		else:
			self.__auth_token = None
			print('Failed to login.')	


	def query(self, query_data, **kwargs):
		'''Queries the History Playground for the given queries in each of the
		datasets specified
		@param self: Playground object
		@param queries: n-gram query terms to search for
		@param datasets: datasets to search against
		@return: List of dictionaries containing the time series
		'''
		if self.__auth_token != None:
			session = requests.Session()
			headers = {
				'Authorization' : 'Bearer ' + self.__auth_token, 
				'Content-Type': 'application/json; charset=UTF-8'
			}
			payload = {
				'corpora': query_data[1],
				'terms': self.__annotate_terms(query_data), 
				'display':[kwargs.pop('display','rank')],
				'lang':self.__expand(['english'], query_data[1]),
				'dateFormat':self.__expand(['YYYY'], query_data[1]),
				'interval':self.__expand(['1'], query_data[1]),
				'resolution':self.__expand(['years'], query_data[1]),
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
			data = session.post(self._base_url + 'ngram', headers=headers, data = json.dumps(payload))
			return data.json()
		else:
			print('Please login first.')

	def available_datasets(self):
		'''Returns a list of the available datasets that the user can query against to compute time series.
		@return: list of datasets which can be queried
		'''
		return ['bna','caa']

	def describe_dataset(self, dataset):
		'''Returns a human-readable description of the dataset
		@return: String describing the dataset
		'''
		switch = {
			'bna': 'British Newspaper Archive (bna).',
			'caa': 'Chronicling America Archive (caa).'
		}
		return switch.get(dataset, 'Invalid dataset')

	def __annotate_terms(self, query_data):
		'''Append each corpus name to each query'''
		return [str(q + ':' + d) for q in query_data[0] for d in query_data[1]]
	
	def __expand(self, list, datasets):
		'''Duplicate entries in list so that the API accepts it'''
		return list * len(datasets)
