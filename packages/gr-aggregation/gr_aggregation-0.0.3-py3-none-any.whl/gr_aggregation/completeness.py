from collections import Counter
from math import sqrt


class Completeness:
    def __init__(self, items: list[dict], weight: int) -> None:
        self.items = items
        self.items_ids = set(self.items[0].keys()) # takes the first preferences row
        self.total_users = len(items)
        self.total_items = len(self.items_ids)
        self.weight = weight

    # this should be for all aggregation methods also 
    def check_all_items(self) -> bool:
        for preferences in self.items:
            check = Counter(preferences.keys()) == Counter(self.items_ids)
            if not check:
                raise Exception
        return True

    def item_completeness(self, item_id):
        sum_satisfaction = 0
        
        for user_preferences in self.items:
            rating = user_preferences.get(item_id)  
            if not rating:
                raise Exception
            sum_satisfaction += self.item_satisfaction(rating)

        sum_preferences = self.total_users * sqrt(self.total_items)

        return round(sum_satisfaction/sum_preferences, 3)

    def item_satisfaction(self, rating):
        satisfaction = sqrt(rating) 
        # TODO: give specific weight to a user
        satisfaction = self.weight * satisfaction
        return satisfaction

    def completeness_result(self, sort: bool | None = None) -> dict: 
        item_satisfaction = dict()

        for item_id in self.items_ids:
            item_satisfaction[item_id] = self.item_completeness(item_id)
    
        if sort:
            item_satisfaction = dict(sorted(item_satisfaction.items(), key=lambda item: item[1], reverse=True))

        return item_satisfaction 
