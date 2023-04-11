from random import randint
from models import ActivityPattern, Interaction
import interactions
from copy import copy


def one_in_x_chance_of(x):
    return randint(0, x) == x


def x_in_hundred_chance_of(x):
    result = randint(0, 100) < x
    return result


class Banking:
    static_navigate_to_transactions = ActivityPattern(
        consecutive=True
    ).add_interactions(
        [interactions.dynamic.account_status, interactions.dynamic.transaction]
    )
    static_browse_transactions_short = ActivityPattern(count=5).add_interaction(
        interactions.dynamic.transaction
    )
    static_browse_transactions = ActivityPattern().add_interaction(
        interactions.dynamic.transaction
    )
    static_transfer = ActivityPattern(consecutive=True).add_interactions(
        [
            interactions.dynamic.transfer_get_success,
            interactions.dynamic.transfer_post_success,
            interactions.dynamic.transfer_complete_success,
        ]
    )

    @staticmethod
    def dynamic_routine_use():
        gohome = copy(Misc.static_home_page)
        gohome.count = randint(2, 8)
        yield gohome
        yield Misc.static_home_page
        if one_in_x_chance_of(15):
            yield Misc.static_faq
        if one_in_x_chance_of(10):
            for i in range(0, randint(1, 3)):
                yield Misc.static_login_failed
        yield Misc.static_login
        yield Banking.static_navigate_to_transactions
        browse = copy(Banking.static_browse_transactions)
        browse.count = randint(1, 6)
        yield browse
        if one_in_x_chance_of(6):
            yield Banking.static_transfer
        if one_in_x_chance_of(20):
            yield Misc.static_password_reset
        if one_in_x_chance_of(50):
            yield Misc.static_change_avatar
        if one_in_x_chance_of(3):
            yield Misc.static_logout

    @staticmethod
    def dynamic_brute_force():
        for ap in Misc.dynamic_brute_force():
            yield ap
        browse = copy(Banking.static_browse_transactions)
        browse.count = randint(1, 6)
        yield browse
        for i in range(0, 6):
            yield Banking.static_transfer
        yield Misc.static_logout


class Misc:
    static_root = ActivityPattern(consecutive=True).add_interaction(
        interactions.misc.root_success
    )
    static_favico = ActivityPattern(consecutive=True).add_interaction(
        interactions.misc.favico_success
    )
    static_home_page = ActivityPattern(consecutive=True).add_interaction(
        interactions.dynamic.index_success
    )
    noise = [
        interactions.misc.favico_success,
        interactions.css.main_success,
        interactions.css.template_success,
        interactions.css.footer_success,
        interactions.css.rand_success,
        interactions.css.rand_success,
        interactions.js.rand_success,
        interactions.css.rand_not_found,
    ]
    static_login_page = ActivityPattern(consecutive=True).add_interaction(
        interactions.dynamic.index_redirect
    )
    static_login = ActivityPattern(consecutive=True).add_interactions(
        [
            interactions.dynamic.index_redirect,
            interactions.dynamic.login_success,
            interactions.dynamic.login_post_301,
        ]
    )
    static_password_reset = ActivityPattern(consecutive=True).add_interactions(
        [
            interactions.dynamic.change_password_get_success,
            interactions.dynamic.change_password_post_success,
            interactions.dynamic.account_status,
        ]
    )
    static_logout = ActivityPattern(consecutive=True).add_interaction(
        interactions.dynamic.logout_success
    )
    static_login_failed = ActivityPattern(
        consecutive=True, min_period_between_invocations_s=1
    ).add_interaction(interactions.dynamic.login_post_401)

    static_faq = ActivityPattern(consecutive=True).add_interaction(
        interactions.dynamic.faq_success
    )

    static_change_avatar = ActivityPattern(consecutive=True).add_interactions(
        [
            interactions.dynamic.account_status,
            interactions.dynamic.change_avatar_post_success,
            interactions.dynamic.account_status,
        ]
    )

    @staticmethod
    def dynamic_brute_force():
        yield Misc.static_login_page
        yield ActivityPattern(
            max_period_between_invocations_s=3,
            min_period_between_invocations_s=1,
            count=randint(0, 300),
            suppress_noise=True,
        ).add_interaction(interactions.dynamic.login_post_401)
        yield ActivityPattern(
            consecutive=True,
            max_period_between_invocations_s=3,
            min_period_between_invocations_s=1,
            suppress_noise=True,
        ).add_interaction(interactions.dynamic.login_post_301)

    @staticmethod
    def dynamic_cmd_injectiom():
        # Login
        yield Misc.static_login
        # view FAQ page a few times
        for i in range(0, 3):
            yield Misc.static_faq
        # change avataer a few times trying to get lfi
        for i in range(1, 5):
            yield Misc.static_change_avatar
            yield ActivityPattern(consecutive=True).add_interaction(
                interactions.dynamic.faq_lfi
            )
        yield ActivityPattern(
            count=(randint(4, 8)), suppress_noise=True
        ).add_interaction(interactions.dynamic.cmd_injection_on_sticky_page_recon)
        yield ActivityPattern(
            count=(randint(1, 2)), suppress_noise=True
        ).add_interaction(interactions.dynamic.cmd_injection_on_sticky_page_attack)


