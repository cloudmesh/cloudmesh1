from map_progress import HeatMapProgress, ServiceMapProgress

from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)

TYPE_RACK_TEMPERATURE = "temperature"
TYPE_RACK_SERVICE = "service"

# type and class pair
type_class_dict = {
    TYPE_RACK_TEMPERATURE: HeatMapProgress,
    TYPE_RACK_SERVICE: ServiceMapProgress,
}

# global unique instance
# support multi user
unique_progress_instance = None


def get_temperature_progress(username):
    return get_progress(username, TYPE_RACK_TEMPERATURE)


def get_service_progress(username):
    return get_progress(username, TYPE_RACK_SERVICE)


def get_progress(username, str_type):
    result = None
    if username:
        progress_dict = get_progress_dict(username)
        if progress_dict and str_type in progress_dict:
            result = progress_dict[str_type]
    return result


def get_progress_dict(username):
    global unique_progress_instance

    if unique_progress_instance is None:
        unique_progress_instance = {}
    if username not in unique_progress_instance:
        unique_progress_instance[username] = {}
        for type_name in type_class_dict:
            unique_progress_instance[username][
                type_name] = type_class_dict[type_name]()
    return unique_progress_instance[username]

# usage
if __name__ == "__main__":
    heat_progress = get_temperature_progress("username")
    heat_progress.set_load_map()
    heat_progress.set_send_http_request()
