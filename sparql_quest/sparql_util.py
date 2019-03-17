"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from __future__ import print_function

from datetime import datetime
import re
import requests

from dateutil.relativedelta import relativedelta


class sparql_util():  # pylint: disable=invalid-name,too-few-public-methods
    """
    Tool for running indexers over a genome FASTA file
    """

    def __init__(self):
        """
        Initialise the tool with its configuration.


        Parameters
        ----------
        configuration : dict
            a dictionary containing parameters that define how the operation
            should be carried out, which are specific to each Tool.
        """
        print("sparql_util")

        self.common_headers = {
            'ContentType': 'application/sparql-results+json',
            'Accept': 'application/json'
        }

        self.common_url = 'http://live.dbpedia.org/sparql/sparql?query='

    def do_sparql_query(self, question):
        """
        do_sparql_query

        Parameters
        ----------
        file_loc : str
            Location of the genome assembly FASTA file
        idx_loc : str
            Location of the output index file
        """

        re_list = {
            'age': re.compile(r'How\ old\ is\ (\w+\ \w+)'),
            'name': re.compile(r'What.+birth\sname.+\s(\w+\ \w+)')
        }

        for pattern in re_list:
            m = re_list[pattern].match(question)
            if m and pattern == 'age':
                return self._get_age(m.group(1))
            elif m and pattern == 'name':
                return self._get_birth_name(m.group(1))

        return True

    def _get_age(self, person):
        """
        _get_age

        Parameters
        ----------
        person : str
            Name of the person

        Returns
        -------
        age : integer
            Age of the person in years
        """

        name_query = person.replace(' ', '_')
        url_query = self.common_url + (
            'SELECT+?dob+FROM+<http://dbpedia.org>+WHERE+{dbr:'
            + name_query
            + '+dbp:birthDate+?dob+.+}+LIMIT+1'
        )

        try:
            req = requests.get(url_query, headers=self.common_headers)
            req_json = req.json()
            dob = req_json['results']['bindings'][0]['dob']['value']

            born = datetime.strptime(dob, '%Y-%m-%d')
            today = datetime.today()

            age = relativedelta(today, born)
            return age.years

        except requests.exceptions.RequestException as err:
            print(err)
            return False

        return False

    def _get_birth_name(self, person):
        """
        _get_birth_name

        Parameters
        ----------
        person : str
            Name of the person

        Returns
        -------
        birth_name : str
            Full name of the person when they were born
        """
        name_query = person.replace(' ', '_')
        url_query = self.common_url + (
            'SELECT+?name+FROM+<http://dbpedia.org>+WHERE+{dbr:' + name_query
            + '+?p+?name+.+dbr:' + name_query
            + '+?p+?name+.+FILTER+(?p+IN+(dbp:birthname,+dbp:birthName)+)}+LIMIT+1'
        )

        try:
            req = requests.get(url_query, headers=self.common_headers)
            req_json = req.json()
            return req_json['results']['bindings'][0]['name']['value']

        except requests.exceptions.RequestException as err:
            print(err)

        return False
