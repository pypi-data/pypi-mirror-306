from collections import defaultdict

from .ranking import Ranking
from .user_items import UserItems

class BordaCount:
    def __init__(self, borda_items: list, factor: int):
        self.user_items_list = [UserItems(user_items) for user_items in borda_items]
        self.distribution_factor = factor
        self.final_ranking = defaultdict(lambda: {'item': '', 'final_rank': 0})
        self.all_items_names = []
        self.collect_all_items_names()
        self.initialize_items()
        self.compute_borda_ranking()

    def compute_borda_ranking(self) -> None:
        # borda rank per user
        for user_items in self.user_items_list:
            user = Ranking(user_items, self.distribution_factor)
            user.rank_items()
            # sum ranks for respective items
            for i in range(len(self.final_ranking)):
                for item_data in user_items.get_items_data().values():
                    if self.final_ranking[i]['item'] in item_data['items']:
                        self.final_ranking[i]['final_rank'] += item_data['rank']

    def borda_result(self) -> dict:
        result_dict = {}
        for item_result in self.final_ranking.values():
            result_dict[item_result['item']] = item_result['final_rank']
        return dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))

    def initialize_items(self) -> None:
        for i, item_name in enumerate(self.all_items_names):
            self.final_ranking[i]['item'] = item_name

    def collect_all_items_names(self) -> None:
        for user_items in self.user_items_list:
            self.all_items_names = list(set(self.all_items_names + user_items.get_items_names()))
