class Pages:
    item_count_per_page = 25
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'active_session'):
            self.active_session = {}

    def remove_user(self, user_id):
        try:
            del self.active_session[user_id]
        except KeyError:
            pass

    def add_user(self, data, user_id):
        self.active_session[user_id] = [data,0]

    def index_increment_plus(self, user_id):
        index = self.active_session[user_id]
        index[1] += 1


    def index_increment_minus(self, user_id):
        index = self.active_session[user_id]
        index[1] -= 1

        if index[1] < 0:
            self.active_session[user_id][1] = 0


    def make_page(self, user_id):
        return self.__make_page(self.active_session.get(user_id)[0], self.active_session.get(user_id)[1])

    def __make_page(self, data, page_index=0):
        output = ""

        at = Pages.item_count_per_page * page_index
        to = at + Pages.item_count_per_page
        for index in range(at, to):
            try:
                output += data[index].row_in_array()
            except IndexError:
                break
        return [output]