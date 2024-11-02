from .user_items import UserItems


class Ranking:
    def __init__(self, user_items: UserItems, factor: int) -> None:
        self.user_items = user_items
        self.distribution_factor = factor

    def rank_items(self) -> None:
        current_points = 1
        for items_rating, items_data in self.user_items.get_items_data().items():
            items_count = len(items_data['items'])
            rank = self.calculate_rank(current_points, items_count)
            self.user_items.get_items_data()[items_rating]['rank'] = rank
            current_points += items_count

    def calculate_rank(self, current_points: int, same_rating_count: int):
        return current_points + (same_rating_count - 1) / self.distribution_factor
