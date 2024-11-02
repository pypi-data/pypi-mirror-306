class UserItems:
    def __init__(self, user_ratings: dict) -> None:
        self.user_items = {}
        self.transform_data(user_ratings)

    def transform_data(self, user_ratings: dict) -> None:
        # sort items by ascending rating
        sorted_ratings = sorted(user_ratings.items(), key=lambda item: item[1])
        # fill items data
        for rank, (item_name, rating) in enumerate(sorted_ratings, start=1):
            item_info = self.user_items.setdefault(rating, {'items': [], 'rank': rank, 'rating': rating})
            item_info['items'].append(item_name)

    def get_item_rank(self, target_item: str) -> int:
        for item_data in self.user_items.values():
            if target_item in item_data['items']:
                return item_data['rank']
        return 0

    def get_items_data(self) -> dict:
        return self.user_items

    def get_items_names(self) -> list:
        item_names = set()
        for item_info in self.user_items.values():
            item_names.update(item_info['items'])
        return list(item_names)
