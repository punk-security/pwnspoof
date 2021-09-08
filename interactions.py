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
    root_success = Interaction(uri="")
    wp_page_success = Interaction(uri="", query="p=__rand_int__")
    wp_jpg_success = Interaction(
        uri="/var/www/wordpress/2021/0__rand_digit__/__rand_two_words__-1024x800.jpg",
        set_as_last=False,
    )


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
    common_success = Interaction(uri="__rand_css_file__.css", set_as_last=False)
    wp_theme_versioned_success = Interaction(
        uri="wp-content/themes/__theme__/assets/css/__rand_css_file__.css",
        query="?ver=__rand_digit__.__rand_digit__.__rand_int__",
        set_as_last=False,
    )
    wp_versioned_success = Interaction(
        uri="wp-includes/css/dist/block-library/__rand_css_file__.css",
        query="?ver=__rand_digit__.__rand_digit__.__rand_int__",
        set_as_last=False,
    )


class js:
    rand_success = Interaction(
        uri="__rand_str__.js", query="v=__rand_long__", set_as_last=False
    )
    wp_theme_versioned_success = Interaction(
        uri="wp-content/themes/__theme__/assets/js/__rand_js_file__.css",
        query="?ver=__rand_digit__.__rand_digit__.__rand_int__",
        set_as_last=False,
    )
    wp_versioned_success = Interaction(
        uri="wp-includes/js/__rand_js_file__.js",
        query="?ver=__rand_digit__.__rand_digit__.__rand_int__",
        set_as_last=False,
    )


class php:
    login_success = Interaction(
        uri="login.php",
    )

    index_seo_friendly_success = Interaction(uri="index.php/__rand_app_page_name__")

    xmlrpc_success = Interaction(uri="xmlrpc.php", method="POST", set_as_last=False)

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
    sticky_page_500 = Interaction(uri="__rand_sticky_str__.php", status_code=500)
    cmd_injection_on_sticky_page_recon = Interaction(
        uri="__rand_sticky_str__.php", query="cmd=__rand_cmd_recon__"
    )

    cmd_injection_on_sticky_page_attack = Interaction(
        uri="__rand_sticky_str__.php", query="cmd=__rand_cmd_attack__"
    )

    wp_admin_login_page_success = Interaction(uri="wp-login.php")

    wp_admin_login_success = Interaction(
        uri="wp-login.php", method="POST", status_code=301, login=True
    )

    wp_admin_login_failed = Interaction(
        uri="wp-login.php", method="POST", status_code=401
    )
    wp_admin_update_success = Interaction(uri="wp-admin/update-core.php")

    wp_admin_users_success = Interaction(uri="wp-admin/users.php")

    wp_admin_users_post_success = Interaction(uri="wp-admin/users.php", method="POST")

    wp_admin_plugins_success = Interaction(uri="wp-admin/plugins.php")

    wp_admin_plugins_install_post_success = Interaction(
        uri="wp-admin/plugins.php",
        method="POST",
        query="action=install-plugin&plugin=__rand_two_words__",
    )

    wp_admin_plugins_install_success = Interaction(
        uri="wp-admin/plugins-install.php",
    )

    wp_admin_health_success = Interaction(uri="wp-admin/site-health.php")
