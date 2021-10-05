import random
from string import ascii_lowercase
from urllib import parse
from ip_handler import IPHandler
import wordlists
import attacks
import sys


def handlebar_replace(string, session):
    while "__" in string:
        # Keep looping until all recursive replacements done
        if "__rand_digit__" in string:
            string = replace_rand_digit(string)
        if "__rand_int__" in string:
            string = replace_rand_int(string)
        if "__rand_long__" in string:
            string = replace_rand_long(string)
        if "__inc_int__" in string:
            string = replace_inc_int(string, session.iter)
        if "__rand_str__" in string:
            string = replace_rand_string(string)
        if "__rand_css_file__" in string:
            string = replace_css_file(string)
        if "__rand_js_file__" in string:
            string = replace_js_file(string)
        if "__rand_cmd_recon__" in string:
            string = replace_cmd_recon(string)
        if "__rand_cmd_attack__" in string:
            string = replace_cmd_attack(string)
        if "__rand_geo_ip__" in string:
            string = replace_ip(string, session)
        if "__rand_sticky_str__" in string:
            string = replace_sticky_str(string, session)
        if "__theme__" in string:
            string = replace_theme(string, session)
        if "__rand_two_words__" in string:
            string = replace_rand_two_words(string)
        if "__rand_app_page_name__" in string:
            string = replace_rand_app_page_name(string, session)
        if "__app_extension__" in string:
            string = replace_app_extension(string, session)
        if "__rand_noise__" in string:
            string = replace_rand_noise(string, session)
        if "__rand_img_ext__" in string:
            string = replace_img_extension(string)
    return string


def replace_rand_digit(param):
    return param.replace("__rand_digit__", "{}".format(random.randint(1, 9)))


def replace_rand_int(param):
    return param.replace("__rand_int__", "{}".format(random.randint(0, 50)))


def replace_rand_long(param):
    return param.replace("__rand_long__", "{}".format(random.randint(100000, 999999)))


def replace_inc_int(param, num):
    return param.replace("__inc_int__", "{}".format(num))


def replace_rand_string(param):
    return param.replace(
        "__rand_str__", "".join(random.choice(ascii_lowercase) for i in range(8))
    )


def replace_cmd_recon(param):
    payload = param.replace("__rand_cmd_recon__", random.choice(attacks.command_recon))
    return parse.quote_plus(payload)


def replace_cmd_attack(param):
    payload = param.replace(
        "__rand_cmd_attack__", random.choice(attacks.command_attack)
    )
    return parse.quote_plus(payload)


def replace_ip(param, session):
    return param.replace("__rand_geo_ip__", IPHandler.get_random_ip(session.geo))


def replace_sticky_str(param, session):
    if not session.stickystr:
        session.stickystr = replace_rand_string("__rand_str__")
    return param.replace("__rand_sticky_str__", session.stickystr)


def replace_css_file(param):
    return param.replace("__rand_css_file__", random.choice(wordlists.common_css_files))


def replace_js_file(param):
    return param.replace("__rand_js_file__", random.choice(wordlists.common_js_files))


def replace_img_extension(param):
    return param.replace("__rand_img_ext__", random.choice(wordlists.images_extensions))


def replace_rand_two_words(param):
    rand_string = "-".join(
        [
            random.choice(wordlists.colours),
            random.choice(wordlists.nouns),
        ]
    )
    return param.replace("__rand_two_words__", rand_string)


def replace_app_extension(param, session):
    return param.replace("__app_extension__", session.app.extension)


def replace_rand_app_page_name(param, session):
    if session.pages != None:
        return param.replace("__rand_app_page_name__", random.choice(session.pages))
    else:
        return param.replace(
            "__rand_app_page_name__", random.choice(wordlists.webpages)
        )


def replace_rand_noise(param, session):
    if session.noise != None:
        return param.replace("__rand_noise__", random.choice(session.noise))
    else:
        return param.replace("__rand_noise__", random.choice(wordlists.noise))


# Theme is run specific so store it here for convenience
this = sys.modules[__name__]
theme = False


def replace_theme(param, session):
    theme = this.theme
    if this.theme:
        return param.replace("__theme__", this.theme)
    if session.theme != None:
        this.theme = session.theme
    else:
        this.theme = handlebar_replace("__rand_two_words__", session)
    return param
