from models import Interaction


class html:
    index_success = Interaction(
        uri="index.html",
        append_extension=False,
    )
    index_redirect = Interaction(
        uri="index.html",
        append_extension=False,
        status_code=302,
    )


class misc:
    favico_success = Interaction(
        uri="favico.ico", set_as_last=False, append_extension=False
    )
    root_success = Interaction(uri="", append_extension=False)
    wp_page_success = Interaction(
        uri="", query="p=__rand_int__", append_extension=False
    )
    wp_jpg_success = Interaction(
        uri="/var/www/wordpress/2021/0__rand_digit__/__rand_two_words__-1024x800.jpg",
        set_as_last=False,
        append_extension=False,
    )


class css:
    main_success = Interaction(
        uri="main.css", set_as_last=False, append_extension=False
    )
    footer_success = Interaction(
        uri="footer.css", set_as_last=False, append_extension=False
    )
    template_success = Interaction(
        uri="template.css",
        query="v=__rand_str__",
        set_as_last=False,
        append_extension=False,
    )
    rand_not_found = Interaction(
        uri="__rand_str__.css",
        status_code=404,
        set_as_last=False,
        append_extension=False,
    )
    rand_success = Interaction(
        uri="__rand_str__.css", set_as_last=False, append_extension=False
    )
    common_success = Interaction(
        uri="__rand_css_file__.css", set_as_last=False, append_extension=False
    )
    wp_theme_versioned_success = Interaction(
        uri="wp-content/themes/__theme__/assets/css/__rand_css_file__.css",
        query="ver=__rand_digit__.__rand_digit__.__rand_int__",
        set_as_last=False,
        append_extension=False,
    )
    wp_versioned_success = Interaction(
        uri="wp-includes/css/dist/block-library/__rand_css_file__.css",
        query="ver=__rand_digit__.__rand_digit__.__rand_int__",
        set_as_last=False,
        append_extension=False,
    )


class js:
    rand_success = Interaction(
        uri="__rand_str__.js",
        query="v=__rand_long__",
        set_as_last=False,
        append_extension=False,
    )
    wp_theme_versioned_success = Interaction(
        uri="wp-content/themes/__theme__/assets/js/__rand_js_file__.css",
        query="ver=__rand_digit__.__rand_digit__.__rand_int__",
        set_as_last=False,
        append_extension=False,
    )
    wp_versioned_success = Interaction(
        uri="wp-includes/js/__rand_js_file__.js",
        query="ver=__rand_digit__.__rand_digit__.__rand_int__",
        set_as_last=False,
        append_extension=False,
    )


class generic:
    seo_friendly_success = Interaction(
        uri="__rand_app_page_name__", append_extension=False
    )
    noise_sucess = Interaction(
        uri="__rand_noise__",
        set_as_last=False,
        append_extension=False,
    )
    old_loot_success = Interaction(
        uri="__loot__.__backup_ext__", append_extension=False, set_as_last=False
    )
    old_loot_404 = Interaction(
        uri="__loot__.__backup_ext__",
        append_extension=False,
        status_code=404,
        set_as_last=False,
    )


class dynamic:
    login_success = Interaction(
        uri="login",
    )

    index_seo_friendly_success = Interaction(
        uri="index__app_extension__/__rand_app_page_name__", append_extension=False
    )

    xmlrpc_success = Interaction(uri="xmlrpc", method="POST", set_as_last=False)

    login_post_301 = Interaction(
        uri="login", method="POST", status_code=301, login=True
    )

    login_post_401 = Interaction(uri="login", method="POST", status_code=401)

    account_status = Interaction(
        uri="account_status",
    )

    transaction = Interaction(
        uri="transactions",
        query="page=__inc_int__",
    )
    logout_success = Interaction(uri="logout", status_code=301, logout=True)
    transfer_get_success = Interaction(
        uri="transfer",
    )
    transfer_post_success = Interaction(
        uri="transfer",
        status_code=200,
        method="POST",
        query="accountid=__rand_long__",
    )
    transfer_complete_success = Interaction(uri="transfer_complete")
    myaccount_success = Interaction(uri="account")
    change_avatar_post_success = Interaction(
        uri="change_avatar",
        average_bytes=30000,
        deviation_bytes=10000,
        method="POST",
        status_code=301,
    )
    change_password_get_success = Interaction(uri="changepassword")
    change_password_post_success = Interaction(
        uri="changepassword", method="POST", status_code=301
    )
    faq_success = Interaction(uri="faq", query="locale=english")
    faq_lfi = Interaction(uri="faq", query="locale=__rand_str__")
    faq_rfi = Interaction(uri="faq", query="locale=http://__rand_str__.io:__rand_int__/__rand_str____app_extension__.txt%00")
    sticky_page_500 = Interaction(uri="__rand_sticky_str__", status_code=500)
    cmd_injection_on_sticky_page_recon = Interaction(
        uri="__rand_sticky_str__", query="cmd=__rand_cmd_recon__"
    )

    cmd_injection_on_sticky_page_attack = Interaction(
        uri="__rand_sticky_str__", query="cmd=__rand_cmd_attack__"
    )

    wp_admin_login_page_success = Interaction(uri="wp-login")

    wp_admin_login_success = Interaction(
        uri="wp-login", method="POST", status_code=301, login=True
    )

    wp_admin_login_failed = Interaction(uri="wp-login", method="POST", status_code=401)
    wp_admin_update_success = Interaction(uri="wp-admin/update-core")

    wp_admin_users_success = Interaction(uri="wp-admin/users")

    wp_admin_users_post_success = Interaction(uri="wp-admin/users", method="POST")

    wp_admin_plugins_success = Interaction(uri="wp-admin/plugins")

    wp_admin_plugins_install_post_success = Interaction(
        uri="wp-admin/plugins",
        method="POST",
        query="action=install-plugin&plugin=__rand_two_words__",
    )

    wp_admin_plugins_install_success = Interaction(
        uri="wp-admin/plugins-install",
    )

    wp_admin_health_success = Interaction(uri="wp-admin/site-health")