class Wordpress:
    noise = [
        interactions.css.wp_theme_versioned_success,
        interactions.css.wp_versioned_success,
        interactions.js.wp_theme_versioned_success,
        interactions.js.wp_versioned_success,
        interactions.misc.wp_jpg_success,
        interactions.dynamic.xmlrpc_success,
    ]

    static_random_page = ActivityPattern(consecutive=True, count=1).add_interactions(
        [
            interactions.misc.wp_page_success,
            interactions.dynamic.index_seo_friendly_success,
            interactions.dynamic.index_seo_friendly_success,
            interactions.dynamic.index_seo_friendly_success,
        ]
    )

    static_login_page_success = ActivityPattern(consecutive=True).add_interaction(
        interactions.dynamic.wp_admin_login_page_success
    )

    static_login_success = ActivityPattern(consecutive=True).add_interaction(
        interactions.dynamic.wp_admin_login_success
    )
    static_login_failed = ActivityPattern(consecutive=True).add_interaction(
        interactions.dynamic.wp_admin_login_failed
    )

    static_admin_pages = ActivityPattern(
        min_period_between_invocations_s=10,
        max_period_between_invocations_s=120,
        count=10,
    ).add_interactions(
        [
            interactions.dynamic.wp_admin_update_success,
            interactions.dynamic.wp_admin_users_success,
            interactions.dynamic.wp_admin_plugins_success,
            interactions.dynamic.wp_admin_plugins_install_success,
            interactions.dynamic.wp_admin_health_success,
        ]
    )

    static_add_plugin = ActivityPattern(
        consecutive=True,
    ).add_interactions(
        [
            interactions.dynamic.wp_admin_plugins_success,
            interactions.dynamic.wp_admin_plugins_install_post_success,
        ]
    )

    static_add_user = ActivityPattern(
        consecutive=True,
    ).add_interactions(
        [
            interactions.dynamic.wp_admin_users_success,
            interactions.dynamic.wp_admin_users_post_success,
        ]
    )

    @staticmethod
    def dynamic_browse():
        if x_in_hundred_chance_of(x=9):
            # 9/10 chance of coming in via index page
            yield Misc.static_root
        if x_in_hundred_chance_of(x=6):
            yield Misc.static_favico
        for i in range(1, randint(3, 8)):
            yield Wordpress.static_random_page

    @staticmethod
    def dynamic_admin():
        if x_in_hundred_chance_of(x=50):
            # 5/10 chance of arriving via root
            yield Misc.static_root
        yield Wordpress.static_login_page_success
        if x_in_hundred_chance_of(x=20):
            # 2/10 chance of password failed
            yield Wordpress.static_login_failed
        # Login OK
        yield Wordpress.static_login_success
        # Do some read-only admin things
        admin_activity = copy(Wordpress.static_admin_pages)
        admin_activity.count = randint(2, 8)
        yield admin_activity
        # Maybe do some other things
        if x_in_hundred_chance_of(x=20):
            yield Wordpress.static_add_user
            return
        if x_in_hundred_chance_of(x=20):
            yield Wordpress.static_add_plugin
            return

    @staticmethod
    def dynamic_browse_or_admin():
        if x_in_hundred_chance_of(x=5):
            pattern = Wordpress.dynamic_admin
        else:
            pattern = Wordpress.dynamic_browse
        for i in pattern():
            yield i

    @staticmethod
    def dynamic_brute_force():
        yield ActivityPattern(
            max_period_between_invocations_s=3,
            min_period_between_invocations_s=1,
            count=randint(100, 300),
            suppress_noise=True,
        ).add_interaction(interactions.dynamic.wp_admin_login_failed)
        # Login OK
        yield Wordpress.static_login_success
        yield Wordpress.static_admin_pages
        yield Wordpress.static_add_user

    @staticmethod
    def dynamic_malicious_plugin():
        # Login
        yield Wordpress.static_login_page_success
        yield Wordpress.static_login_success
        yield Wordpress.static_admin_pages
        # upload plugin a few times to try and get the backdoor
        for i in range(1, 5):
            yield Wordpress.static_add_plugin
        yield ActivityPattern(
            count=(randint(4, 8)), suppress_noise=True
        ).add_interaction(interactions.dynamic.cmd_injection_on_sticky_page_recon)
        yield ActivityPattern(
            count=(randint(1, 2)), suppress_noise=True
        ).add_interaction(interactions.dynamic.cmd_injection_on_sticky_page_attack)


