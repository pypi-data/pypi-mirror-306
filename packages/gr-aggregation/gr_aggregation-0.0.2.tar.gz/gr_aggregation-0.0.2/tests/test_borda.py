import pytest
from src.gr_aggregation.aggregation import start_borda_count

@pytest.fixture
def group_data_2():
    """Data for group of 2 users"""
    new_data = [
        {'40': '2', '100': '3', '104': '5', '126': '3', '441': '3', '1137': '3', '5602': '5', '19003': '5', '36557': '5', '133313': '4'},
        {'40': '5', '100': '5', '104': '5', '126': '3', '441': '1', '1137': '2', '5602': '2', '19003': '5', '36557': '4', '133313': '4'}
    ]
    return new_data
    
def test_borda_1(group_data_2):
    assert start_borda_count(group_data_2, 2) == {'104': 17.0, '19003': 17.0, '36557': 14.0, '100': 12.0, '133313': 11.5, '5602': 11.0, '40': 9.5, '126': 7.5, '1137': 6.0, '441': 4.5}
