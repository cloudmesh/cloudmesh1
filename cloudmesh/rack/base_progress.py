from time import sleep


class BaseProgress:
    # literal text of the status
    status_text = None
    # value of 100 of the status
    status_value = 0
    # next status
    next_status = None
    # data
    data_dict = {}

    def __init__(self):
        self.clear_status()

    # get/set/clear status
    def get_status(self):
        return {"text": self.status_text, "value": self.status_value, "next": self.next_status}

    def set_status(self, text, value, next):
        self.set_status_text(text)
        self.set_status_value(value)
        self.set_next_status(next)
        # sleep 50 ms, other thread can have a chance to get status
        sleep(0.05)

    def set_error_status(self):
        self.set_status("error", -1, self.next_status)

    def clear_status(self):
        self.status_text = ""
        self.status_value = 0
        self.next_status = ""

    # get status text/value
    def get_status_text(self):
        return self.status_text

    def get_status_value(self):
        return self.status_value

    def get_next_status(self):
        return self.next_status

    # set status text/value
    def set_status_text(self, text=None):
        self.status_text = text if text else ""

    def set_status_value(self, value=0):
        if value < 0:
            value = 0
        if value > self.status_value:
            self.status_value = value

    def set_next_status(self, text=None):
        self.next_status = text if text else ""

    # clear/set/update/get data
    def clear_data(self, name):
        if name in self.data_dict:
            self.data_dict[name] = {}

    # value should be a dict
    def set_data(self, name, value):
        self.clear_data(name)
        self.data_dict[name] = value

    def update_data(self, name, value):
        if name not in self.data_dict:
            return self.set_data(name, value)
        for attr in value:
            self.data_dict[name][attr] = value[attr]

    def get_data(self, name, attr=None):
        if name not in self.data_dict:
            return None
        if attr and attr in self.data_dict[name]:
            return self.data_dict[name][attr]
        else:
            return self.data_dict[name]