class Generic:
    static_page_success = ActivityPattern(consecutive=True).add_interaction(
        interactions.generic.seo_friendly_success
    )

    static_page_404 = ActivityPattern(consecutive=True).add_interaction(
        interactions.generic.seo_friendly_404
    )

    old_loot_success = ActivityPattern(
        consecutive=True, suppress_noise=True
    ).add_interaction(interactions.generic.old_loot_success)

    old_loot_404 = ActivityPattern(suppress_noise=True).add_interaction(
        interactions.generic.old_loot_404
    )
    static_noise_success = [interactions.generic.noise_sucess]

    @staticmethod
    def dynamic_browse():
        if x_in_hundred_chance_of(x=9):
            # 9/10 chance of coming in via index page
            yield Misc.static_root
        if x_in_hundred_chance_of(x=6):
            # 6/10 chance of fetching favico
            yield Misc.static_favico
        if x_in_hundred_chance_of(x=10):
            yield Generic.static_page_404
            yield Misc.static_root
        for i in range(1, randint(2, 12)):
            yield Generic.static_page_success

    @staticmethod
    def dynamic_bruteforce_sensitive_files():
        Generic.old_loot_404.min_period_between_invocations_s = 0
        Generic.old_loot_404.max_period_between_invocations_s = 0
        b1 = copy(Generic.old_loot_404)
        b2 = copy(Generic.old_loot_404)
        b1.count = randint(100, 600)
        b2.count = randint(100, 600)
        yield b1
        yield Generic.old_loot_success
        yield b2

    @staticmethod
    def dynamic_command_injection():
        yield ActivityPattern(count=5).add_interaction(interactions.dynamic.faq_rfi)
        yield ActivityPattern(
            count=(randint(4, 8)), suppress_noise=True
        ).add_interaction(interactions.dynamic.cmd_injection_on_sticky_page_recon)
        yield ActivityPattern(
            count=(randint(1, 2)), suppress_noise=True
        ).add_interaction(interactions.dynamic.cmd_injection_on_sticky_page_attack)
