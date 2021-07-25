from models import Interaction


class html:
    index_success = Interaction(
        uri="index.html",
    )
    index_redirect = Interaction(
        uri="index.html",
        status_code=302,
    )


class misc:
    favico_success = Interaction(uri="favico.ico", set_as_last=False)


class css:
    main_success = Interaction(uri="main.css", set_as_last=False)
    footer_success = Interaction(uri="footer.css", set_as_last=False)
    template_success = Interaction(
        uri="template.css", query="v=__rand_str__", set_as_last=False
    )
    rand_not_found = Interaction(
        uri="__rand_str__.css", status_code=404, set_as_last=False
    )
    rand_success = Interaction(uri="__rand_str__.css", set_as_last=False)


class js:
    rand_success = Interaction(
        uri="__rand_str__.css", query="v=__rand_long__", set_as_last=False
    )


class php:
    login_success = Interaction(
        uri="login.php",
    )

    login_post_301 = Interaction(
        uri="login.php", method="POST", status_code=301, login=True
    )

    login_post_401 = Interaction(uri="login.php", method="POST", status_code=401)
    account_status = Interaction(
        uri="account_status.php",
    )

    transaction = Interaction(
        uri="transactions.php",
        query="page=__inc_int__",
    )
    logout_success = Interaction(uri="logout.php", status_code=301, logout=True)
    transfer_get_success = Interaction(
        uri="transfer.php",
    )
    transfer_post_success = Interaction(
        uri="transfer.php",
        status_code=200,
        method="POST",
        query="accountid=__rand_long__",
    )
    transfer_complete_success = Interaction(uri="transfer_complete.php")
    myaccount_success = Interaction(uri="account.php")
    change_avatar_post_success = Interaction(
        uri="change_avatar.php",
        average_bytes=30000,
        deviation_bytes=10000,
        method="POST",
        status_code=301,
    )
    change_password_get_success = Interaction(uri="changepassword.php")
    change_password_post_success = Interaction(
        uri="changepassword.php", method="POST", status_code=301
    )
    faq_success = Interaction(uri="faq.php", query="locale=english")
    faq_lfi = Interaction(uri="faq.php", query="locale=__rand_str__")
    cmd_injection_on_sticky_page_recon = Interaction(
        uri="__rand_sticky_str__.php", query="cmd=__rand_cmd_recon__"
    )

    cmd_injection_on_sticky_page_attack = Interaction(
        uri="__rand_sticky_str__.php", query="cmd=__rand_cmd_attack__"
    )
