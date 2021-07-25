from random import randint
from models import ActivityPattern, Interaction
import interactions
from copy import copy


class Banking:
    static_navigate_to_transactions = ActivityPattern(
        consecutive=True
    ).add_interactions([interactions.php.account_status, interactions.php.transaction])
    static_browse_transactions_short = ActivityPattern(count=5).add_interaction(
        interactions.php.transaction
    )
    static_browse_transactions = ActivityPattern().add_interaction(
        interactions.php.transaction
    )
    static_transfer = ActivityPattern(consecutive=True).add_interactions(
        [
            interactions.php.transfer_get_success,
            interactions.php.transfer_post_success,
            interactions.php.transfer_complete_success,
        ]
    )

    @staticmethod
    def dynamic_routine_use():
        gohome = copy(Misc.static_home_page)
        gohome.count = randint(2, 8)
        yield gohome
        yield Misc.static_home_page
        if randint(0, 19) == 0:
            # 1 in twenty chance of faq
            yield Misc.static_faq
        if randint(0, 9) == 0:
            # 1 in ten chance of wrong password
            for i in range(0, randint(1, 3)):
                yield Misc.static_login_failed
        yield Misc.static_login
        yield Banking.static_navigate_to_transactions
        browse = copy(Banking.static_browse_transactions)
        browse.count = randint(1, 6)
        yield browse
        if randint(0, 6) == 0:
            # if we roll a 6, do a tx
            yield Banking.static_transfer
        if randint(0, 49) == 0:
            # 1 in 50 chance of password reset
            yield Misc.static_password_reset
        if randint(0, 99) == 0:
            #    # 1 in 100 chance of password reset
            yield Misc.static_change_avatar
        if randint(0, 3) == 0:
            # 1 if 4 chance of logging out
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
    static_home_page = ActivityPattern(
        min_period_between_invocations_s=1, max_period_between_invocations_s=2, count=4
    ).add_interactions(
        [
            interactions.html.index_success,
            interactions.html.index_success,
            interactions.misc.favico_success,
            interactions.css.main_success,
            interactions.css.template_success,
            interactions.css.footer_success,
            interactions.css.rand_success,
            interactions.css.rand_not_found,
        ]
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
        interactions.html.index_redirect
    )
    static_login = ActivityPattern(consecutive=True).add_interactions(
        [
            interactions.html.index_redirect,
            interactions.php.login_success,
            interactions.php.login_post_301,
        ]
    )
    static_password_reset = ActivityPattern(consecutive=True).add_interactions(
        [
            interactions.php.change_password_get_success,
            interactions.php.change_password_post_success,
            interactions.php.account_status,
        ]
    )
    static_logout = ActivityPattern(consecutive=True).add_interaction(
        interactions.php.logout_success
    )
    static_login_failed = ActivityPattern(
        consecutive=True, min_period_between_invocations_s=1
    ).add_interaction(interactions.php.login_post_401)

    static_faq = ActivityPattern(consecutive=True).add_interaction(
        interactions.php.faq_success
    )

    static_change_avatar = ActivityPattern(consecutive=True).add_interactions(
        [
            interactions.php.account_status,
            interactions.php.change_avatar_post_success,
            interactions.php.account_status,
        ]
    )

    @staticmethod
    def dynamic_brute_force():
        yield Misc.static_login_page
        yield ActivityPattern(
            max_period_between_invocations_s=3,
            min_period_between_invocations_s=1,
            count=randint(0, 300),
        ).add_interaction(interactions.php.login_post_401)
        yield ActivityPattern(
            consecutive=True,
            max_period_between_invocations_s=3,
            min_period_between_invocations_s=1,
        ).add_interaction(interactions.php.login_post_301)

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
                interactions.php.faq_lfi
            )
        # TODO: this should have noise suppression
        yield ActivityPattern(count=(randint(4, 8))).add_interaction(
            interactions.php.cmd_injection_on_sticky_page_recon
        )
        yield ActivityPattern(count=(randint(1, 2))).add_interaction(
            interactions.php.cmd_injection_on_sticky_page_attack
        )
