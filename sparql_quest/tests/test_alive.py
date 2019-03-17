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
from dateutil.relativedelta import relativedelta
import pytest

from sparql_quest.sparql_util import sparql_util


@pytest.mark.alive
def test_alive():
    """
    Test case to ensure that the testTool works.

    .. code-block:: none

       pytest tests/test_tool.py
    """
    assert True


@pytest.mark.age
def test_age_query():
    """
    Test to ensure theprivate function _get_age works
    """
    print("Get Age")
    today = datetime.today()
    dc_age = relativedelta(today, datetime.strptime('1966-10-09', '%Y-%m-%d'))
    tb_age = relativedelta(today, datetime.strptime('1953-05-06', '%Y-%m-%d'))

    su_handle = sparql_util()
    assert su_handle._get_age('Tony Blair') == tb_age.years  # pylint: disable=protected-access
    assert su_handle._get_age('David Cameron') == dc_age.years  # pylint: disable=protected-access


@pytest.mark.birthname
def test_birthname_query():
    """
    Test to ensure theprivate function _get_age works
    """
    print("Get Birth Name")
    su_handle = sparql_util()
    assert su_handle._get_birth_name('Tony Blair') == 'Anthony Charles Lynton Blair'  # pylint: disable=protected-access
    assert su_handle._get_birth_name('David Cameron') == 'David William Donald Cameron'  # pylint: disable=protected-access


@pytest.mark.scibite
def test_do_sparql_query():
    """
    Tests that need to pass
    """
    su_handle = sparql_util()
    assert su_handle.do_sparql_query("How old is David Cameron") == 52
    assert su_handle.do_sparql_query("How old is Tony Blair") == 65
    assert su_handle.do_sparql_query(
        "What is the birth name of Tony Blair ?"
    ) == "Anthony Charles Lynton Blair"
